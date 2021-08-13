from setuptools import setup, find_packages

setup(
    name='BibParser',
    version='0.0.1',
    keywords=('bib', 'bibtex', 'parser', 'latex', 'reference'),
    description='BibParser, More Than A Parser',
    long_description='[BibParser](https://github.com/Jyonn/BibParser) is a tool to parse, format, merge and export bibtex file.',
    license='MIT Licence',
    url='https://github.com/Jyonn/BibParser',
    author='Jyonn Liu',
    author_email='i@6-79.cn',
    platforms='any',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bibparser = BibParser.command:main',
            'bibanalyser = BibParser.command:analyse',
            'bibmerger = BibParser.command:export',
        ]
    }
)
