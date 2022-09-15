from icecream import ic
from copy import deepcopy as dc
from glob import glob
import nbformat
import json
import os
import argparse
import subprocess
import logging

from RepoTemp.templates import *
from RepoTemp import utils


logging.basicConfig(level=logging.INFO)


def write_nb(nb_data, nb_path):
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f)


def main():
    lookup_dict = {
        "1": nb_1,
        "2": nb_2,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--to_html",
                      help="Export report to html",
                      action="store_true")

    args = parser.parse_args()

    final_nb = dc(nb_master)
    node_list = utils.get_processes(PROCESSES)

    # Add workflow diagram
    final_nb["cells"] = final_nb["cells"] + nb_workflow_diagram["cells"]

    # Add in cells to final notebook
    for curr_proc in node_list:
        final_nb["cells"] = final_nb["cells"] + lookup_dict[curr_proc]["cells"]


    # Write out final notebook
    write_nb(final_nb, "./report.ipynb")
    logging.info("Report notebook created.")


    # Export HTML
    if args.to_html:
        cmd = [
            "jupyter", "nbconvert",
            "--execute",
            "--to", "html",
            "--TemplateExporter.exclude_input=True",
            "./report.ipynb"]

        exp = subprocess.run(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             encoding="ascii",
                             check=True)

        try:
            assert(not exp.stderr)
        except:
            print(exp.stderr)
