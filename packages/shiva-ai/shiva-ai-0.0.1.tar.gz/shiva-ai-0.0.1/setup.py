from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.00.01'
DESCRIPTION = 'Integrate AI into Python projects easily.'
LONG_DESCRIPTION = 'Easily integrate artificial intelligence into your Python projects with Shiva AI.'

# Setting up
setup(
    name="shiva-ai",
    version=VERSION,
    author="Bertran Usher (theaihub)",
    author_email="<bjusher820@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai'],
    keywords=['python', 'openai', 'ai', 'artificial intelligence'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)