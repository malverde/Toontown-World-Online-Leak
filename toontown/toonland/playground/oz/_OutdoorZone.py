########################## THE TOON LAND PROJECT ##########################
# Filename: _OutdoorZone.py
# Created by: Cody/Fd Green Cat Fd (February 20th, 2013)
####
# Description:
#
# The Outdoor Zone added Python implementation.
####

safe_zone = render.find('**/%d:safe_zone' % PlaygroundGlobals.OUTDOOR_ZONE)
filepath = '%s/toonland/playground/oz/maps' % __filebase__
tunnelAheadSign = loader.loadTexture('%s/tt_t_ara_gen_tunnelAheadSign.jpg' % filepath)
safe_zone.find('**/prop_tunnel_ahead_OZ_DNARoot').setTexture(tunnelAheadSign, 1)