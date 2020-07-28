#import sys

class CHS(ICHS):

    def __init__(self):
        pass

    #---
    @staticmethod
    def getAdHocChartDatumCorr( WLZAmplitudeStrId,
                                PointDataDict,
                                CDCorrFactor= ITidalPrd.ADHOC_CHARTDATUM_CORR_FACTOR) :
        """
        Apply an ad-hoc chart datum correction computed
        from the water levels tidal constituents amplitudes.

        NOTE: This ad-hoc chart datum correction is temporary and is
        supposed to be eventually replaced by a more accurate and
        rigourous procedure.

        WLZAmplitudeStrId : The string key id. to index the WL tidal
        amplitudes in PointDataDict

        PointDataDict : A data dictionary holding a WebTide grid
        point input data.

        CDCorrFactor <OPTIONAL,
                      default== ITidalPrd.ADHOC_CHARTDATUM_CORR_FACTOR>:
        A correction factor to apply to the computed ad-hoc CD.
        """

        #methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

        #--- No fool-proof checks here for performance reasons:
        #    Assuming that WLZAmplitudeStrId string identificators
        #    are present in the dictionary keys of PointDataDict

        rgx= re.compile(".*"+WLZAmplitudeStrId[0])
        wlzDataIdsTuple= tuple( filter(rgx.match, PointDataDict.keys()) )

        wlzAmpsAcc= 0.0

        for wlzAmpId in wlzDataIdsTuple :
            wlzAmpsAcc += float(PointDataDict[wlzAmpId])
        #---

        #--- NOTE: PointDataDict[ ICHS.CHART_DATUM_CONV_ID[0] ]
        #    is an unary tuple.
        PointDataDict[ ICHS.CHART_DATUM_CONV_ID[0] ]= \
            ( CDCorrFactor[0] * wlzAmpsAcc ,)
