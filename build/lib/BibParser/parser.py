from typing import Optional, List

from .common import Conflict
from .entry import Entries, default_entries


class BibParser:
    def __init__(
            self,
            conflict_shortname=Conflict.alert,  # ['ignore', 'alert', 'compare', 'replace']
            conflict_shortname_compare=None,  # type: Optional[str, List[str]]
            allow_entries='default',  # type: Optional[str, Entries]
            strict_entry_required=False,  # type: bool
            strict_entry_optional=False,  # type: bool
    ):
        self.conflict_shortname = conflict_shortname
        self.conflict_shortname_compare = conflict_shortname_compare

        if self.conflict_shortname == Conflict.compare:
            assert self.conflict_shortname_compare

        self.allow_entries = allow_entries
        if isinstance(allow_entries, str):
            assert allow_entries == 'default'
            self.allow_entries = default_entries

        self.strict_entry_required = strict_entry_required
        self.strict_entry_optional = strict_entry_optional

    @classmethod
    def from_args(cls, args):
        return cls(
            conflict_shortname=args.conflict_shortname,
            conflict_shortname_compare=args.conflict_shortname_compare,
            strict_entry_required=args.strict_entry_required,
            strict_entry_optional=args.strict_entry_optional,
            allow_entries='default' if args.allow_entry_detect else None,
        )
