# BibParser, More Than A Parser

#### Aug 13th, 2021, Jyonn at Hong Kong

[BibParser]() is a tool to parse, format, merge and export bibtex file.

```python


bib_parser = BibParser(
    conflict_shortname=Conflict.compare,
    conflict_shortname_compare='title',
    # strict_entry_required=True,
)
f1 = BibFile('../recbert-wsdm.bib', parser=bib_parser)
f2 = BibFile('../recbert.bib', parser=bib_parser)

file = BibFile.merge(
    'final.bib',
    f1, f2,
    conflict_shortname=Conflict.compare,
    conflict_shortname_compare='title'
)

file.export(
    'a.bib',
    select_attr=['title', 'author', 'year', 'booktitle', 'journal']
)

```