from setuptools import setup, find_packages

setup(
    name = 'boombig',
    version = '0.1',
    author='Mohammad and Amir',
    author_email = 'mohammadmehrabi175@gmail.com',
    description = 'boombing a Library Python',
    keywords = ['bot' , 'sms' , 'boombers' , 'boomber'],
    long_description = open("README.md", encoding="utf-8").read(),
    python_requires="~=3.6",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/OnlyRad/Boombers',
    packages = find_packages(),
    install_requires = [],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ]
)
