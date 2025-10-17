from googletrans import Translator, LANGUAGES

translator = Translator()

def CodeLang(lang: str) -> str:
    langToLow = lang.lower()
    if langToLow in LANGUAGES:
        return langToLow
    for code, name in LANGUAGES.items():
        if name.lower() == langToLow:
            return code
    return f"{lang}"

def LangDetect(text: str) -> str:
    try:
        detection = translator.detect(text)
        languageName = LANGUAGES.get(detection.lang, "Unknown")
        return f"{languageName.title()} ({detection.lang})"
    except:
        return "Err in LangDetect"

def TransLate(text: str, lang_from: str, lang_to: str) -> str:
    try:
        translated = translator.translate(text, src=lang_from, dest=lang_to)
        return translated.text
    except:
        return "Translation Error"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        rows = []
        for i, (code, name) in enumerate(list(LANGUAGES.items())[:10], 1):
            translated_text = ""
            if text:
                try:
                    translated_text = translator.translate(text, dest=code).text
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
