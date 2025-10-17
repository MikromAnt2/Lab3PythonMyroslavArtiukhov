import json
import os
import asyncio

CONFIG_FILE = "config.json"

def loadModules():
    backends = {}
    try:
        from trans.dtranslator import TransLate as deep_translate
        backends['deep'] = deep_translate
    except:
        backends['deep'] = None
    
    try:
        from trans.gtranslator import TransLate as google_translate
        backends['google'] = google_translate
    except:
        backends['google'] = None
    
    return backends

def textStats(text):

    chars = len(text)
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    return chars, words, sentences

async def translateFile(config):
    backends = loadModules()
    backend_name = config.get("module", "deep")
    backend = backends.get(backend_name)
    
    if not backend:
        print(f"Модуль '{backend_name}' недоступний")
        return

    input_file = config["input_file"]
    target_lang = config["target_language"]
    output_mode = config["output"]
    max_chars = config["max_characters"]
    max_words = config["max_words"]
    max_sentences = config["max_sentences"]
    if not os.path.exists(input_file):
        print(f"Файл '{input_file}' не знайдено")
        return
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    chars, words, sentences = textStats(text)
    print(f"Файл: {input_file}")
    print(f"Розмір: {os.path.getsize(input_file)} байт")
    print(f"Статистика: {chars} символів, {words} слів, {sentences} речень")

    lines = text.splitlines()
    text_to_translate = ""
    current_chars = current_words = current_sentences = 0

    for line in lines:
        line_chars, line_words, line_sentences = textStats(line)
        if (current_chars + line_chars > max_chars or
            current_words + line_words > max_words or
            current_sentences + line_sentences > max_sentences):
            break
        
        text_to_translate += line + " "
        current_chars += line_chars
        current_words += line_words
        current_sentences += line_sentences

    try:
        translated = await backend(text_to_translate.strip(), "auto", target_lang)
    except Exception as e:
        print(f"Помилка перекладу: {e}")
        return

    if output_mode == "screen":
        print(f"\nМова: {target_lang}")
        print(f"Модуль: {backend_name}")
        print(f"Переклад:\n{translated}")
    elif output_mode == "file":
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_{target_lang}{ext}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated)
        print(f"Збережено у: {output_file}")

if __name__ == "__main__":
    if os.path.exists(CONFIG_FILE):
        config = json.load(open(CONFIG_FILE, "r", encoding="utf-8"))
        asyncio.run(translateFile(config))
    else:
        print(f"Файл {CONFIG_FILE} не знайдено")