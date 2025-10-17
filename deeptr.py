import asyncio

from trans.dtranslator import TransLate, LangDetect, CodeLang, LanguageList

async def main():
    print("Переклад:", await TransLate("Де Аліса?", "uk", "en"))
    print("Визначення мови:", await LangDetect("Where is Alice?"))
    print("Код мови для 'uk':", await CodeLang("uk"))
    print("Cписок мов:")
    await LanguageList("screen", "Where is Alice?")

if __name__ == "__main__":
    asyncio.run(main())
