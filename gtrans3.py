from trans.gtranslatoOld import TransLate, LangDetect, CodeLang, LanguageList

print("Переклад:", TransLate("Де Аліса?", "uk", "en"))
print("Визначення мови:", LangDetect("Where is Alice?"))
print("Код мови для 'uk':", CodeLang("uk"))
print("Cписок мов:")
LanguageList("screen", "Where is Alice?")
