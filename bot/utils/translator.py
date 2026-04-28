from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError, LanguageNotSupportedException
from langdetect import detect, LangDetectException
import asyncio
import time
from config import TRANSLATION_MAX_RETRIES, TRANSLATION_TIMEOUT, DEFAULT_SOURCE_LANG
from utils.logger import log_translation, log_error

# Simple in-memory cache for translations with TTL
translation_cache = {}
CACHE_TTL = 3600  # 1 hour
translation_semaphore = asyncio.Semaphore(20)

SUPPORTED_LANGUAGES = {'en', 'ru', 'tr', 'ko', 'ar', 'uz'}


def _get_cache_key(text: str, target_lang: str) -> str:
    """Generate cache key for translation"""
    return f"{text}:{target_lang}"


def _add_to_cache(cache_key: str, result: str):
    """Add translation result to cache with TTL"""
    global translation_cache
    translation_cache[cache_key] = {
        'result': result,
        'timestamp': time.time()
    }


async def detect_language(text: str, user_id: int = None) -> str:
    """Detect source language for incoming text using langdetect (free, no API keys needed).
    
    Special handling for Uzbek to distinguish it from Turkish and other similar languages.
    """
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()
    if not text:
        return DEFAULT_SOURCE_LANG

    # Check for Uzbek-specific patterns before running langdetect
    # Uzbek text often contains specific word patterns and Cyrillic variants.
    uzbek_indicators = [
        "bo'lib", "qilish", "iltimos", "xo'jalik", "o'rganish",
        "salom", "qanday", "nimada", "qayer", "nima", "kim",
        "men", "siz", "bu", "u", "yaxshi", "qayerda", "qachon",
        "har", "o'zbek", "uzbek", "qandaydir", "qanchalik"
    ]
    uzbek_cyrillic_chars = set('ғқҳўӣ')
    text_lower = text.lower()

    if any(indicator in text_lower for indicator in uzbek_indicators):
        return DEFAULT_SOURCE_LANG

    if any(ch in text for ch in uzbek_cyrillic_chars):
        return DEFAULT_SOURCE_LANG

    try:
        loop = asyncio.get_event_loop()
        detected = await asyncio.wait_for(
            loop.run_in_executor(None, detect, text),
            timeout=TRANSLATION_TIMEOUT
        )
        if isinstance(detected, str) and detected:
            detected_lang = detected.lower()
            # Normalize language codes (e.g., 'zh-cn' -> 'zh')
            if '-' in detected_lang:
                detected_lang = detected_lang.split('-')[0]

            # If Uzbek markers appear in a Turkish/Azeri detection, treat it as Uzbek.
            if detected_lang in {'tr', 'az', 'ru', 'en'}:
                uzbek_markers = ["o'", "g'", "sh", "ch", "q", "yo", "yu", "ya", "ng"]
                if any(marker in text_lower for marker in uzbek_markers):
                    return DEFAULT_SOURCE_LANG

            # If Turkish appears but Uzbek indicators exist, preserve Turkish only if no Uzbek signs exist.
            return detected_lang
    except asyncio.TimeoutError:
        log_error("Language detection timeout", user_id)
    except LangDetectException as e:
        log_error(f"Language detection failed: {e}", user_id)
    except Exception as e:
        log_error(f"Language detection error: {e}", user_id)

    return DEFAULT_SOURCE_LANG


async def translate_text(text: str, target_lang: str, user_id: int = None) -> tuple[str, str] | None:
    """
    Translate text using automatic source language detection.

    If the incoming text is Uzbek, it is translated into the user's selected foreign language.
    If the incoming text is non-Uzbek, it is translated into Uzbek.

    Args:
        text: Text to translate
        target_lang: User-selected foreign language code
        user_id: Optional user ID for logging

    Returns:
        Tuple of (translated_text, actual_target_lang) or None if translation failed
    """
    start_time = time.time()
    async with translation_semaphore:
        if not isinstance(text, str):
            text = str(text)

        text = text.strip()
        if not text:
            return None

        if target_lang not in SUPPORTED_LANGUAGES:
            log_error(f"Unsupported target language: {target_lang}", user_id)
            return None

        source_lang = await detect_language(text, user_id)

        if target_lang == DEFAULT_SOURCE_LANG:
            if source_lang == DEFAULT_SOURCE_LANG:
                log_error("Selected Uzbek while input is Uzbek: no translation needed", user_id)
                return None
            destination_lang = DEFAULT_SOURCE_LANG
        else:
            destination_lang = target_lang if source_lang == DEFAULT_SOURCE_LANG else DEFAULT_SOURCE_LANG

        cache_key = _get_cache_key(text, destination_lang)
        if cache_key in translation_cache:
            cache_entry = translation_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < CACHE_TTL:
                translated_text = cache_entry['result']
                duration = time.time() - start_time
                log_translation(user_id or 0, source_lang, destination_lang, True, duration=duration, cached=True)
                return translated_text, destination_lang
            else:
                del translation_cache[cache_key]

        last_error = None
        for attempt in range(TRANSLATION_MAX_RETRIES):
            try:
                # Use auto source detection in the translator to avoid echo when our heuristic misclassifies the language.
                translator = GoogleTranslator(source='auto', target=destination_lang)
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, translator.translate, text),
                    timeout=TRANSLATION_TIMEOUT
                )

                if result and isinstance(result, str) and result.strip():
                    translated_text = result.strip()
                    _add_to_cache(cache_key, translated_text)
                    duration = time.time() - start_time
                    log_translation(user_id or 0, source_lang, destination_lang, True, duration=duration, cached=False)
                    return translated_text, destination_lang

            except asyncio.TimeoutError:
                last_error = f"Timeout on attempt {attempt + 1}"
                log_error(f"Translation timeout (attempt {attempt + 1})", user_id)

            except TranslationNotFound:
                last_error = "Translation not found"
                log_error("Translation not found", user_id)
                return None

            except (RequestError, LanguageNotSupportedException) as e:
                last_error = f"API error: {e}"
                log_error(f"Translation API error: {e}", user_id)

            except Exception as e:
                last_error = f"Unexpected error: {e}"
                log_error(f"Translation unexpected error: {e}", user_id)

            if attempt < TRANSLATION_MAX_RETRIES - 1:
                wait_time = min(2 ** attempt, 8)
                await asyncio.sleep(wait_time)

        duration = time.time() - start_time
        log_error(f"Translation failed after {TRANSLATION_MAX_RETRIES} attempts: {last_error}", user_id)
        log_translation(user_id or 0, source_lang, destination_lang, False, duration=duration)
        return None


def clear_translation_cache():
    """Clear the translation cache"""
    global translation_cache
    translation_cache = {}


def get_cache_stats():
    """Get cache statistics"""
    current_time = time.time()
    valid_entries = sum(1 for entry in translation_cache.values() if current_time - entry['timestamp'] < CACHE_TTL)
    return {
        "size": len(translation_cache),
        "valid_entries": valid_entries,
        "ttl_seconds": CACHE_TTL
    }


