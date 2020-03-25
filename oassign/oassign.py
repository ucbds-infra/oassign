"""Convert a Jupyter notebook to OK format for release."""

import argparse
import json
import pathlib
from otter.grade import grade_notebook
from glob import glob
import sys
import os

try:
    from .to_ok import gen_views
except ImportError:
    from to_ok import gen_views

def blockPrint():
	"""
	Disables printing to stdout.
	"""
	sys.stdout = open(os.devnull, 'w')

def enablePrint():
	"""
	Enables printing to stdout.
	"""
	sys.stdout = sys.__stdout__

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("master", help="Notebook with solutions and tests.")
    parser.add_argument("result", help="Directory containing the result.")
    # parser.add_argument("endpoint", help="OK endpoint; e.g., cal/data8/sp19")
    parser.add_argument("--no-export-cell", help="Don't inject an export cell into the notebook",
                        default=False, action="store_true")
    parser.add_argument("--no-run-tests", help="Don't run tests.",
                        default=False, action="store_true")
    parser.add_argument("--no-init-cell", help="Don't automatically generate an Otter init cell",
                        default=False, action="store_true")
    parser.add_argument("--no-filter", help="Don't filter the PDF.",
                        default=False, action="store_true")
    parser.add_argument("--instructions", help="Additional submission instructions for students")
    parser.add_argument("files", nargs='*', help="Other support files needed for distribution (e.g. .py files, data files)")
    return parser.parse_args()


def run_tests(nb_path):
    """Run tests in the autograder version of the notebook."""
    results = grade_notebook(nb_path, glob(str(nb_path.parent / "tests" / "*.py")))
    assert results["total"] == results["possible"], "Some autograder tests failed"


def main():
    args = parse_args()
    master, result = pathlib.Path(args.master), pathlib.Path(args.result)
    print("Generating views...")
    gen_views(master, result, args)
    if not args.no_run_tests:
        print("Running tests...")
        blockPrint()
        run_tests(result / 'autograder'  / master.name )
        enablePrint()
        print("All tests passed!")

if __name__ == "__main__":
    main()
