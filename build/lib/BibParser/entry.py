from typing import List, Union, Tuple


class Entry:
    def __init__(self, name: str, required=None, optional=None):
        self.name = name.lower()
        self.required = required or []  # type: List[Union[str, Tuple[str]]]
        self.optional = optional or []  # type: List[Union[str, Tuple[str]]]

        self.required = self.lower(self.required)
        self.optional = self.lower(self.optional)

    @staticmethod
    def lower(attrs: List[Union[str, Tuple[str]]]):
        return [item.lower() if isinstance(item, str) else (x.lower() for x in item) for item in attrs]

    def detect_attr(self, ref: 'Ref', strict_entry_optional=False):
        required = set(self.required)
        optional = set(self.optional)

        for key in ref.attrs:
            key = key.lower()

            found = 0
            element = None
            for index, attrs in enumerate([required, optional]):
                for a in attrs:
                    if isinstance(a, str):
                        if key == a:
                            found = index + 1
                            element = a
                            break
                    else:
                        for b in a:
                            if key == b:
                                found = index + 1
                                element = a
                                break
                if found:
                    break

            if found == 1:
                required.remove(element)
            elif found == 2:
                optional.remove(element)
            elif strict_entry_optional:
                raise ValueError('Undefined attribute %s in Ref %s' % (key, ref.shortname))

        if required:
            raise ValueError('Required attribute %s in Ref %s' % (list(required)[0], ref.shortname))

    def clone(self, name):
        return Entry(
            name=name,
            required=self.required,
            optional=self.optional,
        )




article = Entry(
    name='article',
    required=['author', 'title', 'journal', 'year', 'volume'],
    optional=['number', 'pages', 'month', 'doi', 'note', 'key'],
)

book = Entry(
    name='book',
    required=[('author', 'editor'), 'title', 'publisher', 'year'],
    optional=[('volume', 'number'), 'series', 'address', 'edition', 'month', 'note', 'key', 'url']
)

booklet = Entry(
    name='booklet',
    required=['title'],
    optional=['author', 'howpublished', 'address', 'month', 'year', 'note', 'key'],
)

conference = Entry(
    name='conference',
    required=['author', 'title', 'booktitle', 'year'],
    optional=['editor', ('volume', 'number'), 'series', 'pages', 'address', 'month', 'organization', 'publisher',
              'note', 'key'],
)

inbook = Entry(
    name='inbook',
    required=[('author', 'editor'), 'title', ('chapter', 'pages'), 'publisher', 'year'],
    optional=[('volume', 'number'), 'series', 'type', 'address', 'edition', 'month', 'note', 'key'],
)

incollection = Entry(
    name='incollection',
    required=['author', 'title', 'booktitle', 'publisher', 'year'],
    optional=['editor', ('volume', 'number'), 'series', 'type', 'chapter', 'pages', 'address', 'edition', 'month',
              'note', 'key'],
)

inproceedings = conference.clone('inproceedings')

manual = Entry(
    name='manual',
    required=['title'],
    optional=['author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'key'],
)

mastersthesis = Entry(
    name='mastersthesis',
    required=['author', 'title', 'school', 'year'],
    optional=['type', 'address', 'month', 'note', 'key'],
)

misc = Entry(
    name='misc',
    required=[],
    optional=['author', 'title', 'howpublished', 'month', 'year', 'note', 'key'],
)

phdthesis = Entry(
    name='phdthesis',
    required=['author', 'title', 'school', 'year'],
    optional=['type', 'address', 'month', 'note', 'key'],
)

proceedings = Entry(
    name='proceedings',
    required=['title', 'year'],
    optional=['editor', ('volume', 'number'), 'series', 'address', 'month', 'publisher', 'organization', 'note', 'key'],
)

techreport = Entry(
    name='techreport',
    required=['author', 'title', 'institution', 'year'],
    optional=['type', 'number', 'address', 'month', 'note', 'key'],
)

unpublished = Entry(
    name='unpublished',
    required=['author', 'title', 'note'],
    optional=['month', 'year', 'key'],
)


class Entries:
    def __init__(self, entries: List[Entry] = None):
        self.entries = dict()

        if entries:
            for entry in entries:
                self.add(entry)

    def add(self, entry: Entry):
        if entry.name in self.entries:
            raise ValueError('Already has "%s" entry' % entry.name)
        self.entries[entry.name] = entry
        return self


default_entries = Entries(entries=[
    article,
    book,
    booklet,
    conference,
    inbook,
    incollection,
    inproceedings,
    manual,
    mastersthesis,
    misc,
    phdthesis,
    proceedings,
    techreport,
    unpublished,
])
