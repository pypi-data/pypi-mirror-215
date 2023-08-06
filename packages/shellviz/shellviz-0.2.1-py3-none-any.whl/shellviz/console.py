#!/usr/bin/env python

# Usage: sv [options] data
# Data can be piped in or passed as an argument.
# e.g. sv [options] '[1, 2, 3]'
# e.g. sv [options] < data.json
# options:
#  -h, --help            show this help message and exit
#  -i ID, --id=ID        ID of the visualization to update
#  -d, --domain          The domain of a self-hosted shellviz server. Defaults to https://shellviz.com
#  -k, --key             The API key for the shellviz server. Not required if using the free tier
#  -I, --instance        The id of an existing instance to use. If not provided, a new instance will be created



import argparse
import sys
from . import Shellviz


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Process data for shellviz')
    parser.add_argument('-i', '--id', type=str, help='ID of the visualization to update')
    parser.add_argument('-d', '--domain', type=str, help='The domain of a self-hosted shellviz server. Defaults to https://shellviz.com')
    parser.add_argument('-k', '--key', type=str, help='The API key for the shellviz server. Not required if using the free tier')
    parser.add_argument('-I', '--instance', type=str, help='The id of an existing instance to use. If not provided, a new instance will be created')
    parser.add_argument('data', nargs='?', help='Data to process; may be passed from input redirection (e.g. shellviz < data.json), piped (e.g. cat data.son | shellviz) or passed as an argument (e.g. shellviz "[1, 2, 3]")')
    args = parser.parse_args(args)

    sv = Shellviz(domain=args.domain, key=args.key, id=args.instance)
    data = args.data or sys.stdin.read()
    result = sv.visualize(data, args.id)

if __name__ == "__main__":  # pragma: no cover
    main()