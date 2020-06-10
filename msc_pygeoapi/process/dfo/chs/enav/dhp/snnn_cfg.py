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

#---
ALLOWED_DHP_SNNN_SOURCES= ( "S104_IWLS", "S111_RIOPS" )

#---
PROCESS_METADATA = {

    'version': '0.1.0',
    'id': 'snnn-get',
    'title': 'on-demand DFO-CHS-ENAV-DHP data generation process',
    'description': 'on-demand DFO-CHS-ENAV-DHP data generation process',
    'keywords': ['on-demand DFO-CHS-ENAV-DHP'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'URL to come',
        'hreflang': 'en-CA'
    }, {
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'URL a venir',
        'hreflang': 'fr-CA'
    }],
    'inputs': [{
        'id': 'snnn_source',
        'title': 's<nnn>_<source> dhp data id.',
        'input': {
            'literalDataDomain': {
                'dataType': 'string',
                'valueDefinition': {
                    'anyValue': True
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1
    }, {
        'id': 'bbox_swc_lat',
        'title': 'Bounding Box SW corner latitude(EPSG:4326)',
        'input': {
            'literalDataDomain': {
                'dataType': 'float',
                'valueDefinition': {
                    'anyValue': True
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1
    }, {
        'id': 'bbox_swc_Lon',
        'title': 'Bounding Box SW corner longitude(EPSG:4326)',
        'input': {
            'literalDataDomain': {
                'dataType': 'float',
                'valueDefinition': {
                    'anyValue': True
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1
    }, {
        'id': 'bbox_nec_lat',
        'title': 'Bounding Box NE corner latitude(EPSG:4326)',
        'input': {
            'literalDataDomain': {
                'dataType': 'float',
                'valueDefinition': {
                    'anyValue': True
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1
    }, {
        'id': 'bbox_nec_lon',
        'title': 'Bounding Box NE corner longitude(EPSG:4326)',
        'input': {
            'literalDataDomain': {
                'dataType': 'float',
                'valueDefinition': {
                    'anyValue': True
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1
    }],
    'outputs': [{
        'id': 'sfmt-get-response',
        'title': 'output sfmt get',
        'output': {
            'formats': [{
                'mimeType': 'application/x-hdf5'
            }]
        }
    }]
}
