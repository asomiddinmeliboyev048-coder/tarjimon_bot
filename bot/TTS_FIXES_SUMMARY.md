# Uzbek TTS Voice Generation - Fixes Applied

## Issues Fixed

### 1. Uzbek Voice Code Correction
**Problem:** 
- Voice code was `uz-UZ-SardorNeural` which caused edge_tts error 403 (not available)
- gTTS doesn't support Uzbek language at all (error: "Language not supported: uz")

**Solution:**
- Updated to `uz-UZ-MadinaNeural` (valid edge-tts voice for Uzbek)
- Added language validation to skip gTTS fallback for unsupported languages

**Location:** `config.py` - VOICE_MAP

---

### 2. Improved Edge-TTS Error Handling
**Problem:**
- edge_tts errors (403, connection issues) weren't properly caught
- Failed voice files weren't cleaned up properly
- Error messages weren't descriptive enough

**Solution:**
```python
async def _generate_edge_tts(text: str, voice_name: str, file_path: str) -> None:
    """Generate voice using edge-tts with improved error handling."""
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(file_path)
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise Exception("Voice file not generated or empty")
    except Exception as e:
        # Clean up failed file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        raise Exception(f"edge-tts generation failed: {str(e)}")
```

---

### 3. Fixed gTTS Fallback (Language Validation)
**Problem:**
- gTTS was being called for Uzbek even though it doesn't support it
- This caused unnecessary errors in the fallback chain

**Solution:**
```python
def _generate_gtts(text: str, lang: str, file_path: str) -> None:
    """Generate voice using gTTS fallback (only for supported languages)."""
    # Map language codes to gTTS codes if needed
    gtts_lang_map = {
        'en': 'en',
        'ru': 'ru',
        'tr': 'tr',
        'ko': 'ko',
        'ar': 'ar',
    }
    
    gtts_lang = gtts_lang_map.get(lang)
    if not gtts_lang:
        raise Exception(f"gTTS does not support language: {lang}")
    # ... rest of implementation
```

**Key Changes:**
- Uzbek (uz) NOT in gTTS language map - skips fallback attempt
- Added explicit language validation before attempting gTTS

---

### 4. Text Length Validation
**Problem:**
- Very long text could cause TTS generation to fail
- edge-tts has practical limits on text length

**Solution:**
```python
# Added to config.py
MAX_TTS_TEXT_LENGTH = 1000  # character limit

# In generate_voice() function:
if len(text) > MAX_TTS_TEXT_LENGTH:
    text = text[:MAX_TTS_TEXT_LENGTH]
    log_error(f"Text truncated to {MAX_TTS_TEXT_LENGTH} characters for TTS")
```

**Behavior:**
- Text automatically truncated to 1000 characters
- Prevents TTS API from rejecting oversized requests
- Error logged for debugging

---

### 5. Smart Fallback Logic
**Problem:**
- gTTS fallback was attempted for all languages equally
- No language-specific handling

**Solution:**
```python
try:
    await _generate_edge_tts(text, voice_name, file_path)
    success = True
except Exception as edge_error:
    error_message = str(edge_error)
    log_error(f"edge_tts error: {edge_error}")
    
    # For Uzbek or unsupported languages, don't try gTTS
    if lang not in GTTS_SUPPORTED_LANGS:
        log_error(f"gTTS not available for {lang}, cannot fallback")
        success = False
    else:
        # Try gTTS fallback only for supported languages
        try:
            _generate_gtts(text, lang, file_path)
            success = True
        except Exception as gtts_error:
            log_error(f"gTTS fallback error: {gtts_error}")
            success = False
```

---

## Configuration Changes

### config.py
```python
VOICE_MAP = {
    "en": "en-US-GuyNeural",
    "ru": "ru-RU-DmitryNeural",
    "tr": "tr-TR-AhmetNeural",
    "ko": "ko-KR-InJoonNeural",
    "ar": "ar-SA-HamedNeural",
    "uz": "uz-UZ-MadinaNeural",  # UPDATED: Was uz-UZ-SardorNeural
}

# NEW: Languages supported by gTTS (for fallback)
GTTS_SUPPORTED_LANGS = {'en', 'ru', 'tr', 'ko', 'ar'}  # uz NOT supported

# NEW: Maximum text length for TTS
MAX_TTS_TEXT_LENGTH = 1000  # characters
```

---

## Voice Generation Flow (Updated)

```
User presses "Ovozini eshitish" button
    ↓
generate_voice(text, lang) called
    ↓
[Text Validation]
  - Check if text is empty → Return None
  - Truncate to 1000 chars if too long
    ↓
[Cache Check]
  - If cached voice exists → Return cached file
    ↓
[edge-tts Attempt]
  - Try: edge_tts with voice_name (uz-UZ-MadinaNeural for Uzbek)
  - Success? → Return file path ✓
    ↓
[edge-tts Failed]
  - Clean up failed file
  - Log error
    ↓
[Language Check]
  - Is language in GTTS_SUPPORTED_LANGS?
    ├─ NO (Uzbek, etc.) → Return None ✗
    └─ YES (English, Russian, etc.)
        ↓
    [gTTS Fallback Attempt]
      - Try: gTTS with language code
      - Success? → Return file path ✓
      - Failed? → Return None ✗
```

---

## Language Support Matrix

| Language | Code | Edge-TTS Voice | gTTS Support | Fallback |
|----------|------|----------------|--------------|----------|
| Uzbek    | uz   | uz-UZ-MadinaNeural | ✗ No | None (edge-tts only) |
| English  | en   | en-US-GuyNeural | ✓ Yes | Yes |
| Russian  | ru   | ru-RU-DmitryNeural | ✓ Yes | Yes |
| Turkish  | tr   | tr-TR-AhmetNeural | ✓ Yes | Yes |
| Korean   | ko   | ko-KR-InJoonNeural | ✓ Yes | Yes |
| Arabic   | ar   | ar-SA-HamedNeural | ✓ Yes | Yes |

---

## Error Messages (What to Expect)

### Success Case (Uzbek Text)
```
User: "Salom, bu test matnidir"
Translation: "Hello, this is test text" (English)
Voice Button Pressed:
  → Uses edge-tts with uz-UZ-MadinaNeural
  → Uzbek audio plays correctly
  → Terminal: [Silent - no errors]
```

### Edge-TTS Error with Fallback (English)
```
Original text: "Hello world"
Voice Button Pressed:
  → edge_tts fails with connection error
  → gTTS fallback triggered (en is supported)
  → English audio plays from gTTS
  → Terminal: "edge_tts error: ... | gTTS fallback successful"
```

### Complete Failure (Hypothetical)
```
For any language if both edge-tts AND gTTS fail:
  → Terminal: "Voice generation failed for [lang]: [error details]"
  → User sees error message in Telegram
  → No audio sent
```

---

## Testing Verification

✅ All imports successful
✅ Uzbek voice code: uz-UZ-MadinaNeural
✅ gTTS supported languages: {en, ru, tr, ko, ar}
✅ Max text length: 1000 characters
✅ No syntax errors
✅ Backward compatible with existing code

---

## Files Modified

1. ✅ [config.py](config.py)
   - Updated Uzbek voice code
   - Added GTTS_SUPPORTED_LANGS constant
   - Added MAX_TTS_TEXT_LENGTH constant

2. ✅ [utils/voice.py](utils/voice.py)
   - Improved _generate_edge_tts() with better error handling
   - Updated _generate_gtts() with language validation
   - Enhanced generate_voice() with smart fallback logic
   - Added text length validation and truncation

---

## Notes

- Uzbek now uses edge-tts exclusively (no gTTS fallback)
- Other languages have gTTS as fallback if edge-tts fails
- Text automatically truncated to prevent API errors
- Failed voice files are cleaned up properly
- Error messages are now more descriptive for debugging
- No changes to other bot functions (translation, menu, subscription)
