import io
from collections import OrderedDict
from typing import Optional, Union, Dict, List

from .common import Status, Conflict, Quote


class Attr:
    def __init__(self):
        self.key = None  # type: Optional[str]
        self.value = None  # type: Optional[str]
        self.quote = None  # type: Optional[Quote]

    def __str__(self):
        return self.key

    def d(self):
        return dict(
            key=self.key,
            value=self.value,
            quote=str(self.quote),
        )


class Ref:
    def __init__(self):
        self.entry = None  # type: Optional[str]
        self.shortname = None  # type: Optional[str]
        self.attrs = OrderedDict()  # type: OrderedDict[str, Attr]
        self.raw = ''

    def d(self, with_raw_ref=False):
        d = dict(
            entry=self.entry,
            shortname=self.shortname,
            attrs=[self.attrs[key].d() for key in self.attrs],
        )
        if with_raw_ref:
            d['raw'] = self.raw
        return d

    def strip(self):
        self.entry = self.entry.strip()
        self.shortname = self.shortname.strip()

        for key in self.attrs:
            attr = self.attrs[key]
            attr.key = attr.key.strip()
            attr.value = attr.value.strip()
            if attr.quote:
                assert attr.value[0] == attr.quote.start
                assert attr.value[-1] == attr.quote.end
                attr.value = attr.value[1: -1]

    @classmethod
    def load(cls, bib_stream: Union[str, io.TextIOWrapper]):
        ref = cls()
        attr = None  # type: Optional[Attr]

        status = Status.free
        index = 0
        is_file_stream = isinstance(bib_stream, io.TextIOWrapper)
        quote_deep = 0

        while True:
            if is_file_stream:
                c = bib_stream.read(1)
                if c == '':
                    break
            else:
                if index < len(bib_stream):
                    c = bib_stream[index]
                    index += 1
                else:
                    break

            ref.raw += c

            if status == Status.free:
                if c == '@':
                    status = Status.entry
                    ref.entry = ''

            elif status == Status.entry:
                if c == '{':
                    status = Status.shortname
                    ref.shortname = ''
                else:
                    ref.entry += c

            elif status == Status.shortname:
                if c == ',':
                    status = Status.free_attr
                else:
                    ref.shortname += c

            elif status == Status.free_attr:
                if c == '}':
                    status = Status.end
                elif c.isalpha():
                    status = Status.attr_key
                    attr = Attr()
                    attr.key = c

            elif status == Status.attr_key:
                if c == '=':
                    status = Status.attr_value
                    attr.value = ''
                else:
                    attr.key += c

            elif status == Status.attr_value:
                if not attr.quote:
                    if c in Quote.starts:
                        attr.value += c
                        attr.quote = Quote(start=c)
                    elif c == ',' or c == '\n':
                        ref.attrs[attr.key.strip()] = attr
                        status = Status.free_attr
                    else:
                        attr.value += c
                else:
                    attr.value += c
                    if c == attr.quote.end:
                        if not quote_deep:
                            ref.attrs[attr.key.strip()] = attr
                            status = Status.free_attr
                        else:
                            quote_deep -= 1
                    elif c == attr.quote.start:
                        quote_deep += 1

            elif status == Status.end:
                break

        if ref.entry and ref.shortname:
            ref.strip()
        else:
            ref = None

        if is_file_stream:
            return ref, bib_stream
        return ref, bib_stream[index + 1:]


class Refs:
    def __init__(self):
        self.refs = dict()  # type: Dict[str, Ref]

    def update(
            self,
            refs: 'Refs',
            conflict_shortname=Conflict.alert,  # ['ignore', 'alert', 'compare', 'replace']
            conflict_shortname_compare=None,  # type: Optional[str, List[str]]
    ):
        for shortname in refs.refs:
            ref = refs.refs[shortname]
            self.add(
                ref,
                conflict_shortname=conflict_shortname,
                conflict_shortname_compare=conflict_shortname_compare,
            )

    def add(
            self,
            ref: Ref,
            conflict_shortname=Conflict.alert,  # ['ignore', 'alert', 'compare', 'replace']
            conflict_shortname_compare=None,  # type: Optional[str, List[str]]
    ):
        if ref.shortname in self.refs:
            if conflict_shortname == Conflict.ignore:
                return self
            if conflict_shortname == Conflict.alert:
                raise ValueError('Already has "%s" reference' % ref.shortname)
            if conflict_shortname == Conflict.compare:
                another = self.refs[ref.shortname]
                if isinstance(conflict_shortname_compare, str):
                    conflict_shortname_compare = [conflict_shortname_compare]
                for key in conflict_shortname_compare:
                    if key not in ref.attrs:
                        raise ValueError('Ref %s has no %s attribute' % (ref.shortname, key))
                    if key not in another.attrs:
                        raise ValueError('Ref %s has no %s attribute' % (another.shortname, key))
                    if ref.attrs[key].value.lower() != another.attrs[key].value.lower():
                        raise ValueError('Already has "%s" reference, with different %s' % (ref.shortname, key))
        self.refs[ref.shortname] = ref
        return self

    def d(self, with_raw_ref=False):
        return [self.refs[ref].d(with_raw_ref=with_raw_ref) for ref in self.refs]
