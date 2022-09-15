import pkg_resources
import json
from glob import glob

import RepoTemp.templates

PROCESSES = ["1", "2"]

def read_ipynb(filename):
    fn = pkg_resources.resource_filename("RepoTemp.templates", filename)

    with open(fn, 'r') as f:
        return json.load(f)


nb_master = read_ipynb("./report_master.ipynb")
nb_1 = read_ipynb("./report_1.ipynb")
nb_2 = read_ipynb("./report_2.ipynb")
nb_workflow_diagram = read_ipynb("./workflow_diagram.ipynb")
