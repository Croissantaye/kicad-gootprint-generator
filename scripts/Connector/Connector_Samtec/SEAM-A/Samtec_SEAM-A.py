#!/usr/bin/env python3

import math
import os
import sys
import argparse
import yaml

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..","..", "..", ".."))

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..","..", "..", "tools"))  # load parent path of tools

from KicadModTree import *
import itertools
from string import ascii_uppercase

def generateFootprint(config, fpParams, fpId):
    # Common parameters for all types
    size_source = "http://suddendocs.samtec.com/prints/seam-xx-xx.x-xx-xx-x-a-xx-footprint.pdf"
    pitchX = 1.27
    pitchY = pitchX
    pitchString = str(pitchX) + "x" + str(pitchY)    
    # The paste mask is bigger than the copper and stop-mask
    # For this type of connector it is a must to do so.
    pad_diameter = 0.64
    mask_margin = 0.0
    paste_margin = 0.125
    paste_ratio = 0.0
    npth_drill_AlignmentHole = 1.27
    # Holes use paste in hole technology .. therefore the THT-via size is same as drill
    # resulting in a THT with no copper pad
    pth_drill = 0.99
    pth_distance = 2.97
    pth_paste_length = 2.29
    
    # Check if given parameters are correct according catalogue ordering guideline
    # checking-clause
    # (-10 only available in 04 row)
    if ((fpParams["no_pins_of_row"] == 10) and (fpParams["no_of_rows"] != 4)):
        print('Skipping {0} => This connector is not orderable.'.format(fpId))
        sys.exit()
    # checking-clause
    # (-15 only available in 4 Row with -02.0 lead style and 10 row with any lead style)
    elif ((fpParams["no_pins_of_row"] == 15) and 
          (fpParams["no_of_rows"] != 4) and
        (fpParams["lead_style"] != "02.0")):
        print('Skipping {0} => This connector is not orderable.'.format(fpId))
        sys.exit()
    # checking-clause
    # (Four Rows, -06.5 not available)
    # (Five Rows, -06.5 not available)
    # (Six Rows, -06.5 not available)
    elif (((fpParams["no_of_rows"] == 4) or (fpParams["no_of_rows"] == 5) or (fpParams["no_of_rows"] == 6)) and 
          (fpParams["lead_style"] == "06.5")):
        print('Skipping {0} => This connector is not orderable.'.format(fpId))
        sys.exit()
    else:
        print('Building footprint for parameter set: {}'.format(fpId))    
    
    
    # Read the number of positions (a.k.a. number of pins of an row )
    num_positions = fpParams["no_pins_of_row"]
    # Read the number of rows
    num_rows = fpParams["no_of_rows"]
    # define the correct pin-order here according datasheet
    # tlbr = top left to bottom right
    # trbl = top right to bottom left
    # bltr = bottom left to top right
    # brtl = bottom right to top left
    pin_order = "trbl"
    # Parameters for SEAM-A and SEAM-A-GP used from datasheet
    tab_DIM_A = [[10, 15, 19, 20, 25, 30, 40, 50],                          # number of positions per row
                 [17.86, 24.03, 29.11, 30.38, 36.73, 43.08, 55.78, 68.48]]  # dimension values for the number of positions per row
    tab_DIM_B = [[10, 15, 19, 20, 25, 30, 40, 50],
                 [11.43, 17.78, 22.86, 24.13, 30.48, 36.83, 49.53, 62.23]]
    tab_DIM_C = [[10, 15, 19, 20, 25, 30, 40, 50],
                 [16.28, 22.63, 27.71, 28.98, 35.33, 41.68, 54.38, 67.08]]
    if ((fpParams["lead_style"] == "02.0") and (fpParams["no_of_rows"] != 14)):
        tab_DIM_D = [[4, 5, 6, 8, 10], # Row
                     [7.06, 9.60, 9.60, 12.14, 14.68]]
        tab_DIM_E = [[4, 5, 6, 8, 10],
                     [3.81, 5.08, 6.35, 8.89, 11.43]]
        tab_DIM_F = [[4, 5, 6, 8, 10],
                     [2.01, 3.05, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 5, 6, 8, 10],
                     [1.60, 0.89, 0.89, 0.89, 0.89]]
    elif ((fpParams["lead_style"] == "03.0") and (fpParams["no_of_rows"] != 14)):
        tab_DIM_D = [[4, 5, 6, 8, 10], # Row
                     [7.06, 9.60, 9.60, 12.14, 14.68]]
        tab_DIM_E = [[4, 5, 6, 8, 10],
                     [3.81, 5.08, 6.35, 8.89, 11.43]]
        tab_DIM_F = [[4, 5, 6, 8, 10],
                     [2.01, 3.05, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 5, 6, 8, 10],
                     [1.60, 0.89, 0.89, 0.89, 0.89]]
    elif (fpParams["lead_style"] == "03.5"):
        tab_DIM_D = [[4, 5, 6, 8, 10, 14], # Row
                     [7.06, 9.60, 9.60, 12.14, 14.68, 19.76]]
        tab_DIM_E = [[4, 5, 6, 8, 10, 14],
                     [3.81, 5.08, 6.35, 8.89, 11.43, 16.51]]
        tab_DIM_F = [[4, 5, 6, 8, 10, 14],
                     [2.01, 3.05, 3.05, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 5, 6, 8, 10, 14],
                     [1.60, 0.89, 0.89, 0.89, 0.89, 0.89]]
    elif ((fpParams["lead_style"] == "05.5") and 
          ((fpParams["no_of_rows"] == 5) or (fpParams["no_of_rows"] == 6))):   
        tab_DIM_D = [[5, 6], # Row
                     [9.60, 9.60]]
        tab_DIM_E = [[5, 6],
                     [5.08, 6.35]]
        tab_DIM_F = [[5, 6],
                     [3.05, 3.05]]
        tab_DIM_M = [[5, 6],
                     [0.89, 0.89]]
    elif ((fpParams["lead_style"] == "06.0") and (fpParams["no_of_rows"] == 6)):
        tab_DIM_D = [[6], # Row
                     [10.87]]
        tab_DIM_E = [[6],
                     [6.35]]
        tab_DIM_F = [[6],
                     [3.05]]
        tab_DIM_M = [[6],
                     [0.89]]
    elif ((fpParams["lead_style"] == "06.5") and 
          ((fpParams["no_of_rows"] == 8) or (fpParams["no_of_rows"] == 10))):    
        tab_DIM_D = [[8, 10], # Row
                     [13.41, 15.95]]
        tab_DIM_E = [[8, 10],
                     [8.89, 11.43]]
        tab_DIM_F = [[8, 10],
                     [3.05, 3.05]]
        tab_DIM_M = [[8, 10],
                     [0.89, 0.89]]
    elif ((fpParams["lead_style"] == "07.0") and 
          ((fpParams["no_of_rows"] != 5) or (fpParams["no_of_rows"] != 14))):
        tab_DIM_D = [[4, 6, 8, 10], # Row
                     [8.33, 10.87, 13.41, 15.95]]
        tab_DIM_E = [[4, 6, 8, 10],
                     [3.81, 6.35, 8.89, 11.43]]
        tab_DIM_F = [[4, 6, 8, 10],
                     [2.01, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 6, 8, 10],
                     [1.60, 0.89, 0.89, 0.89]]
    elif ((fpParams["lead_style"] == "09.0") and 
          ((fpParams["no_of_rows"] != 5) or (fpParams["no_of_rows"] != 14))):
        tab_DIM_D = [[4, 6, 8, 10], # Row
                     [8.33, 10.87, 13.41, 15.95]]
        tab_DIM_E = [[4, 6, 8, 10],
                     [3.81, 6.35, 8.89, 11.43]]
        tab_DIM_F = [[4, 6, 8, 10],
                     [2.01, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 6, 8, 10],
                     [1.60, 0.89, 0.89, 0.89]]
        
    elif ((fpParams["lead_style"] == "11.0") and 
          ((fpParams["no_of_rows"] != 5) or (fpParams["no_of_rows"] != 14))):    
        tab_DIM_D = [[4, 6, 8, 10], # Row
                     [8.33, 10.87, 13.41, 15.95]]
        tab_DIM_E = [[4, 6, 8, 10],
                     [3.81, 6.35, 8.89, 11.43]]
        tab_DIM_F = [[4, 6, 8, 10],
                     [2.01, 3.05, 3.05, 3.05]]
        tab_DIM_M = [[4, 6, 8, 10],
                     [1.60, 0.89, 0.89, 0.89]]
    else:
        print('Error, the lead_style={} is not defined with no_of_rows={}'.format(fpParams["lead_style"], fpParams["no_of_rows"]))
        sys.exit()
    
    tab_DIM_G = [[20, 30, 40, 50],
                 [44.86, 57.56, 70.26, 82.96]]
    tab_DIM_H = [[20, 30, 40, 50],
                 [38.94, 51.64, 64.34, 77.04]]

    len_REF_A = 1.52 # Dimension right side "nose" in datasheet page 1
    #len_REF_B = 3.12 # Dimension right side from DIM "A" in datasheet page 1
    #len_REF_C = 4.08 # Dimension upper to DIM "E" in datasheet page 3 for 05-row connectors
    len_REF_D = 1.91 # Dimension near DIM "C" in datasheet page 3 for 05-row connectors (upper left pin distance)
    len_REF_E = 5.61 # Dimension replacement for right and left side "nose" for SEAF-A-GP types connectors in datasheet page 5
    
    pkg_DIM_A = getTableEntry(tab_DIM_A, num_positions)
    if pkg_DIM_A == -1:
        print('Error, no_pins_of_row = {} does not exist in tab_DIM_A-list'.format(fpParams["no_pins_of_row"]))
        sys.exit()
    pkg_DIM_B = getTableEntry(tab_DIM_B, num_positions)
    if pkg_DIM_B == -1:
        print('Error, no_pins_of_row = {} does not exist in tab_DIM_B-list'.format(fpParams["no_pins_of_row"]))
        sys.exit()
    pkg_DIM_C = getTableEntry(tab_DIM_C, num_positions)
    if pkg_DIM_C == -1:
        print('Error, no_pins_of_row = {} does not exist in tab_DIM_C-list'.format(fpParams["no_pins_of_row"]))
        sys.exit()
    pkg_DIM_D = getTableEntry(tab_DIM_D, num_rows)
    if pkg_DIM_D == -1:
        print('Error, no_of_rows = {} does not exist in tab_DIM_D-list'.format(fpParams["no_of_rows"]))
        sys.exit()
    pkg_DIM_E = getTableEntry(tab_DIM_E, num_rows)
    if pkg_DIM_E == -1:
        print('Error, no_of_rows = {} does not exist in tab_DIM_E-list'.format(fpParams["no_of_rows"]))
        sys.exit()
    pkg_DIM_F = getTableEntry(tab_DIM_F, num_rows)
    if pkg_DIM_F == -1:
        print('Error, no_of_rows = {} does not exist in tab_DIM_F-list'.format(fpParams["no_of_rows"]))
        sys.exit()
    pkg_DIM_M = getTableEntry(tab_DIM_M, num_rows)
    if pkg_DIM_F == -1:
        print('Error, no_of_rows = {} does not exist in tab_DIM_M-list'.format(fpParams["no_of_rows"]))
        sys.exit()

    
    
    pkg_DIM_G = getTableEntry(tab_DIM_G, num_positions)
    if pkg_DIM_G == -1:
        print('Error, no_pins_of_row = {} does not exist in tab_DIM_G-list'.format(fpParams["no_pins_of_row"]))
        sys.exit()
    pkg_DIM_H = getTableEntry(tab_DIM_H, num_positions)
    if pkg_DIM_H == -1:
        print('Error, no_pins_of_row = {} does not exist in tab_DIM_H-list'.format(fpParams["no_pins_of_row"]))
        sys.exit()


    #num_positions = fpParams["layout_x"]
    #num_rows = fpParams["layout_y"]
    
    if "additional_tags" in fpParams:
        additionalTag = " " + fpParams["additional_tags"]
    else:
        additionalTag = ""
    
    if "row_names" in fpParams:
        row_names = fpParams["row_names"]
    else:
        row_names = config['row_names']
    
    if "row_skips" in fpParams:
        row_skips = fpParams["row_skips"]
    else:
        row_skips = []

    # must be given pitch (equal in X and Y) or a unique pitch in both X and Y
    #if "pitch" in fpParams:
    #    if "pitch_x" and "pitch_y" in fpParams:
    #        raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fpId))
    #    else:
    #        pitchString = str(fpParams["pitch"])
    #        pitchX = fpParams["pitch"]
    #        pitchY = fpParams["pitch"]
    #else:
    #    if "pitch_x" and "pitch_y" in fpParams:
    #        pitchString = str(fpParams["pitch_x"]) + "x" + str(fpParams["pitch_y"])
    #        pitchX = fpParams["pitch_x"]
    #        pitchY = fpParams["pitch_y"]
    #    else:
    #        raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fpId))

    f = Footprint(fpId)
    f.setAttribute("smd")
    #if "mask_margin" in fpParams: f.setMaskMargin(fpParams["mask_margin"])
    #if "paste_margin" in fpParams: f.setPasteMargin(fpParams["paste_margin"])
    #if "paste_ratio" in fpParams: f.setPasteMarginRatio(fpParams["paste_ratio"])
    f.setMaskMargin(mask_margin)
    f.setPasteMargin(paste_margin)
    f.setPasteMarginRatio(paste_ratio)

    s1 = [1.0, 1.0]
    s2 = [min(1.0, round(pkg_DIM_A / 4.3, 2))] * 2

    t1 = 0.15 * s1[0]
    t2 = 0.15 * s2[0]

    padShape = Pad.SHAPE_CIRCLE
    if "pad_shape" in fpParams:
        if fpParams["pad_shape"] == "rect":
            padShape = Pad.SHAPE_RECT
        if fpParams["pad_shape"] == "roundrect":
            padShape = Pad.SHAPE_ROUNDRECT

    #chamfer = min(config['fab_bevel_size_absolute'], min(pkgX, pkgY) * config['fab_bevel_size_relative'])
    
    silkOffset = config['silk_fab_offset']
    crtYdOffset = config['courtyard_offset']['connector']
    
    

    X_Center = 0.0
    Y_Center = 0.0
    
    ########################### Front Edge of PCB - Marker #################################
    # not needed here

    ########################### Fabrication, Courtyard and Silk  #################################   
    if (fpParams["option"] == "NONE"):
        # Generating Points for the "Fab"-layer (fabrication)
        P1_X_Fabrication = X_Center - (pkg_DIM_A / 2.0)
        P1_Y_Fabrication = Y_Center - (pkg_DIM_D / 2.0)
        P2_X_Fabrication = X_Center + (pkg_DIM_A / 2.0)
        P2_Y_Fabrication = P1_Y_Fabrication
        P3_X_Fabrication = P2_X_Fabrication
        P3_Y_Fabrication = Y_Center - (len_REF_A / 2.0) 
        P4_X_Fabrication = X_Center + ((pkg_DIM_A / 2.0) + pkg_DIM_M)
        P4_Y_Fabrication = P3_Y_Fabrication
        P5_X_Fabrication = P4_X_Fabrication
        P5_Y_Fabrication = Y_Center + (len_REF_A / 2.0)
        P6_X_Fabrication = P3_X_Fabrication
        P6_Y_Fabrication = P5_Y_Fabrication
        P7_X_Fabrication = P2_X_Fabrication
        P7_Y_Fabrication = Y_Center + (pkg_DIM_D / 2.0)
        P8_X_Fabrication = P1_X_Fabrication
        P8_Y_Fabrication = P7_Y_Fabrication
        # Generating Points for the "crtYd"-layer (courty yard)
        P1_X_Courtyard = crtYdRound(P1_X_Fabrication - crtYdOffset)
        P1_Y_Courtyard = crtYdRound(P1_Y_Fabrication - crtYdOffset)
        P2_X_Courtyard = crtYdRound(P4_X_Fabrication + crtYdOffset)
        P2_Y_Courtyard = P1_Y_Courtyard
        P3_X_Courtyard = P2_X_Courtyard
        P3_Y_Courtyard = crtYdRound(P7_Y_Fabrication + crtYdOffset)
        P4_X_Courtyard = P1_X_Courtyard
        P4_Y_Courtyard = P3_Y_Courtyard        
        # Generating Points for the "Silk"-layer (silkscreed)
        P1_X_Silk = P1_X_Fabrication - silkOffset
        P1_Y_Silk = P1_Y_Fabrication - silkOffset
        P2_X_Silk = P2_X_Fabrication + silkOffset
        P2_Y_Silk = P2_Y_Fabrication - silkOffset
        P3_X_Silk = P3_X_Fabrication + silkOffset
        P3_Y_Silk = P3_Y_Fabrication - silkOffset
        P4_X_Silk = P4_X_Fabrication + silkOffset
        P4_Y_Silk = P4_Y_Fabrication - silkOffset
        P5_X_Silk = P5_X_Fabrication + silkOffset
        P5_Y_Silk = P5_Y_Fabrication + silkOffset
        P6_X_Silk = P6_X_Fabrication + silkOffset
        P6_Y_Silk = P6_Y_Fabrication + silkOffset
        P7_X_Silk = P7_X_Fabrication + silkOffset
        P7_Y_Silk = P7_Y_Fabrication + silkOffset
        P8_X_Silk = P8_X_Fabrication - silkOffset
        P8_Y_Silk = P8_Y_Fabrication + silkOffset
        if (fpParams["no_of_rows"] != 5):
            # Define the position of pads to be placed
            Pad_X_Left = X_Center - pitchX * ((num_positions - 1) / 2.0)
            Pad_X_Right = X_Center + pitchX * ((num_positions - 1) / 2.0)
            Pad_Y_Top = Y_Center - pitchY * ((num_rows - 1) / 2.0)
            Pad_Y_Bottom = Y_Center + pitchY * ((num_rows - 1) / 2.0)
        else: # connectors with rows = 5 are not symmetric about horizontal line
            Pad_X_Left = X_Center - pitchX * ((num_positions - 1) / 2.0)
            Pad_X_Right = X_Center + pitchX * ((num_positions - 1) / 2.0)
            Pad_Y_Top = Y_Center + len_REF_D - pkg_DIM_E
            Pad_Y_Bottom = Y_Center + len_REF_D
        # Define the position of the REF** in silkscreen
        Ref_X_Silk = X_Center
        Ref_Y_Silk = P1_Y_Courtyard - 2.0
        # Define the position of the REF** in fabrication
        Ref_X_Fab = X_Center
        Ref_Y_Fab = Y_Center
        # Define the position of the VALUE in fabrication
        Value_X_Fabrication = X_Center
        Value_Y_Fabrication = P4_Y_Courtyard + 2.0
        # Setting the correct line width for fabrication, courtyard and silk layers
        width_Line_Fabrication = configuration['fab_line_width']
        width_Line_Courtyard = configuration['courtyard_line_width']
        width_line_Silk = configuration['silk_line_width']
        # Place the Text
        f.append(Text(type="reference",
                      text="REF**",
                      at=[Ref_X_Silk, Ref_Y_Silk],
                      layer="F.SilkS",
                      size=s1,
                      thickness=t1))
    
        f.append(Text(type="value",
                      text=fpId,
                      at=[Value_X_Fabrication, Value_Y_Fabrication],
                      layer="F.Fab",
                      size=s1,
                      thickness=t1))
    
        f.append(Text(type="user",
                      text="%R",
                      at=[Ref_X_Fab, Ref_Y_Fab],
                      layer="F.Fab",
                      size=s2,
                      thickness=t2))
        # Place the fabrication layer line
        f.append(PolygoneLine(polygone=[[P1_X_Fabrication, P1_Y_Fabrication],
                                        [P2_X_Fabrication, P2_Y_Fabrication],
                                        [P3_X_Fabrication, P3_Y_Fabrication],
                                        [P4_X_Fabrication, P4_Y_Fabrication],
                                        [P5_X_Fabrication, P5_Y_Fabrication],
                                        [P6_X_Fabrication, P6_Y_Fabrication],
                                        [P7_X_Fabrication, P7_Y_Fabrication],
                                        [P8_X_Fabrication, P8_Y_Fabrication],
                                        [P1_X_Fabrication, P1_Y_Fabrication]],
                              layer="F.Fab",
                              width=width_Line_Fabrication))
    
        # Place the courtyard layer line
        f.append(RectLine(start=[P1_X_Courtyard, P1_Y_Courtyard],
                          end=[P3_X_Courtyard, P3_Y_Courtyard],
                          layer="F.CrtYd",
                          width=width_Line_Courtyard))
        # Place the silk layer line
        f.append(PolygoneLine(polygone=[[P1_X_Silk, P1_Y_Silk],
                                        [P2_X_Silk, P2_Y_Silk],
                                        [P3_X_Silk, P3_Y_Silk],
                                        [P4_X_Silk, P4_Y_Silk],
                                        [P5_X_Silk, P5_Y_Silk],
                                        [P6_X_Silk, P6_Y_Silk],
                                        [P7_X_Silk, P7_Y_Silk],
                                        [P8_X_Silk, P8_Y_Silk],
                                        [P1_X_Silk, P1_Y_Silk]],
                              layer="F.SilkS",
                              width=width_line_Silk))
    elif (fpParams["option"] == "LP"):
        print('Error, this type of option={} is not defined nor implemented'.format(fpParams["option"]))
        sys.exit()
    elif (fpParams["option"] == "GP"):
        # Generating Points for the "Fab"-layer (fabrication)
        P1_X_Fabrication = X_Center - (pkg_DIM_A / 2.0)
        P1_Y_Fabrication = Y_Center - (pkg_DIM_D / 2.0)
        P2_X_Fabrication = X_Center + (pkg_DIM_A / 2.0)
        P2_Y_Fabrication = P1_Y_Fabrication
        P3_X_Fabrication = P2_X_Fabrication
        P3_Y_Fabrication = Y_Center - (len_REF_E / 2.0)
        P4_X_Fabrication = X_Center + (pkg_DIM_G / 2.0)
        P4_Y_Fabrication = P3_Y_Fabrication
        P5_X_Fabrication = P4_X_Fabrication
        P5_Y_Fabrication = Y_Center + (len_REF_E / 2.0)
        P6_X_Fabrication = P3_X_Fabrication
        P6_Y_Fabrication = P5_Y_Fabrication
        P7_X_Fabrication = P2_X_Fabrication
        P7_Y_Fabrication = Y_Center + (pkg_DIM_D / 2.0)
        P8_X_Fabrication = P1_X_Fabrication
        P8_Y_Fabrication = P7_Y_Fabrication
        P9_X_Fabrication = P8_X_Fabrication
        P9_Y_Fabrication = P6_Y_Fabrication
        P10_X_Fabrication = X_Center - (pkg_DIM_G / 2.0)
        P10_Y_Fabrication = P9_Y_Fabrication
        P11_X_Fabrication = P10_X_Fabrication
        P11_Y_Fabrication = P4_Y_Fabrication
        P12_X_Fabrication = P1_X_Fabrication
        P12_Y_Fabrication = P11_Y_Fabrication        
        # Generating Points for the "crtYd"-layer (courty yard)
        P1_X_Courtyard = crtYdRound(P11_X_Fabrication - crtYdOffset)
        P1_Y_Courtyard = crtYdRound(P1_Y_Fabrication - crtYdOffset)
        P2_X_Courtyard = crtYdRound(P4_X_Fabrication + crtYdOffset)
        P2_Y_Courtyard = P1_Y_Courtyard
        P3_X_Courtyard = P2_X_Courtyard
        P3_Y_Courtyard = crtYdRound(P7_Y_Fabrication + crtYdOffset)
        P4_X_Courtyard = P1_X_Courtyard
        P4_Y_Courtyard = P3_Y_Courtyard
        # Generating Points for the "Silk"-layer (silkscreed)
        P1_X_Silk = P1_X_Fabrication - silkOffset
        P1_Y_Silk = P1_Y_Fabrication - silkOffset
        P2_X_Silk = P2_X_Fabrication + silkOffset
        P2_Y_Silk = P2_Y_Fabrication - silkOffset            
        P3_X_Silk = P3_X_Fabrication + silkOffset
        P3_Y_Silk = P3_Y_Fabrication - silkOffset
        P4_X_Silk = P4_X_Fabrication + silkOffset
        P4_Y_Silk = P4_Y_Fabrication - silkOffset
        P5_X_Silk = P5_X_Fabrication + silkOffset
        P5_Y_Silk = P5_Y_Fabrication + silkOffset
        P6_X_Silk = P6_X_Fabrication + silkOffset
        P6_Y_Silk = P6_Y_Fabrication + silkOffset
        P7_X_Silk = P7_X_Fabrication + silkOffset
        P7_Y_Silk = P7_Y_Fabrication + silkOffset
        P8_X_Silk = P8_X_Fabrication - silkOffset
        P8_Y_Silk = P8_Y_Fabrication + silkOffset
        P9_X_Silk = P9_X_Fabrication - silkOffset
        P9_Y_Silk = P9_Y_Fabrication + silkOffset
        P10_X_Silk = P10_X_Fabrication - silkOffset
        P10_Y_Silk = P10_Y_Fabrication + silkOffset
        P11_X_Silk = P11_X_Fabrication - silkOffset
        P11_Y_Silk = P11_Y_Fabrication - silkOffset
        P12_X_Silk = P12_X_Fabrication - silkOffset
        P12_Y_Silk = P12_Y_Fabrication - silkOffset
        # Define the position of pads to be placed
        Pad_X_Left = X_Center - pitchX * ((num_positions - 1) / 2.0)
        Pad_X_Right = X_Center + pitchX * ((num_positions - 1) / 2.0)
        Pad_Y_Top = Y_Center - pitchY * ((num_rows - 1) / 2.0)
        Pad_Y_Bottom = Y_Center + pitchY * ((num_rows - 1) / 2.0)
        # Define the position of the REF** in silkscreen
        Ref_X_Silk = X_Center
        Ref_Y_Silk = P1_Y_Courtyard - 2.0
        # Define the position of the REF** in fabrication
        Ref_X_Fab = X_Center
        Ref_Y_Fab = Y_Center
        # Define the position of the VALUE in fabrication
        Value_X_Fabrication = X_Center
        Value_Y_Fabrication = P4_Y_Courtyard + 2.0
        # Setting the correct line width for fabrication, courtyard and silk layers
        width_Line_Fabrication = configuration['fab_line_width']
        width_Line_Courtyard = configuration['courtyard_line_width']
        width_line_Silk = configuration['silk_line_width']
        # Place the Text
        f.append(Text(type="reference",
                      text="REF**",
                      at=[Ref_X_Silk, Ref_Y_Silk],
                      layer="F.SilkS",
                      size=s1,
                      thickness=t1))
    
        f.append(Text(type="value",
                      text=fpId,
                      at=[Value_X_Fabrication, Value_Y_Fabrication],
                      layer="F.Fab",
                      size=s1,
                      thickness=t1))
    
        f.append(Text(type="user",
                      text="%R",
                      at=[Ref_X_Fab, Ref_Y_Fab],
                      layer="F.Fab",
                      size=s2,
                      thickness=t2))
        # Place the fabrication layer line
        f.append(PolygoneLine(polygone=[[P1_X_Fabrication, P1_Y_Fabrication],
                                        [P2_X_Fabrication, P2_Y_Fabrication],
                                        [P3_X_Fabrication, P3_Y_Fabrication],
                                        [P4_X_Fabrication, P4_Y_Fabrication],
                                        [P5_X_Fabrication, P5_Y_Fabrication],
                                        [P6_X_Fabrication, P6_Y_Fabrication],
                                        [P7_X_Fabrication, P7_Y_Fabrication],
                                        [P8_X_Fabrication, P8_Y_Fabrication],
                                        [P9_X_Fabrication, P9_Y_Fabrication],
                                        [P10_X_Fabrication, P10_Y_Fabrication],
                                        [P11_X_Fabrication, P11_Y_Fabrication],
                                        [P12_X_Fabrication, P12_Y_Fabrication],
                                        [P1_X_Fabrication, P1_Y_Fabrication]],
                              layer="F.Fab",
                              width=width_Line_Fabrication))
    
        # Place the courtyard layer line
        f.append(RectLine(start=[P1_X_Courtyard, P1_Y_Courtyard],
                          end=[P3_X_Courtyard, P3_Y_Courtyard],
                          layer="F.CrtYd",
                          width=width_Line_Courtyard))
        # Place the silk layer line
        f.append(PolygoneLine(polygone=[[P1_X_Silk, P1_Y_Silk],
                                        [P2_X_Silk, P2_Y_Silk],
                                        [P3_X_Silk, P3_Y_Silk],
                                        [P4_X_Silk, P4_Y_Silk],
                                        [P5_X_Silk, P5_Y_Silk],
                                        [P6_X_Silk, P6_Y_Silk],
                                        [P7_X_Silk, P7_Y_Silk],
                                        [P8_X_Silk, P8_Y_Silk],
                                        [P9_X_Silk, P9_Y_Silk],
                                        [P10_X_Silk, P10_Y_Silk],
                                        [P11_X_Silk, P11_Y_Silk],
                                        [P12_X_Silk, P12_Y_Silk],
                                        [P1_X_Silk, P1_Y_Silk]],
                              layer="F.SilkS",
                              width=width_line_Silk))
    else:
        print('Error, this type of option={} is not defined in general'.format(fpParams["option"]))
        sys.exit()
    
    ########################### Pin 1 - Marker #################################
    markerOffset = 0.4
    markerLength = pad_diameter
    
    PM1_X_Pin1Marker = Pad_X_Right
    PM1_Y_Pin1Marker = P1_Y_Silk - markerOffset
    
    PM2_X_Pin1Marker = PM1_X_Pin1Marker - (markerLength / 2)
    PM2_Y_Pin1Marker = PM1_Y_Pin1Marker - (markerLength / sqrt(2))
    
    PM3_X_Pin1Marker = PM2_X_Pin1Marker + markerLength
    PM3_Y_Pin1Marker = PM2_Y_Pin1Marker
    
    # Silk
    f.append(PolygoneLine(polygone=[[PM1_X_Pin1Marker, PM1_Y_Pin1Marker],
                                    [PM2_X_Pin1Marker, PM2_Y_Pin1Marker],
                                    [PM3_X_Pin1Marker, PM3_Y_Pin1Marker],
                                    [PM1_X_Pin1Marker, PM1_Y_Pin1Marker]],
                          layer="F.SilkS",
                          width=width_line_Silk))    
    
    ########################### Pads Generation ###################    
    # Pads generated according pin_order
    # tlbr = top left to bottom right
    # trbl = top right to bottom left
    # bltr = bottom left to top right
    # brtl = bottom right to top left
    pad_array_size = num_positions * num_rows
    if row_skips == []:
        for _ in range(num_rows):
            row_skips.append([])
    for row_num, row in zip(range(num_rows), row_names):
        row_set = set(range(1, num_positions + 1))
        for item in row_skips[row_num]:
            try:
                # If item is a range, remove that range
                row_set -= set(range(*item))
                pad_array_size -= item[1] - item[0]
            except TypeError:
                # If item is an int, remove that int
                row_set -= {item}
                pad_array_size -= 1
        for col in row_set:
            if pin_order == "tlbr":            
                f.append(Pad(number="{}{}".format(row, col),
                             type=Pad.TYPE_SMT,
                             shape=padShape,
                             at=[Pad_X_Left + (col-1) * pitchX, Pad_Y_Top + row_num * pitchY],
                             size=[pad_diameter, pad_diameter],
                             layers=Pad.LAYERS_SMT, 
                             radius_ratio=config['round_rect_radius_ratio']))
            elif pin_order == "trbl":
                f.append(Pad(number="{}{}".format(row, col),
                             type=Pad.TYPE_SMT,
                             shape=padShape,
                             at=[Pad_X_Right - (col-1) * pitchX, Pad_Y_Top + row_num * pitchY],
                             size=[pad_diameter, pad_diameter],
                             layers=Pad.LAYERS_SMT, 
                             radius_ratio=config['round_rect_radius_ratio']))
            elif pin_order == "bltr":
                f.append(Pad(number="{}{}".format(row, col),
                             type=Pad.TYPE_SMT,
                             shape=padShape,
                             at=[Pad_X_Left + (col-1) * pitchX, Pad_Y_Bottom - row_num * pitchY],
                             size=[pad_diameter, pad_diameter],
                             layers=Pad.LAYERS_SMT, 
                             radius_ratio=config['round_rect_radius_ratio']))
            elif pin_order == "brtl":
                f.append(Pad(number="{}{}".format(row, col),
                             type=Pad.TYPE_SMT,
                             shape=padShape,
                             at=[Pad_X_Right - (col-1) * pitchX, Pad_Y_Bottom - row_num * pitchY],
                             size=[pad_diameter, pad_diameter],
                             layers=Pad.LAYERS_SMT, 
                             radius_ratio=config['round_rect_radius_ratio']))
            else:
                print('Error, pin_order = {} does not exist.'.format(pin_order))
                sys.exit()
                
    ##################  Alignment Holes NPTH  ########################
    # Those are all the same for "NONE", "GP" or "LP"
    PAH1_X_AlignmentHole = X_Center - (pkg_DIM_C / 2.0)
    PAH1_Y_AlignmentHole = Y_Center + pkg_DIM_F

    f.append(Pad(at=[PAH1_X_AlignmentHole, PAH1_Y_AlignmentHole],
                 number="",
                 type=Pad.TYPE_NPTH,
                 shape=Pad.SHAPE_CIRCLE,
                 size=npth_drill_AlignmentHole,
                 drill=npth_drill_AlignmentHole,
                 layers=Pad.LAYERS_NPTH))

    PAH2_X_AlignmentHole = X_Center + (pkg_DIM_C / 2.0)
    PAH2_Y_AlignmentHole = Y_Center

    f.append(Pad(at=[PAH2_X_AlignmentHole, PAH2_Y_AlignmentHole],
                 number="",
                 type=Pad.TYPE_NPTH,
                 shape=Pad.SHAPE_CIRCLE,
                 size=npth_drill_AlignmentHole,
                 drill=npth_drill_AlignmentHole,
                 layers=Pad.LAYERS_NPTH))
        
    ##################  Latch Post Holes PTH  ########################
    if (fpParams["option"] == "GP"):
        # Left side Latch post holes
        PAH1_X_LatchPostHoleLeftSide = X_Center - (pkg_DIM_H / 2.0) - (pth_distance / 2.0)
        PAH1_Y_LatchPostHoleLeftSide = Y_Center - (pth_distance / 2.0)
        PAH2_X_LatchPostHoleLeftSide =  X_Center - (pkg_DIM_H / 2.0) + (pth_distance / 2.0)
        PAH2_Y_LatchPostHoleLeftSide = PAH1_Y_LatchPostHoleLeftSide
        PAH3_X_LatchPostHoleLeftSide = PAH1_X_LatchPostHoleLeftSide
        PAH3_Y_LatchPostHoleLeftSide = Y_Center + (pth_distance / 2.0)
        PAH4_X_LatchPostHoleLeftSide = PAH2_X_LatchPostHoleLeftSide
        PAH4_Y_LatchPostHoleLeftSide = PAH3_Y_LatchPostHoleLeftSide
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH1_X_LatchPostHoleLeftSide, PAH1_Y_LatchPostHoleLeftSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH1_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH2_X_LatchPostHoleLeftSide, PAH2_Y_LatchPostHoleLeftSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH2_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH3_X_LatchPostHoleLeftSide, PAH3_Y_LatchPostHoleLeftSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH3_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH4_X_LatchPostHoleLeftSide, PAH4_Y_LatchPostHoleLeftSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH4_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleLeftSide - (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleLeftSide + (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleLeftSide - (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleLeftSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Right side Latch post holes
        PAH1_X_LatchPostHoleRightSide = X_Center + (pkg_DIM_H / 2.0) - (pth_distance / 2.0)
        PAH1_Y_LatchPostHoleRightSide = Y_Center - (pth_distance / 2.0)
        PAH2_X_LatchPostHoleRightSide = X_Center + (pkg_DIM_H / 2.0) + (pth_distance / 2.0)
        PAH2_Y_LatchPostHoleRightSide = PAH1_Y_LatchPostHoleRightSide
        PAH3_X_LatchPostHoleRightSide = PAH1_X_LatchPostHoleRightSide
        PAH3_Y_LatchPostHoleRightSide = Y_Center + (pth_distance / 2.0)
        PAH4_X_LatchPostHoleRightSide = PAH2_X_LatchPostHoleRightSide
        PAH4_Y_LatchPostHoleRightSide = PAH3_Y_LatchPostHoleRightSide
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH1_X_LatchPostHoleRightSide, PAH1_Y_LatchPostHoleRightSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH1_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)],
                                [PAH1_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH1_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH2_X_LatchPostHoleRightSide, PAH2_Y_LatchPostHoleRightSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH2_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)],
                                [PAH2_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH2_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH3_X_LatchPostHoleRightSide, PAH3_Y_LatchPostHoleRightSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH3_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)],
                                [PAH3_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH3_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
        
        # Apply the pad itself without a solder paste mask
        f.append(Pad(at=[PAH4_X_LatchPostHoleRightSide, PAH4_Y_LatchPostHoleRightSide],
                 number="",
                 type=Pad.TYPE_THT,
                 shape=Pad.SHAPE_CIRCLE,
                 size=pth_drill,
                 drill= pth_drill,
                 layers=Pad.LAYERS_THT))
        # Apply the solder paste mask            
        f.append(Polygon(nodes=[[PAH4_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleRightSide - (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleRightSide + (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)],
                                [PAH4_X_LatchPostHoleRightSide - (pth_paste_length / 2.0), PAH4_Y_LatchPostHoleRightSide + (pth_paste_length / 2.0)]],
                         layer='F.Paste',
                         width=0.0))
  
    ##################  Gereration of File-Name, Description and Tags  ########################
    # Prepare name variables for footprint folder, footprint name, etc.
    familiyType = fpParams['family']
    packageType = fpId

    f.append(Model(filename="{}Connector_Samtec_{}.3dshapes/{}.wrl".format(
                  config['3d_model_prefix'], familiyType, fpId)))

    f.setDescription("{0}, {1}x{2}mm, {3} Ball, {4}x{5} Layout, {6}mm Pitch, {7}".format(
                     fpId,
                     ((P1_X_Courtyard * -1) + P2_X_Courtyard),
                     ((P1_Y_Courtyard * -1) + P4_Y_Courtyard),
                     pad_array_size,
                     num_positions,
                     num_rows,
                     pitchString,
                     size_source))
    f.setTags("{} {} {}{}".format(
              packageType,
              pad_array_size,
              pitchString,
              additionalTag))

    outputDir = 'Connector_Samtec_{lib_name:s}.pretty/'.format(lib_name=familiyType)
    if not os.path.isdir(outputDir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(outputDir)
    filename = '{outdir:s}{fpId:s}.kicad_mod'.format(outdir=outputDir, fpId=fpId)
    
    file_handler = KicadFileHandler(f)
    file_handler.writeFile(filename)

def crtYdRound(x):
        # Round away from zero for proper courtyard calculation
        neg = x < 0
        if neg:
            x = -x
        x = math.ceil(x * 100) / 100.0
        if neg:
            x = -x
        return x
    
def rowNameGenerator(seq):
    for n in itertools.count(1):
        for s in itertools.product(seq, repeat = n):
            yield ''.join(s)

def getTableEntry(table, number):
    pkg_val = -1
    for i in range(len(table[0])):
        #print('{}'.format(table[0][i]))
        if table[0][i] == number:
            pkg_val = table[1][i]
            break; # quit the for-loop when a correct match is made to reduce script duration time
    return pkg_val
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../../tools/global_config_files/config_KLCv3.0.yaml')
    # parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../package_config_KLCv3.yaml')

    args = parser.parse_args()
    
    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    # with open(args.series_config, 'r') as config_stream:
        # try:
            # configuration.update(yaml.safe_load(config_stream))
        # except yaml.YAMLError as exc:
            # print(exc)
    
    # generate dict of A, B .. Y, Z, AA, AB .. CY less easily-confused letters
    rowNamesList = [x for x in ascii_uppercase if x not in ["I", "O", "Q", "S", "X", "Z"]]
    configuration.update({'row_names': list(itertools.islice(rowNameGenerator(rowNamesList), 80))})

    for filepath in args.files:
        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            generateFootprint(configuration, cmd_file[pkg], pkg)