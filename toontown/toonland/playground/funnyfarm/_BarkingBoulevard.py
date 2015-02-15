########################## THE TOON LAND PROJECT ##########################
# Filename: _BarkingBoulevard.py
# Created by: Cody/Fd Green Cat Fd (February 19th, 2013)
####
# Description:
#
# The Barking Boulevard added Python implementation.
####

filepath = __filebase__ + '/toonland/playground/funnyfarm/maps/%s'
sidewalkTexture = loader.loadTexture(filepath % 'sidewalkyellow.jpg')
for tunnelNode in render.findAllMatches('**/linktunnel*'):
    tunnelNode.find('**/tunnel_floor*').setTexture(sidewalkTexture, 1)

toonHq = render.find('**/tb42:toon_landmark_hqFF_DNARoot')
for doorFrameHole in toonHq.findAllMatches('**/doorFrameHole*'):
    doorFrameHole.hide()