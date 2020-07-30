#--- Algo to get the CHS S102 bathymetry tiles that are
#    inside or that intersect a regukar bounding box
#    provided by a client asynchronous request.
#
#    Using tiles index files(at different levels) in GeoJSON
#    format.
#
#    Beginning at L2(1x1 or 1x2 degrees)
#
#    bounding box box provided by a client request is regular.
#
#    SWCLat == SECLat
#    NWCLat == NECLat
#    SWCLon == NWCLon
#    NECLon == SECLon
#
#    SWCTileLat and SECTileLat -> int(floor(SWCLat))
#    SWCTileLon and NWCTileLon -> int(floot(SWCLon))
#    NWCTileLat and NECTileLat -> int(ceil(NECLat))
#    SECTileLon and NECTileLon -> int(ceil(SECLon))
#
#    Iterate on lon,lat limits to extract the L2 bathy
#    tiles from the geojson index but beware that we
#    can have locations where tiles are not existing
#    (ex. on land or outside canadian coastal waters)
