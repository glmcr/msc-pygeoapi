#--- Algo to get the tiles that are inside or that intersect
#    a boundinfg box provided by a client request.
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
#    WIP
