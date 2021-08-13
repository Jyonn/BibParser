from typing import List, Optional

from .common import Conflict
from .parser import BibParser
from .reference import Ref, Refs


class BibFile:
    def __init__(self, filename=None, parser: BibParser = None):
        self.filename = filename  # type: Optional[List[str], str]
        self.parser = parser
        self.refs = Refs()

        if self.filename:
            self._parse()

    def _parse(
            self,
    ):
        assert self.filename

        with open(self.filename, 'r') as f:
            bib_stream = f.read()

        # analyse refs
        while True:
            ref, bib_stream = Ref.load(bib_stream)
            if not ref:
                break
            self.refs.add(
                ref,
                conflict_shortname=self.parser.conflict_shortname,
                conflict_shortname_compare=self.parser.conflict_shortname_compare,
            )

        # entries detect
        if self.parser.allow_entries:
            for key in self.refs.refs:
                ref = self.refs.refs[key]
                assert ref.entry in self.parser.allow_entries.entries, 'Undefined entry %s' % ref.entry

                if self.parser.strict_entry_required:
                    entry = self.parser.allow_entries.entries[ref.entry]
                    entry.detect_attr(ref, strict_entry_optional=self.parser.strict_entry_optional)

    def d(self, with_raw_ref=False):
        return dict(
            filename=self.filename,
            refs=self.refs.d(with_raw_ref=with_raw_ref)
        )

    @classmethod
    def merge(
            cls,
            *files: 'BibFile',
            conflict_shortname=Conflict.alert,  # ['ignore', 'alert', 'compare', 'replace']
            conflict_shortname_compare=None,  # type: Optional[str, List[str]]
    ):
        if conflict_shortname == Conflict.compare:
            assert conflict_shortname_compare

        file = cls(filename=None)
        for f in files:
            file.refs.update(
                f.refs,
                conflict_shortname=conflict_shortname,
                conflict_shortname_compare=conflict_shortname_compare,
            )

        return file

    def export(
            self,
            to: str,
            selected_attrs: List[str] = None,
    ):
        with open(to, 'w') as f:
            for key in self.refs.refs:
                ref = self.refs.refs[key]
                f.write('@%s{%s,\n' % (ref.entry, ref.shortname))
                for attr_key in ref.attrs:
                    if selected_attrs and attr_key not in selected_attrs:
                        continue
                    attr = ref.attrs[attr_key]
                    quote = attr.quote
                    f.write('\t%s = %s%s%s\n' % (attr.key, quote.start if quote else '', attr.value, quote.end if quote else ''))
                f.write('}\n\n')
