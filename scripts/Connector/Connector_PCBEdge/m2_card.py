#SPDX-License-Identifier: GPL-3.0-or-later
#Copyright (c) 2024, Lothar Felten <lothar.felten@gmail.com>
"""
m2_card 
M.2 card footprint generator script for KiCad
Supported dimensions: 2242, 2280, 22110, 3042, 3080, 30110
Supported notches: A, B, E and M
"""
import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

from KicadModTree import *

notchTypes = ['A', 'B', 'E', 'M']
notchOffset = {'A':6.625, 'B':5.625, 'E':2.625, 'M':-6.125}
widthTypes = [22, 30]
heightTypes = [42, 80, 110]
datasheet = "https://web.archive.org/web/20210118201723/http://read.pudn.com/downloads794/doc/project/3133918/PCIe_M.2_Electromechanical_Spec_Rev1.0_Final_11012013_RS_Clean.pdf"

for notchType in notchTypes:
    for widthType in widthTypes:
        for heightType in heightTypes:
            footprint_name = "M.2_" + str(widthType) + str(heightType) + "-xx-" + str(notchType)
            f = Footprint(footprint_name, FootprintType.SMD)
            f.setDescription(datasheet)
            f.setTags("Connector PCBEdge "+footprint_name)

            #settings
            padCount = 75
            padToPad = 0.5
            padHeight = 2.5
            padChamfer = 0.5
            padWidth = 0.35
            padSize = [padWidth, padHeight]
            padShape = Pad.SHAPE_ROUNDRECT
            padRadiusRatio = 0.2
            notchWidth = 1.2
            notch = notchOffset.get(notchType)
            cutWidth = 0.2
            conWidth = 19.85
            conHeight = 4
            conRadius = 0.5
            holeWidth = 3.5
            holeCopperWidth = 1.5
            layers_top = ['F.Cu', 'F.Mask']
            layers_bottom = ['B.Cu', 'B.Mask']
            yPad = conHeight - padHeight/2 - padChamfer
            xPadRight = ((padCount-1)/2 * padToPad)/2
            courtyardWidth = 0.1
            courtyardBorder = 0.1
            courtyardRadius = 3
            t1 = 0.1
            t2 = 0.15
            refSize = [0.7, 0.7]
            textsize = [1.0, 1.0]
            chamferLength = 0.30
            chamferText = "Chamfer 20 degree " + str(chamferLength) + " mm"
            chamferOffset = 5.5
            thicknessText = "PCB thickness 0.8 mm"
            thicknessOffset = 7
            valueTextOffset = -1.5
            referenceTextOffset = (-conWidth/2)+4
           
            # connector cutout
            f.append(PolygonLine(polygon=[[(-holeWidth/2), -(heightType-conHeight)],
                [(-widthType/2), -(heightType-conHeight)],
                [(-widthType/2), 0],
                [(-conRadius-conWidth/2), 0]],
                layer="Edge.Cuts", width=cutWidth))
            f.append(Arc(center=[-(conWidth/2)-conRadius, conRadius],
                start=[-(conWidth/2)-conRadius, 0],
                angle=90.0, layer="Edge.Cuts", width=cutWidth))
            f.append(PolygonLine(polygon=[[(-conWidth/2), conRadius],
                [(-conWidth/2), conHeight],
                [(notch-(notchWidth/2)), conHeight],
                [(notch-(notchWidth/2)), conRadius]],
                layer="Edge.Cuts", width=cutWidth))
            f.append(Arc(center=[notch, conRadius],
                start=[(notch-(notchWidth/2)), conRadius],
                angle=180.0, layer="Edge.Cuts", width=cutWidth))
            f.append(PolygonLine(polygon=[[(notch+(notchWidth/2)), conRadius],
                [(notch+(notchWidth/2)), conHeight],
                [(conWidth/2), conHeight],
                [(conWidth/2), conRadius]],
                layer="Edge.Cuts", width=cutWidth))
            f.append(Arc(center=[(conWidth/2)+conRadius, conRadius],
                start=[(conWidth/2)+conRadius, 0],
                angle=-90.0, layer="Edge.Cuts", width=cutWidth))
            f.append(PolygonLine(polygon=[[(conRadius+conWidth/2), 0],
                [(widthType/2), 0],
                [(widthType/2), -(heightType-conHeight)],
                [(holeWidth/2), -(heightType-conHeight)]],
                layer="Edge.Cuts", width=cutWidth))
            f.append(Arc(center=[0, -(heightType-conHeight)],
                start=[(holeWidth/2), -(heightType-conHeight)],
                angle=180.0, layer="Edge.Cuts", width=cutWidth))
                
            # mounting hole copper - TODO: this overlaps with the cutout on the edges of the arc
            #f.append(Arc(center=[0, -(heightType-conHeight)],
            #    start=[(holeWidth/2)+(holeCopperWidth/2), -(heightType-conHeight)],
            #    angle=180.0, layer="F.Cu", width=holeCopperWidth))
                
            # courtyard
            f.append(RectLine(start=[-((widthType+courtyardBorder)/2), 0-courtyardBorder],
                end=[((widthType+courtyardBorder)/2), conHeight+courtyardBorder],
                layer="F.CrtYd", width=courtyardWidth))
            f.append(PolygonLine(polygon=[[-(courtyardRadius), -(heightType-conHeight)],
                [(courtyardRadius), -(heightType-conHeight)]],
                layer="F.CrtYd", width=cutWidth))
            f.append(Arc(center=[0, -(heightType-conHeight)],
                start=[-(courtyardRadius), -(heightType-conHeight)],
                angle=-180.0, layer="F.CrtYd", width=cutWidth))        
            f.append(PolygonLine(polygon=[[-(courtyardRadius), -(heightType-conHeight)],
                [(courtyardRadius), -(heightType-conHeight)]],
                layer="B.CrtYd", width=cutWidth))
            f.append(Arc(center=[0, -(heightType-conHeight)],
                start=[-(courtyardRadius), -(heightType-conHeight)],
                angle=-180.0, layer="B.CrtYd", width=cutWidth))   
                
            # chamfer
            f.append(PolygonLine(polygon=[[-(conWidth/2), conHeight - chamferLength],
                [(notch-(notchWidth/2)), conHeight - chamferLength]],
                layer="Dwgs.User", width=cutWidth))
            f.append(PolygonLine(polygon=[[+(conWidth/2), conHeight - chamferLength],
                [(notch+(notchWidth/2)), conHeight - chamferLength]],
                layer="Dwgs.User", width=cutWidth))
            f.append(Text(type="user", text=chamferText, at=[0, chamferOffset],
                layer="Cmts.User", size=refSize, thickness=t2))
            f.append(Text(type="user", text=thicknessText, at=[0, thicknessOffset],
                layer="Cmts.User", size=refSize, thickness=t2))
                
            # silkscreen
            # TODO set alignment to left for REF**
            f.append(Text(type="reference", text="REF**", at=[referenceTextOffset, 0],
                layer="F.SilkS", size=textsize, thickness=t2))
            f.append(Text(type="user", text="1", at=[xPadRight, 0],
                layer="F.SilkS", size=textsize, thickness=t1))
            f.append(Text(type="user", text=str(notchType), at=[notch+notchWidth, 0],
                layer="F.SilkS", size=textsize, thickness=t1))

            # text
            # TODO set alignment to left for %R
            f.append(Text(type="value", text=footprint_name, at=[0, valueTextOffset],
                layer="F.Fab", size=textsize, thickness=t2))
            f.append(Text(type="user", text="%R", at=[referenceTextOffset, 0],
                layer="F.Fab", size=refSize, thickness=t2))

            # pads
            for i in range(0, padCount):
                x = xPadRight - (padToPad/2 * i)
                if i%2 == 0:
                    layer=layers_top
                else:
                    layer=layers_bottom
                if abs(notch - x) > 1:
                    f.append(Pad(number=i+1, type=Pad.TYPE_SMT, shape=padShape,
                             at=[x, yPad], size=padSize, layers=layer,
                             radius_ratio=padRadiusRatio))
            file_handler = KicadFileHandler(f)
            file_handler.writeFile(footprint_name + ".kicad_mod")
