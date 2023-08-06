from setuptools import setup, find_packages

setup(
    name='PyTransLingo',
    version='1.0.0',
    author='Hari Prasath .S',
    author_email='harishreehp80@gmail.com',
    license='MIT',
    description='PyTransLingo is a command-line tool that provides translation and text-to-speech functionalities. It allows users to translate text between different languages using the Google Translate API. PyTransLingo also provides the ability to fetch the meaning of translated text using the PyDictionary library. Additionally, users can perform Google searches directly from the command line and listen to the search results using text-to-speech. Explore the world of languages with PyTransLingo!',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'PyTransLingo = PyTransLingo.translator_menu:translator_menu',
        ],
    },
    install_requires=[
        'pyttsx3',
        'translate',
        'PyDictionary',
        'requests',
        'beautifulsoup4',
        'tabulate',
    ],

)