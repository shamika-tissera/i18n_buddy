import logging
from deep_translator import GoogleTranslator as GT

class Translator:
    """Translator class to translate text from source language to target languages.
    """
    def __init__(self, source: str | None, targets: list[str]):
        if source is None:
            logging.warning("""
                            No source language specified. Source language will be detected automatically.
                            """)
            self.source_language = "auto"
        else:
            self.source_language = source
        self.target_languages = targets

    def translate(self, text, source_lang, dest_lang) -> dict[str, str]:
        """Translate text from source language to target languages.
        """
        translations = {}
        for target in self.target_languages:
            translated_text = GT(source=source_lang, target=dest_lang).translate(text)
            translations[target] = translated_text
        return translations
    
    # use deep_translator's translate_batch
    def translate_batch(self, texts: list[str], source_lang, dest_lang) -> dict[str, str]:
        """Translate a batch of texts from source language to target languages.
        """
        if len(texts) == 0:
            return {}
        if dest_lang == "zh":
            dest_lang = "zh-CN"
        translations = GT(source=source_lang, target=dest_lang).translate_batch(texts)
        return translations
    