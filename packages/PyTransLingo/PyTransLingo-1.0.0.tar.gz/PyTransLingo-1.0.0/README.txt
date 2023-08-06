# PyTransLingo

PyTransLingo is a Python package that provides translation and search functionality using various APIs. It allows you to translate text between different languages and search for information on Google.

## Installation

To install PyTransLingo, use pip:


## Dependencies

PyTransLingo requires the following dependencies:

- pyttsx3
- translate
- PyDictionary
- requests
- bs4
- tabulate

You can install these dependencies using pip:


## Usage

Import the necessary modules:

```python
import pyttsx3
from translate import Translator
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

#translator_menu
Use the translator_menu function to interact with the translation and search functionalities:

translator_menu()

#Examples
Here are a few examples of how to use PyTransLingo:

1.Translating text:

source_lang = 'en'
target_lang = 'fr'
text = 'Hello, how are you?'
translate_and_speak(source_lang, target_lang, text)


2.Searching on Google:

search_text = 'Python programming'
search_google(search_text)

Contributing
Contributions to PyTransLingo are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on GitHub.