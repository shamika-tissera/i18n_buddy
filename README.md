# i18n_buddy

i18n_buddy is a tool designed to assist with the internationalization of your project by managing translations across different languages. It automates the process of translating JSON files, ensuring that your project can support multiple languages with ease.

## Features

- **Automatic Translation**: Uses the Google Translator API to translate text from a source language to multiple target languages.
- **Batch Processing**: Supports batch translation of multiple JSON files.
- **Customizable Settings**: Allows you to configure the base path, source language, and target languages via a `settings.toml` file.
- **Logging**: Provides detailed logging to help you track the translation process.
- **Error Handling**: Includes error handling for invalid JSON files and API rate limits.

## Usage

### Running from Source

1. Configure the [settings.toml](http://_vscodecontentref_/1) file in the root directory with your project settings:
    ```toml
    [project]
    base_path = 'path/to/your/locales'
    source_lang = "en"
    target_lang = ["am", "es", "fr", "ko", "vi", "zh"]

    [language_folder_mapper]
    en = "en"
    am = "am"
    es = "es"
    fr = "fr"
    ko = "ko"
    vi = "vi"
    zh = "zh"
    ```

2. Run the main script:
    ```sh
    python main.py --base-path path/to/your/locales
    ```

### Running the Executable on Windows

1. Configure the `settings.toml` file in the root directory with your project settings as shown above.

2. Run the executable:
    ```sh
    i18n_buddy.exe
    ```
    To override the base path in the settings file, you can specify it as a command-line argument:
    ```sh
    i18n_buddy.exe --base-path path/to/your/locales
    ```
    

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/i18n_buddy.git
    cd i18n_buddy
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Convert the program to an executable using `py2exe`:
    ```sh
    python setup.py py2exe
    ```



## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
