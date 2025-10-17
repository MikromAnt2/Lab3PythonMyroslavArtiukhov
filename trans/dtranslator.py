import sys
import asyncio
from deep_translator import GoogleTranslator
from langdetect import detect_langs

def get_languages():
    return GoogleTranslator(source='auto', target='en').get_supported_languages(as_dict=True)

LANGUAGES = get_languages()

async def TransLate(text: str, src: str, dest: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, lambda: GoogleTranslator(source=src, target=dest).translate(text)
        )
        return result
    except Exception as e:
        return f"Помилка перекладу: {e}"

async def LangDetect(text: str, set: str = "all") -> str:
    try:
        loop = asyncio.get_event_loop()

        result = await loop.run_in_executor(None, lambda: detect_langs(text))
        lang = result[0].lang
        confidence = round(result[0].prob, 2)

        if set == "lang":
            return lang
        elif set == "confidence":
            return str(confidence)
        else:
            lang_name = next((name for name, code in LANGUAGES.items() if code == lang), lang)
            return f"Мова: {lang_name} ({lang}), довіра: {confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {e}"

async def CodeLang(lang: str) -> str:
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Помилка: мову не знайдено"

async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        rows = []
        for i, (code, name) in enumerate(list(LANGUAGES.items())[:10], 1):
            translated_text = ""
            if text:
                try:
                    loop = asyncio.get_event_loop()
                    translated_text = await loop.run_in_executor(
                        None, lambda: GoogleTranslator(source="auto", target=code).translate(text)
                    )
                except:
                    translated_text = "Error"
            rows.append((i, name.title(), code, translated_text))

        header = f"{'N':<4}{'Language':<20}{'ISO-639 code':<15}{'Text'}"
        separator = "-" * 60
        content = "\n".join([f"{n:<4}{lang:<20}{code:<15}{t}" for n, lang, code, t in rows])
        
        if out == "screen":
            print(f"{header}\n{separator}\n{content}\nOk")
        elif out == "file":
            with open("languages.txt", "w", encoding="utf-8") as f:
                f.write(f"{header}\n{separator}\n{content}\nOk\n")
        else:
            return "Помилка: некоректний параметр out"
            
        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 13:
        print("Python 3.13+")
    else:
        print(f"Python {version.major}.{version.minor}")

check_python_version()
