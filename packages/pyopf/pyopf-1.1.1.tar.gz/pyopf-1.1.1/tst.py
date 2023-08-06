from pprint import pprint

import numpy as np
from pathlib import Path

import pyopf
from pyopf.io import load
from pyopf.resolve import resolve
from pyopf.uid64 import Uid64
from pyopf.versions import format_and_version_to_type


pprint(format_and_version_to_type)

project_path = "/home/pgafton/data/16_project_planes/opf/project.opf"

# Load the json data and resolve the project, i.e. load the project items as named attributes.
project = load(project_path)

print()
print()
pprint(project)
print()
print()
pprint(project)
print()
print()
pprint(project.items)
print()
print()
pprint([it.type.name for it in project.items])
print()
print()

project = resolve(project, supported_extensions=['ext_pix4d_planes'])

pprint(project)
print()
print()
