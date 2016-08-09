#!/usr/bin/env python

#   Copyright 2016 Scott Bezek
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import division
from __future__ import print_function

import logging
import os
import sys

from colored_stl_exporter import ColoredStlExporter

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(repo_root)

from util import rev_info


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    folder = os.path.dirname(__file__)

    openscad_variables = {
        'render_3d': True,
        'render_enclosure': 2,
        'render_flaps': True,
        'render_units': 1,
        'render_pcb': True,
        'render_revision': rev_info.git_short_rev(),
        'render_date': rev_info.current_date(),
    }

    exporter = ColoredStlExporter(
        os.path.join(folder, 'splitflap.scad'),
        os.path.join(folder, 'build'),
        openscad_variables)
    exporter.run()
