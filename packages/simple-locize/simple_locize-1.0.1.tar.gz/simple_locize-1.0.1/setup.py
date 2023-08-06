from setuptools import setup
from pathlib import Path

setup(
    name = 'simple_locize',
    version = '1.0.1',
    license = 'MIT',
    url = 'https://github.com/Maxoplata/simple-locize-py',
    description = 'A lightweight library for handling translations via the Locize API',
    author = 'Maxamilian Demian',
    author_email = 'max@maxdemian.com',
    long_description = Path('README.md').read_text(),
    long_description_content_type = 'text/markdown',
    install_requires = [],
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ]
)
