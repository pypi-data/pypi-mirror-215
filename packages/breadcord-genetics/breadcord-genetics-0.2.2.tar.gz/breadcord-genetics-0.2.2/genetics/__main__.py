from genetics.api import genPatches, genSources, applyPatches
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("action", help="Action to perform", choices=["genPatches", "genSources", "applyPatches"])

args = parser.parse_args()

if args.action == "genPatches":
    genPatches()
elif args.action == "genSources":
    genSources()
elif args.action == "applyPatches":
    applyPatches()
else:
    parser.print_help()