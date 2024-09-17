#SPDX-License-Identifier: GPL-3.0-or-later
#Copyright (c) 2024, Lothar Felten <lothar.felten@gmail.com>
"""
dec_card 
DEC card edge footprint generator script for KiCad
Generates PCB card egdes for DEC (Digital Equipent Corporation)
card slots. Typically used for flip-chip modules or Qbus, Unibus or Omnibus cards.
DEC has a special pad naming scheme: 
The pads have letters, omitting G, I, O, Q.
The finger prefix is 'A' to 'C'.
The side postfix is '1' for the component top side, bottom side prefix is 2.
Early boards have no side prefix as both sides carry the same signal.
Supported finger types: single, double, quad
Supported height types: short, long
"""
import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

from KicadModTree import *

datasheet1 = "http://www.bitsavers.org/pdf/dec/handbooks/Digital_Logic_Handbook_1975-76.pdf page 10 (24)"
datasheet2 = "http://www.bitsavers.org/pdf/dec/pdp8/pdp8e/PDP-8E_Engineering_Drawings_Dec72.pdf page 70"
widthTypes = ['single', 'double', 'quad']
heightTypes = ['short', 'long']
padNames = ['V','U','T','S','R','P','N','M','L','K','J','H','F','E','D','C','B','A']
fingerNames = ['A','B','C','D']

#all dimensions in mil, 1 mil = 0.0254 mm
def mil(x):
    return x * 0.0254
    
padWidth = mil(80)
padHeight = mil(563)
padOffset = 0.5
padSize = [padWidth, padHeight]
padToPad = mil(125)
padPositions = [mil(156), mil(2906), mil(5406), mil(8156)]
pcbWidths = {'single':mil(2437), 'double':mil(5187), 'quad':mil(10457)}
pcbHeights = {'short':mil(4930), 'long':mil(8430)}
padText = mil(650)
fingerCount = {'single':1, 'double':2, 'quad':4}
chamferLength = 0.3
padRadiusRatio = 0.2
notchHeight = mil(625)
notchDeepHeight = mil(725)
notchDeepWidth = mil(140)
notchNarrowWidth = mil(258)
notchWideWidth = mil(510)
fingerPositions = [mil(100), mil(2850), mil(5348), mil(8097)]
fingerWidth = mil(2240)
cutWidth = 0.2
handleHoleOffsetX = mil(219)
handleHoleOffsetY = mil(-180) 
handleHolePositions = [mil(0), mil(2750), mil(5250), mil(8000)]
handleHoleDistance = mil(2000)
handleHoleDiameter = mil(128)
layers_top = ['F.Cu', 'F.Mask']
layers_bottom = ['B.Cu', 'B.Mask']

for heightType in heightTypes:
    height = pcbHeights.get(heightType)
    for widthType in widthTypes:
        width = pcbWidths.get(widthType)
        footprint_name = "DEC_" + str(widthType) + "_" + str(heightType)
        f = Footprint(footprint_name, FootprintType.SMD)
        f.setDescription(datasheet1 + ' ' + datasheet2)
        f.setTags("Connector PCBEdge "+footprint_name)
        
        fingers = fingerCount.get(widthType)
        for finger in range (0, fingers):
            # pads
            i=0
            for pad in padNames:
                y = -((padHeight/2) + padOffset)
                x = padPositions[finger] + (padToPad * i)
                f.append(Pad(number=fingerNames[fingers-1-finger]+padNames[i]+'1', type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                     at=[x, y], size=padSize, layers=layers_top, radius_ratio=padRadiusRatio))
                f.append(Pad(number=fingerNames[fingers-1-finger]+padNames[i]+'2', type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                     at=[x, y], size=padSize, layers=layers_bottom, radius_ratio=padRadiusRatio))
                #silkscreen
                f.append(Text(type="user", text=fingerNames[fingers-1-finger]+padNames[i]+'1', 
                    at=[x, -padText], rotation=90, layer="F.SilkS", size=[1,1], thickness=0.15))
                f.append(Text(type="user", text=fingerNames[fingers-1-finger]+padNames[i]+'2', 
                    at=[x, -padText], rotation=90, layer="B.SilkS", size=[1,1], thickness=0.15))
                i=i+1
            #edge cuts finger
            f.append(PolygonLine(polygon=[
                [fingerPositions[finger],-notchHeight],
                [fingerPositions[finger], 0],
                [fingerPositions[finger] + fingerWidth, 0],
                [fingerPositions[finger] + fingerWidth, -notchHeight]],
                layer="Edge.Cuts", width=cutWidth))
            # chamfer
            f.append(PolygonLine(polygon=[[fingerPositions[finger], -chamferLength],
                [fingerPositions[finger]+fingerWidth, -chamferLength]],
                layer="Dwgs.User", width=cutWidth))
            #holes for handles, 2 per finger
            f.append(Pad(number='H', type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                at=[handleHoleOffsetX+handleHolePositions[finger], -(height+handleHoleOffsetY)],
                size=handleHoleDiameter+mil(100), layers=Pad.LAYERS_THT, drill=handleHoleDiameter))
            f.append(Pad(number='H', type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                at=[handleHoleOffsetX+handleHolePositions[finger]+handleHoleDistance, -(height+handleHoleOffsetY)],
                size=handleHoleDiameter+mil(100), layers=Pad.LAYERS_THT, drill=handleHoleDiameter))

        #edge cut notches
        f.append(PolygonLine(polygon=[
            [0, -notchDeepHeight],
            [fingerPositions[0], -notchDeepHeight],
            [fingerPositions[0], -notchHeight]],
            layer="Edge.Cuts", width=cutWidth))
        for notch in range (0, fingers-1):
            # notches
            f.append(PolygonLine(polygon=[
                [fingerPositions[notch]+fingerWidth,-notchHeight],
                [fingerPositions[notch+1]-notchDeepWidth,-notchHeight],
                [fingerPositions[notch+1]-notchDeepWidth,-notchDeepHeight],
                [fingerPositions[notch+1],-notchDeepHeight],
                [fingerPositions[notch+1],-notchHeight]],
                layer="Edge.Cuts", width=cutWidth))
        f.append(PolygonLine(polygon=[
            [fingerPositions[fingers-1]+fingerWidth, -notchHeight],
            [width, -notchHeight],
            [width, -notchDeepHeight]],
            layer="Edge.Cuts", width=cutWidth))
        #edge cuts sides
        f.append(PolygonLine(polygon=[
            [0, -notchDeepHeight],
            [0 , -height],
            [width, -height],
            [width, -notchDeepHeight]],
            layer="Edge.Cuts", width=cutWidth))

        # courtyard
        f.append(RectLine(start=[0, 0],
            end=[width, -notchDeepHeight],
            layer="F.CrtYd", width=cutWidth))
        
        #text
        f.append(Text(type="user", text="Chamfer 30 degree 1 mm", at=[15, 2],
            layer="Cmts.User"))
        f.append(Text(type="user", text="PCB thickness 1.6 mm", at=[15, 4],
            layer="Cmts.User"))
        f.append(Text(type="value", rotation=90,text=footprint_name, at=[mil(50), -height*3/4],
            layer="F.Fab"))
        f.append(Text(type="user", rotation=90, text="%R", at=[mil(50), -height/2],
            layer="F.Fab"))
        
        # silkscreen
        f.append(Text(type="reference", text="REF**", at=[mil(50), -height/4],
            layer="F.SilkS", rotation=90, size=[1,1], thickness=0.15))

        file_handler = KicadFileHandler(f)
        file_handler.writeFile(footprint_name + ".kicad_mod")

