from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

VERSION = '0.0.7'
DESCRIPTION = 'A python package to clone yourself with GPT'
LONG_DESCRIPTION = 'A python package to clone yourself with GPT'

# Setting up
setup(
    name="gptdjmme",
    version=VERSION,
    author="Daniel J. McDonald",
    author_email="<daniel@danielmcdonald.dev>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai', 'python-dotenv'],
    keywords=['python', 'gpt', 'openai', 'ai', 'chatbot', 'clone', 'me'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

