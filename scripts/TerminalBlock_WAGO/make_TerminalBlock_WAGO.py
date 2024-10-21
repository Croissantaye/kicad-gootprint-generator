#!/usr/bin/env python3

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from footprint_scripts_terminal_blocks import *





if __name__ == '__main__':

    script_generated_note="script-generated using https://gitlab.com/kicad/libraries/kicad-footprint-generator/-/tree/master/scripts/TerminalBlock_WAGO";
    classname="TerminalBlock_WAGO"
    
    

   
    
    pins=[1,2,3,4,5,6,7,8,9,10,11,12,16,24]
    rm=7.5
    package_height=15
    leftbottom_offset=[2.75, 6.7, 3.75]
    ddrill=1.2
    pad=[2,3]
    screw_diameter=2.2
    bevel_height=[2.9]
    vsegment_lines_offset=[-1.25]
    opening=[2.9,2.3]
    opening_xoffset=1.25
    opening_yoffset=1.45
    opening_elliptic=True
    secondDrillDiameter=ddrill
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=[4,4.4]
    secondHoleOffset=[1.25,0]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=3#4
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[2.5,-0.75]
    secondEllipseSize=[0,0]
    secondEllipseOffset=[1.25,2.5]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="804-{0}".format(300+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, vsegment_lines_offset=vsegment_lines_offset,
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening_elliptic=opening_elliptic,
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, fifthHoleDiameter=fifthHoleDiameter,fifthHoleOffset=fifthHoleOffset,
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  secondEllipseSize=secondEllipseSize,secondEllipseOffset=secondEllipseOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

     
     

    
    pins=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,24]
    rm=5
    package_height=15
    leftbottom_offset=[2.75, 6.7, 3.75]
    ddrill=1.2
    pad=[2,3]
    screw_diameter=2.2
    bevel_height=[2.9]
    vsegment_lines_offset=[-1.25]
    opening=[2.9,2.3]
    opening_xoffset=1.25
    opening_yoffset=1.45
    opening_elliptic=True
    secondDrillDiameter=ddrill
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=[4,4.4]
    secondHoleOffset=[1.25,0]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=3#4
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[1.25,-0.75]
    secondEllipseSize=[0,0]
    secondEllipseOffset=[1.25,2.5]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="804-{0}".format(100+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad,  vsegment_lines_offset=vsegment_lines_offset,
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening_elliptic=opening_elliptic,
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, fifthHoleDiameter=fifthHoleDiameter,fifthHoleOffset=fifthHoleOffset,
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  secondEllipseSize=secondEllipseSize,secondEllipseOffset=secondEllipseOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)


    pins=[1,2,3,4,5,6,7,8,9,12,14,16,24,36,48]
    rm=5
    package_height=14
    leftbottom_offset=[3.5, 9, 3.8]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[5,14]
    secondHoleOffset=[0.5,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=[1,2.5]
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(100+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(400+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

    pins=[1,2,3,4,5,6,7,8,9,12,16,24]
    rm=7.5
    package_height=14
    leftbottom_offset=[3.5, 9, 6.3]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[rm,package_height]
    secondHoleOffset=[1.75,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=1,2.5
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(200+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(500+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

    pins=[1,2,3,4,5,6,8,9,12,16,24]
    rm=10
    package_height=14
    leftbottom_offset=[3.5, 9, 8.8]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[rm,package_height]
    secondHoleOffset=[3,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=1,2.5
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(300+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(600+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KICAD8_3DMODEL_DIR}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)


    # WAGO 2601

    pins=[2,3,4,5,6,8,9,10,11,12]
    rm=3.5
    package_height=14.5
    leftbottom_offset=[2.44, 5.35, 2.56]
    ddrill=1.2
    pad=[1.5,2.3]
    secondDrillOffset=[0,-5]

    for p in pins:
        name="2601-11{0:02}".format(p);
        webpage="https://www.wago.com/global/pcb-terminal-blocks-and-pluggable-connectors/pcb-terminal-block/p/{0}".format(name);
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)

        makeTerminalBlockStd(footprint_name=footprint_name,
            pins=p,
            rm=rm,
            package_height=package_height,
            leftbottom_offset=leftbottom_offset,
            ddrill=ddrill,
            pad=pad,
            screw_diameter=0,
            bevel_height=[],
            slit_screw=False,
            screw_pin_offset=[0,0],
            secondHoleDiameter=0,
            secondHoleOffset=[0,0],
            thirdHoleDiameter=0,
            thirdHoleOffset=[0,0],
            fourthHoleDiameter=0,
            fourthHoleOffset=[0,0],
            secondDrillDiameter=ddrill,
            secondDrillOffset=secondDrillOffset,
            secondDrillPad=pad,
            nibbleSize=[],
            nibblePos=[],
            fabref_offset=[0,0],
            stackable=False,
            tags_additional=[],
            lib_name="${KICAD8_3DMODEL_DIR}/" + classname,
            classname=classname,
            classname_description="Terminal Block WAGO {0}".format(name),
            webpage=webpage,
            script_generated_note=script_generated_note)

    pins=[2,3,4,5,6,7,8,9,10,11,12,14,24]
    rm=3.5
    package_height=12.75
    leftbottom_offset=[2.56, 5.45, 2.44]
    ddrill=1.2
    pad=[1.5,2.3]
    secondDrillOffset=[0,-5]

    for p in pins:
        name="2601-31{0:02}".format(p);
        webpage="https://www.wago.com/global/pcb-terminal-blocks-and-pluggable-connectors/pcb-terminal-block/p/{0}".format(name);
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_Vertical".format(name, rm, p)

        makeTerminalBlockStd(footprint_name=footprint_name,
            pins=p,
            rm=rm,
            package_height=package_height,
            leftbottom_offset=leftbottom_offset,
            ddrill=ddrill,
            pad=pad,
            screw_diameter=0,
            bevel_height=[],
            slit_screw=False,
            screw_pin_offset=[0,0],
            secondHoleDiameter=0,
            secondHoleOffset=[0,0],
            thirdHoleDiameter=0,
            thirdHoleOffset=[0,0],
            fourthHoleDiameter=0,
            fourthHoleOffset=[0,0],
            secondDrillDiameter=ddrill,
            secondDrillOffset=secondDrillOffset,
            secondDrillPad=pad,
            nibbleSize=[],
            nibblePos=[],
            fabref_offset=[0,0],
            stackable=False,
            tags_additional=[],
            lib_name="${KICAD8_3DMODEL_DIR}/" + classname,
            classname=classname,
            classname_description="Terminal Block WAGO {0}".format(name),
            webpage=webpage,
            script_generated_note=script_generated_note)
