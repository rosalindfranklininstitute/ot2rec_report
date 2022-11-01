import pkg_resources
import json
from glob import glob

import ot2rec_report.templates


PROCESSES = ["motioncor2", "ctffind", "ctfsim", "imod_align", "imod_recon", "aretomo", "savu_recon", "rlf_deconv"]

def read_ipynb(filename):
    fn = pkg_resources.resource_filename("ot2rec_report.templates", filename)

    with open(fn, 'r') as f:
        return json.load(f)


nb_main = read_ipynb("report_main.ipynb")
nb_mc = read_ipynb("report_mc.ipynb")
nb_ctffind = read_ipynb("report_ctffind.ipynb")
nb_ctfsim = read_ipynb("report_ctfsim.ipynb")
nb_imod_header = read_ipynb("report_imod_header.ipynb")
nb_imod_align = read_ipynb("report_imod_align.ipynb")
nb_imod_recon = read_ipynb("report_imod_recon.ipynb")
nb_aretomo = read_ipynb("report_aretomo.ipynb")
nb_savu_recon = read_ipynb("report_savu_recon.ipynb")
nb_rlf_deconv = read_ipynb("report_rlf_deconv.ipynb")
nb_workflow_diagram = read_ipynb("workflow_diagram.ipynb")
