from icecream import ic
from copy import deepcopy as dc
from glob import glob
import nbformat
import json
import os
import argparse
import subprocess
import logging

import papermill as pm

from ot2rec_report.templates import *
from ot2rec_report import utils


logging.basicConfig(level=logging.INFO)


def write_nb(nb_data, nb_path):
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f)


def main():
    lookup_dict = {
        "motioncor2": nb_mc,
        "ctffind": nb_ctffind,
        "ctfsim": nb_ctfsim,
        "exclude_bad_tilts": nb_ebt,
        "imod_header": nb_imod_header,
        "imod_align": nb_imod_align,
        "imod_recon": nb_imod_recon,
        "aretomo_header": nb_aretomo_header,
        "aretomo_align": nb_aretomo_align,
        "aretomo_recon": nb_aretomo_recon,
        "savu_recon": nb_savu_recon,
        "rlf_deconv": nb_rlf_deconv,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name",
                        help="Rootname of project",)
    parser.add_argument("--to_html",
                      help="Export report to html",
                      action="store_true")
    parser.add_argument("--to_slides",
                      help="Export report as Jupyter Slides",
                      action="store_true")

    args = parser.parse_args()

    final_nb = dc(nb_main)
    node_list = utils.get_processes(PROCESSES)

    # Check if AreTomo has been used
    at_list = list(i for i, s in enumerate(node_list) if "aretomo" in s)
    at_used = len(at_list) > 0
    if at_used:
        at_first_idx = at_list[0]

    # Add workflow diagram
    final_nb["cells"] = final_nb["cells"] + nb_workflow_diagram["cells"]
    logging.info(f"Added workflow diagram")

    # Add in cells to final notebook
    for idx, curr_proc in enumerate(node_list):
        if curr_proc == "imod_align":
            final_nb["cells"] = final_nb["cells"] + lookup_dict["imod_header"]["cells"]
        elif at_used and idx==at_first_idx:
            final_nb["cells"] = final_nb["cells"] + lookup_dict["aretomo_header"]["cells"]
        final_nb["cells"] = final_nb["cells"] + lookup_dict[curr_proc]["cells"]
        logging.info(f"Added {curr_proc}.")

    # Write out template notebook
    write_nb(final_nb, "./report_temp.ipynb")

    # Use papermill to populate empty notebook
    params = dict(
        proj_name = args.proj_name,
    )

    pm.execute_notebook(
        "./report_temp.ipynb",
        "./report.ipynb",
        parameters=params,
    )

    logging.info("Report notebook created.")

    # Export HTML
    if args.to_html:
        cmd = [
            "jupyter-nbconvert",
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
    
    # Export slides
    if args.to_slides:
        cmd = [
            "jupyter-nbconvert",
            "./report.ipynb",
            "--to", "slides",
            "--TemplateExporter.exclude_input=True",
            "--SlidesExporter.reveal_theme=simple",
            "--SlidesExporter.reveal_scroll=True"
        ]

        exp = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ascii",
            check=True
        )

        try:
            assert(not exp.stderr)
        except:
            print(exp.stderr)
