import tomli

def fetch_project_settings() -> list[str]:
    with open('settings.toml', 'rb') as f:
        config = tomli.load(f)
        base_path = config['project']['base_path']
        source_language = config['project']['source_lang']
        target_languages = config['project']['target_lang']
    return [base_path, source_language, target_languages]

def fetch_folder_mappings() -> dict[str, str]:
    with open('settings.toml', 'rb') as f:
        config = tomli.load(f)
        folder_mappings = config['language_folder_mapper']
    return folder_mappings

def fetch_program_settings() -> dict[str, str]:
    with open('settings.toml', 'rb') as f:
        config = tomli.load(f)
        program_settings = config['program']
    return program_settings


print(fetch_program_settings())