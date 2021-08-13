import argparse

from .bib import BibFile
from .common import boolize
from .parser import BibParser


ACTIONS = ['analyse', 'merge']


parser = argparse.ArgumentParser()
parser.add_argument('--conflict_shortname', '-n', type=str, default='ignore')
parser.add_argument('--conflict_shortname_compare', '-c', type=str, default=None)
parser.add_argument('--allow_entry_detect', '-d', type=boolize, default=False)
parser.add_argument('--strict_entry_required', '-r', type=boolize, default=False)
parser.add_argument('--strict_entry_optional', '-o', type=boolize, default=False)
parser.add_argument('--file', '-f', required=True, nargs='+')
parser.add_argument('--action', '-a', type=str, default='analyse')
parser.add_argument('--export', '-e', type=str, default=None)
parser.add_argument('--merge_conflict_shortname', '-mn', type=str, default='ignore')
parser.add_argument('--merge_conflict_shortname_compare', '-mc', type=str, default=None)
parser.add_argument('--selected_attrs', '-t', nargs='*', default=None)


def analyse():
    args = parser.parse_args()
    bib_parser = BibParser.from_args(args)

    for file in args.file:
        bib_file = BibFile(file, parser=bib_parser)
        print('Total', len(bib_file.refs.refs), 'references in', file)


def merge():
    args = parser.parse_args()
    bib_parser = BibParser.from_args(args)

    assert args.export
    bib_files = [BibFile(file, parser=bib_parser) for file in args.file]
    bib_file = BibFile.merge(
        *bib_files,
        conflict_shortname=args.merge_conflict_shortname,
        conflict_shortname_compare=args.merge_conflict_shortname_compare,
    )
    selected_attrs = args.selected_attrs
    bib_file.export(
        to=args.export,
        selected_attrs=selected_attrs,
    )

    print('Successfully merged to', args.export)


def main():
    args = parser.parse_args()

    assert args.action in ACTIONS

    if args.action == 'analyse':
        analyse()

    elif args.action == 'merge':
        merge()

    else:
        raise ValueError('Undefined action', args.action)
