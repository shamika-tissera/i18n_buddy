import argparse
from settings_fetcher import fetch_project_settings
from translation_manager import TranslationManager
from translator import Translator
from interactor import log_in_console
from constants.log_levels import LogLevel

def main():
    
    parser = argparse.ArgumentParser(description='This program intends to help you with internationalization in your project.')
    parser.add_argument('--base-path', help="Enter the base path of your project's internationalization files. This will override the one specified in the settings.toml file", required=False)
    args = parser.parse_args()
    
    try:
        settings_base_path, settings_source_language, settings_target_languages = fetch_project_settings()
    except FileNotFoundError:
        log_in_console("Settings file not found. Please create a settings.toml file in the root directory. Exiting the program.", LogLevel.CRITICAL)
        return
    
    base_path = args.base_path if args.base_path else settings_base_path
    
    log_in_console("Base path: %s" % base_path, LogLevel.INFO)
    log_in_console("Source language: %s" % settings_source_language, LogLevel.INFO)
    log_in_console("Target languages: %s" % settings_target_languages, LogLevel.INFO)
    
    translator = Translator(settings_source_language, settings_target_languages)
    translation_manager = TranslationManager(translator, base_path, settings_source_language, settings_target_languages)

    translation_manager.execute_translations()
    
    log_in_console("Translations completed successfully. You're good to go!", LogLevel.INFO)
    

if __name__ == '__main__':
    main()
