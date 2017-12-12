"""
relativizer
"""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"

import json
from pathlib import Path
from argparse import ArgumentParser
from os import scandir

def rscandir(path):
    for entry in scandir(path):
        yield Path(entry.path)
        if entry.is_dir():
            yield from rscandir(entry.path)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'paths',
        type=str, nargs="+", help="The absolute paths to consider relative roots"
    )
    args = parser.parse_args()

    listings = {x: set() for x in args.paths}
    relative_listings = {x: set() for x in args.paths}

    print("Gathering abspaths...")
    for abspath in listings:
        for node in rscandir(abspath):
            listings[abspath].add(node)

    print("Relativizing paths...")
    for abspath in listings:
        for nodepath in listings[abspath]:
            relative_listings[abspath].add(Path(nodepath).relative_to(abspath))

    print("Crunching the numbers...")
    all_rels = {}
    for abspath in relative_listings:
        for nodepath in relative_listings[abspath]:
            if all_rels.get(str(nodepath)) is None:
                all_rels[str(nodepath)] = set()
            all_rels[str(nodepath)].add(abspath)
    rel_collisions = {x: all_rels[x] for x in all_rels if len(all_rels[x]) > 1}

    print("Generating Reports...")
    jsonable_listings = {}
    for abspath in listings:
        jsonable_listings[abspath] = [str(x) for x in listings[abspath]]
    jsonable_relative_listings = {}
    for abspath in relative_listings:
        jsonable_relative_listings[abspath] = [str(x) for x in relative_listings[abspath]]
    jsonable_all_rels = {}
    for relpath in all_rels:
        jsonable_all_rels[relpath] = [x for x in all_rels[relpath]]
    jsonable_rel_collisions = {}
    for relpath in rel_collisions:
        jsonable_rel_collisions[relpath] = [x for x in rel_collisions[relpath]]

    print("Writing Reports...")
    with open('listings.json', 'w') as f:
        json.dump(jsonable_listings, f, indent=2)
    with open('relative_listings.json', 'w') as f:
        json.dump(jsonable_relative_listings, f, indent=2)
    with open('all_rels.json', 'w') as f:
        json.dump(jsonable_all_rels, f, indent=2)
    with open('rel_collisions.json', 'w') as f:
        json.dump(jsonable_rel_collisions, f, indent=2)
    print("Done. Collisions: {}".format(
            str(len(rel_collisions))
        )
    )
    report_names = [
        "listings.json",
        "relative_listings.json",
        "all_rels.json",
        "rel_collisions.json"
    ]
    print(
        "Reports in...\n{}".format(
            "\n".join(
                [x for x in report_names]
            )
        )
    )

if __name__ == '__main__':
    main()
