import argparse
from backup_manager import create_backup, delete_backup
from settings_fetcher import fetch_project_settings, fetch_program_settings
from translation_manager import TranslationManager
from translator import Translator
from interactor import log_in_console, get_user_response
from constants.log_levels import LogLevel

def manage_backup(post_translation: bool, source_dir: str):
    backup_settings = fetch_program_settings()
    if not post_translation:
        if backup_settings['enable_temp_backup']:
            if backup_settings['temp_backup_dest'] == '':
                continue_program = get_user_response("Temp backup destination not specified in settings.toml. Do you want to continue without temp backup? (yes/no): ")
                if not continue_program:
                    log_in_console("Exiting the program.", LogLevel.INFO)
                    exit()
                else:
                    log_in_console("Continuing without temp backup.", LogLevel.INFO)
            else:
                log_in_console("Creating temp backup...", LogLevel.INFO)
                create_backup(source_dir, backup_settings['temp_backup_dest'])
                log_in_console("Temp backup created successfully.", LogLevel.INFO)
    else:
        if backup_settings['enable_temp_backup'] and backup_settings['delete_backup_after_successful_completion']:
            log_in_console("Deleting temp backup...", LogLevel.INFO)
            delete_backup(backup_settings['temp_backup_dest'])
            log_in_console("Temp backup deleted successfully.", LogLevel.INFO)

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
    
    manage_backup(False, base_path)
    
    log_in_console("Base path: %s" % base_path, LogLevel.INFO)
    log_in_console("Source language: %s" % settings_source_language, LogLevel.INFO)
    log_in_console("Target languages: %s" % settings_target_languages, LogLevel.INFO)
    
    translator = Translator(settings_source_language, settings_target_languages)
    translation_manager = TranslationManager(translator, base_path, settings_source_language, settings_target_languages)

    translation_manager.execute_translations()
    
    log_in_console("Translations completed successfully. You're good to go!", LogLevel.INFO)
    manage_backup(False, base_path)
    

if __name__ == '__main__':
    main()
