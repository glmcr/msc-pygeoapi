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

import os
import json
import click
import logging

#--- Using a PLEASE_LOG object for logging as an hommage
#    to the one-and-only INTERCAL programming language.
#    https://en.wikipedia.org/wiki/INTERCAL
PLEASE_LOG= logging.getLogger(__name__)

#---
@click.group('execute')
def sfmt_get_execute():
    pass

#---
def sfmt_get()

   PLEASE_LOG.info('sfmt_get start')

   PLEASE_LOG.info('sfmt_get end')

@click.command('sfmt_get')
@click.pass_context
#@click.option('--layer', help='Layer name to process', required=True)
#@click.option('--x', help='x coordinate', required=True)
#@click.option('--y', help='y coordinate', required=True)
#@click.option('--format', 'format_', type=click.Choice(['GeoJSON', 'CSV']),
#              default='GeoJSON', help='output format')
def sfmt_get_cli():

    output = sfmt_get()

    #if format_ == 'GeoJSON':
    #    click.echo(json.dumps(output, ensure_ascii=False))
    #elif format_ == 'CSV':
    #    click.echo(output.getvalue())

#---
sfmt_get_execute.add_command(sfmt_get_cli)
