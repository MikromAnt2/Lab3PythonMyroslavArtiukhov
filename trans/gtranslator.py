import asyncio
from googletrans import Translator, LANGUAGES

translator = Translator()

async def TransLate(text: str, src: str, dest: str) -> str:
    try:
        result = await translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {e}"

async def LangDetect(text: str, set: str = "all") -> str:
    try:
        result = await translator.detect(text)
        if set == "lang":
            return result.lang
        elif set == "confidence":
            return str(result.confidence)
        return f"Мова: {result.lang}, довіра: {result.confidence}"
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
                    tr = await translator.translate(text, dest=code)
                    translated_text = tr.text
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
        return f"Помилка створення списку мов: {e}"