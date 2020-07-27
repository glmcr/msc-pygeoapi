# =================================================================
#
# Author: Gilles Mercier
#         <gilles.mercier@dfo-mpo.gc.ca> <gilles.mercier2@canada.ca>
#
# Copyright (c) 2020 Gilles Mercier
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import click


#---
from msc_pygeoapi.process.dfo.chs.enav.dhp import (
    dhp_get_execute
)

#from msc_pygeoapi.process.dfo.chs.enav.dhp import (
#    chs_enav_dhp
#)


@click.group()
def dfo_chs_enav():
    pass

dfo_chs_enav.add_command(dhp_get_execute)

#@click.group()
#def dfo():
#    pass


# NOTE: dfo is a msc_pygeoapi.process object.
#dfo.add_command(chs_enav_dhp)
