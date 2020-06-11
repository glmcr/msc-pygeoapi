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

# import os
# import json
import click
import logging

from msc_pygeoapi.process.dfo.chs.enav.dhp.snnn_chk import snnn_chk_bbox
from msc_pygeoapi.process.dfo.chs.enav.dhp.snnn_cfg import DHP_SNNN_SOURCES
#                                                        PROCESS_METADATA )

LOGGER = logging.getLogger(__name__)


def snnn_get(snnn_source,
             bbox_swc_lat,
             bbox_swc_lon,
             bbox_nec_lat,
             bbox_nec_lon):

    # LOGGER.debug('sfmt_get start')

    # Check if the snnn_source combo exists.
    try:
        snnn_get_func = DHP_SNNN_SOURCES[snnn_source]

    except IndexError as err:

        msg = 'invalid snnn_source value: {}'.format(err)
        LOGGER.exception(msg)

    # click.echo("snnn_get_func="+snnn_get_func)

    # LOGGER.debug('sfmt_get end')

    return snnn_chk_bbox((bbox_swc_lat,
                          bbox_swc_lon,
                          bbox_nec_lat,
                          bbox_nec_lon))


@click.group('execute')
def snnn_get_execute():
    pass


@click.command('snnn-get')
@click.pass_context
@click.option('--snnn_source',
              help='snnn_source(ex. S104_IWLS) dhp type name id. to process',
              required=True)
@click.option('--bbox_swc_lat',
              help='Bounding Box SW corner latitude(EPSG:4326)',
              required=True)
@click.option('--bbox_swc_lon',
              help='Bounding Box SW corner longitude(EPSG:4326)',
              required=True)
@click.option('--bbox_nec_lat',
              help='Bounding Box NE corner latitude(EPSG:4326)',
              required=True)
@click.option('--bbox_nec_lon',
              help='Bounding Box NE corner longitude(EPSG:4326)',
              required=True)
def snnn_get_cli(objectNotUsedForNow,
                 snnn_source,
                 bbox_swc_lat,
                 bbox_swc_lon,
                 bbox_nec_lat,
                 bbox_nec_lon):

    output = snnn_get(snnn_source,
                      bbox_swc_lat,
                      bbox_swc_lon,
                      bbox_nec_lat,
                      bbox_nec_lon)

    # LOGGER.debug('output='+str(output))

    click.echo(str(output))

    # if format_ == 'GeoJSON':
    #    click.echo(json.dumps(output, ensure_ascii=False))
    # elif format_ == 'CSV':
    #    click.echo(output.getvalue())


#
snnn_get_execute.add_command(snnn_get_cli)
