from constants.log_levels import LogLevel
from settings_fetcher import fetch_folder_mappings
from file_handler import fetch_source_files, fetch_target_files, fetch_file_content, write_to_file
from translator import Translator
from interactor import log_in_console, get_user_response
import concurrent.futures
from deep_translator.exceptions import TooManyRequests

class TranslationManager:
    def __init__(self, translator, base_path, source_language, target_languages):
        self.translator: Translator = translator
        self.base_path = base_path
        self.source_language = source_language
        self.target_languages = target_languages
        self.folder_mappings = fetch_folder_mappings()
        
        self.source_files = fetch_source_files(f'{self.base_path}\\{self.folder_mappings[self.source_language]}')
    
    def execute_translations(self):
        self.source_key_values = self.get_source_key_values()
        self.verify_target_files_exist()
        self.keys_by_file_to_translate = self.get_keys_by_file_to_translate()
        self.translate_keys()
        self.write_translations()
        
    def write_translations(self):
        log_in_console("Writing translations to the target files...", LogLevel.INFO)
        
        def write_file(lang, file_to_translate):
            file_name = file_to_translate['file_name']
            target_file = fetch_file_content(f'{self.base_path}\\{self.folder_mappings[lang]}\\{file_name}')
            for key in file_to_translate['keys']:
                source_key_value = next((source_key for source_key in self.source_key_values if source_key['file_name'] == file_name), None)
                if source_key_value:
                    source_key = next((source_key for source_key in source_key_value['content'] if source_key['key'] == key), None)
                    if source_key:
                        translated_value = source_key['value']
                        target_file[key] = translated_value
            log_in_console(f"Writing translations to {file_name} in {lang}...", LogLevel.INFO)
            write_to_file(f'{self.base_path}\\{self.folder_mappings[lang]}\\{file_name}', target_file, ensure_ascii=False)
            log_in_console(f"Translations written to {file_name} in {lang}.", LogLevel.INFO)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for lang in self.target_languages:
                lang_content = next((item for item in self.keys_by_file_to_translate if item['lang'] == lang), None)
                if lang_content:
                    for file_to_translate in lang_content['content']:
                        futures.append(executor.submit(write_file, lang, file_to_translate))
            concurrent.futures.wait(futures)
                    
    def translate_keys(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            def translate_batch_keys(lang, file_to_translate):
                source_key_value = next((src for src in self.source_key_values if src['file_name'] == file_to_translate['file_name']), None)
                if source_key_value:
                    # Collect all texts to translate
                    texts_to_translate = []
                    for key in file_to_translate['keys']:
                        src_key = next((s for s in source_key_value['content'] if s['key'] == key), None)
                        if src_key:
                            texts_to_translate.append(src_key['value'])
                    # Perform batch translation
                    try:
                        if len(texts_to_translate) > 0:
                            log_in_console(f"Translating {len(texts_to_translate)} keys in {file_to_translate['file_name']} to {lang}...", LogLevel.INFO)
                            translated_values = self.translator.translate_batch(texts_to_translate, self.source_language, lang)
                    except TooManyRequests:
                        log_in_console("Too many requests made to the translation API. Please try again later. Exiting the program.", LogLevel.CRITICAL)
                        return
                    # Assign translations back
                    for i, key in enumerate(file_to_translate['keys']):
                        source_key = next((src for src in source_key_value['content'] if src['key'] == key), None)
                        if source_key:
                            source_key['value'] = translated_values[i]

            for lang in self.target_languages:
                lang_content = next((item for item in self.keys_by_file_to_translate if item['lang'] == lang), None)
                if lang_content:
                    for file_to_translate in lang_content['content']:
                        executor.submit(translate_batch_keys, lang, file_to_translate)
            
    def get_source_key_values(self) -> list[dict]:
        source_key_value_pair_list: list[dict] = []
        for source_file in self.source_files:
            source_file_content = source_file['content']
            key_value_pairs = []
            for key, value in source_file_content.items():
                key_value_pairs.append({
                    'key': key,
                    'value': value
                })
            source_key_value_pair_list.append({
                'file_name': source_file['file_name'],
                'content': key_value_pairs
            })
        return source_key_value_pair_list
    
    def verify_target_files_exist(self):
        for lang in self.target_languages:
            target_files = fetch_target_files(f'{self.base_path}\\{self.folder_mappings[lang]}')
            
            for source_file in self.source_files:
                source_file_name = source_file['file_name']
                target_file = next((file for file in target_files if file['file_name'] == source_file_name), None)
                if target_file is None:
                    log_in_console(f"File {source_file_name} does not exist in {lang} folder.", LogLevel.INFO)
                    log_in_console(f"Creating {source_file_name} file in {lang} folder...", LogLevel.INFO)
                    with open(f'{self.base_path}\\{self.folder_mappings[lang]}\\{source_file_name}', 'w') as f:
                        f.write('{}')
    
    def get_keys_by_file_to_translate(self) -> list[dict]:
        list_to_translate: list[dict] = []
        is_translation_required = False
        for lang in self.target_languages:
            keys_to_translate_in_lang = []
            for source_file in self.source_files:
                file_name = source_file['file_name']
                dest_file_contents = fetch_file_content(f'{self.base_path}\\{self.folder_mappings[lang]}\\{file_name}')
                keys_to_translate = set(source_file['content'].keys()) - set(dest_file_contents.keys())
                if keys_to_translate:
                    is_translation_required = True
                keys_to_translate_in_lang.append({
                    'file_name': file_name,
                    'keys': keys_to_translate
                })
            list_to_translate.append({
                'lang': lang,
                'content': keys_to_translate_in_lang
            })

        if not is_translation_required:
            log_in_console("All your files are in sync. You're good to go! Exiting the program.", LogLevel.INFO)
            exit()
        else:
            log_in_console("There are some files not in sync with the source files. Beginning translation...", LogLevel.INFO)
        
        return list_to_translate
