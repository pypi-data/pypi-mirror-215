from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

VERSION = '0.1.0'
DESCRIPTION = 'A python package to clone yourself with the help of GPT'
LONG_DESCRIPTION = 'A python package to clone yourself with the help of GPT'

# Setting up
setup(
    name="me_gpt",
    version=VERSION,
    author="Daniel J. McDonald",
    author_email="<daniel@danielmcdonald.dev>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai', 'python-dotenv', 'numpy'],
    keywords=['python', 'gpt', 'openai', 'ai', 'chatbot', 'clone'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

