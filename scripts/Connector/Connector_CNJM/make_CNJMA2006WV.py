#!/usr/bin/env python3

#
# CNJM CNJMA2006WV-S footprint generator
#   Currently only generates CNJMA2006WV-S-2xXX fooprints (straight SMD variants) 
#
# Sources:
#   https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_CNJM-CNJMA2006WV-S-2X8P_C2834695.pdf
#

#
# Author: Armin Schoisswohl @armin.sch
#
# This file is heavily inspired from the MECF card edge generator by @poeschlr
#

import sys
import os

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0], "..", "..", "..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools")) # load kicad_mod path

import argparse
import yaml

from KicadModTree import *  # NOQA
from footprint_text_fields import addTextFields

lib_name_category = 'CNJM'

pad_pitch = 2.0

from collections import namedtuple

datasheet = "https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_CNJM-CNJMA2006WV-S-2X8P_C2834695.pdf"

class Size(namedtuple('Size', ['x', 'y'])):
    def to_rect_line(self, layer='F.Fab', width=0.1):
        """
        Convert this Size to a RectLine, centered on the origin.
        """
        return RectLine(
            start=[-self.x/2, -self.y/2], end=[self.x/2, self.y/2],
            layer=layer, width=width
        )

pad_size = Size(1.1, 2.0)

# Number of pins per row: 2 => 2x02 pins !!
pinrange = range(2, 20+1, )

def y_pad_position(pad_number: int, n_positions: int):
    pos_unsigned = 5.30/2 + pad_size.y/2
    # Pad "1" on the lower lower row
    if pad_number % 2 == 0:
        return pos_unsigned
    else:
        return -pos_unsigned
    
def pad_column_number(pad_number: int, n_positions: int):
    return (pad_number + 1) // 2

def x_pad_position(pad_number: int, n_positions: int):
    # NOTE: Pin 1,2 or 3,4 always have the same X position
    column = pad_column_number(pad_number, n_positions)
    
    half_positions = n_positions / 2
    return (column - half_positions - 0.5) * pad_pitch

def overall_width(n_positions: int):
    """Overall component width"""
    return (n_positions + 1) * pad_pitch

def component_size(n_positions):
    """Component size (F.Fab layer)"""
    return Size(overall_width(n_positions), 5.3)

def roundToBase(value, base):
    return round(value/base) * base

def generate_one_footprint(n_positions: int, variant: str, configuration):
    fp_name = f'CNJM_CNJMA2006WV-S-2x{n_positions:d}_P2.0mm'

    print("%s" % fp_name)
    kicad_mod = Footprint(fp_name, FootprintType.UNSPECIFIED)

    description = f"Dual-row 2.0mm SMD connector, 2x{n_positions:02d} contacts, 6.2mm height {datasheet}"
    #set the FP description
    kicad_mod.setDescription(description)

    tags = "conn cnjm phd"

    #set the FP tags
    kicad_mod.setTags(tags)
    
    # Create F.Fab layer
    kicad_mod.append(component_size(n_positions).to_rect_line(
        layer='F.Fab', width=configuration['fab_line_width'])
    )
    
    ## create courtyards
    #for layer in ['F.CrtYd', 'B.CrtYd']:
    #    kicad_mod.append(RectLine(start=[left, top], end=[right, bot], layer=layer, width=configuration['courtyard_line_width']))
    
    # Create Pads. NOTE: For n_positions=3, we create 6 pads, since this is a 2xN footprint
    for i in range(1, (n_positions*2)+1):
        x = x_pad_position(i, n_positions)
        y = y_pad_position(i, n_positions)
        kicad_mod.append(Pad(number=i, type=Pad.TYPE_CONNECT, shape=Pad.SHAPE_ROUNDRECT,
            at=[x, y], size=list(pad_size), layers=Pad.LAYERS_CONNECT_FRONT)
        )
    
    ####
    #### Silkscreen etc
    #### Copied from conn_jst_PHD_vertical.py
    ####
    
    #calculate fp dimensions
    pitch = 2.0
    A = (n_positions - 1) * pitch
    B = A + 4.0   # Total width
    
    body_size = Size(B, 5.3)

    #draw the component outline
    x1 = -B/2.0
    x2 = B/2.0
    y2 = body_size.y/2
    y1 = -y2
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}
    
    #wall thickness
    t_short = 0.75 #short side (fixed at 5mm)
    t_long = 0.5 #long side, from CNJM datasheet

    ########################### CrtYd #################################
    # Courtyard from conn_jst_PHD_vertical.py, modified to include pads
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'] - pad_size.y + 0.25, configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'] + pad_size.y - 0.25, configuration['courtyard_grid'])
    
    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    #draw silk polarity lines
    kicad_mod.append(RectLine(start=[x1+t_short,y1+t_long],end=[x2-t_short,y2-t_long],layer='F.Fab',width=configuration['fab_line_width']))

    #offset off
    off = configuration['silk_fab_offset']

    #draw silk keying/polarity marks measured from 3D model on JST's site
    # from bottom (pin 2 row) of connector, notches are 1.6mm up and 0.8mm wide
    # NOTE: Drawn on Fab layer as this is a SMD part family
    kicad_mod.append(Line(start=[x1,y2-2.4],end=[x1+t_short,y2-2.4],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2,y2-2.4],end=[x2-t_short,y2-2.4],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x1,y2-1.6],end=[x1+t_short,y2-1.6],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2,y2-1.6],end=[x2-t_short,y2-1.6],layer='F.Fab',width=configuration['fab_line_width']))
    # from sides, inner edge of notches are 3.42mm inside and 0.94mm wide at the top (pin 1 row) and 1.50mm wide at the bottom (pin 2 row)
    kicad_mod.append(Line(start=[x1+3.42,y1],end=[x1+3.42,y1+t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x1+2.48,y1],end=[x1+2.48,y1+t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2-3.42,y1],end=[x2-3.42,y1+t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2-2.48,y1],end=[x2-2.48,y1+t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x1+3.42,y2],end=[x1+3.42,y2-t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x1+1.92,y2],end=[x1+1.92,y2-t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2-3.42,y2],end=[x2-3.42,y2-t_long],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[x2-1.92,y2],end=[x2-1.92,y2-t_long],layer='F.Fab',width=configuration['fab_line_width']))
    
    # Draw silk orientation lines outside the part
    indicator_xofs = 0.35
    kicad_mod.append(Line(start=[x1-indicator_xofs,y2-2.4],end=[x1-indicator_xofs,y2-1.6],layer='F.SilkS',width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[x2+indicator_xofs,y2-2.4],end=[x2+indicator_xofs,y2-1.6],layer='F.SilkS',width=configuration['silk_line_width']))

    x1 -= off
    y1 -= off
    x2 += off
    y2 += off

    #draw silk outline
    # Vertical lines are the same as in a [x1,y1] to [x2,y2] rectangle
    # but the horizontal lines need to be broken at the pads
    kicad_mod.append(Line(start=[x1,y1],end=[x1,y2],width=configuration['silk_line_width'],layer='F.SilkS'))
    kicad_mod.append(Line(start=[x2,y1],end=[x2,y2],width=configuration['silk_line_width'],layer='F.SilkS'))
    
    # Create lines from corner to leftmost pad (1)
    pad_silk_xofs = pad_size.x/2 + 0.3 # from pad centerpoint. 0.25 is clearance
    left_silk_end_x = x_pad_position(1, n_positions) - pad_silk_xofs
    
    kicad_mod.append(Line(start=[x1, y1], end=[left_silk_end_x, y1], width=configuration['silk_line_width'], layer='F.SilkS'))
    kicad_mod.append(Line(start=[x1, y2], end=[left_silk_end_x, y2], width=configuration['silk_line_width'], layer='F.SilkS'))
    
    # Right side is just symmetrical (but we use the rightmost pad's X coords)
    right_silk_end_x = x_pad_position(n_positions*2, n_positions) + pad_silk_xofs
    
    kicad_mod.append(Line(start=[x2, y1], end=[right_silk_end_x, y1], width=configuration['silk_line_width'], layer='F.SilkS'))
    kicad_mod.append(Line(start=[x2, y2], end=[right_silk_end_x, y2], width=configuration['silk_line_width'], layer='F.SilkS'))
    
    # Add a short line between every two pads
    for i in range(1, n_positions*2+1):
        # Ignore every 2nd pad, since we draw both top and bottom at once
        if i % 2 == 0:
            continue
        # Same row, different columns => i+2
        start_x = x_pad_position(i, n_positions) + pad_silk_xofs
        stop_x = x_pad_position(i+2, n_positions) - pad_silk_xofs
        # Add top and bottom lines
        kicad_mod.append(Line(start=[start_x, y1], end=[stop_x, y1], width=configuration['silk_line_width'], layer='F.SilkS'))
        kicad_mod.append(Line(start=[start_x, y2], end=[stop_x, y2], width=configuration['silk_line_width'], layer='F.SilkS'))
        
    
    ########### Marker ############
    # Pin 1 marker arrow
    
    marker_xofs = 1.0
    marker_x_coord = x_pad_position(1, n_positions) - marker_xofs
    marker_y_coord = y_pad_position(1, n_positions)
    
    marker_size = 0.4
    marker = [
        {'x': marker_x_coord,'y': marker_y_coord},
        {'x': marker_x_coord-2*marker_size,'y': marker_y_coord+marker_size},
        {'x': marker_x_coord-2*marker_size,'y': marker_y_coord-marker_size},
        {'x': marker_x_coord,'y': marker_y_coord}
    ]

    kicad_mod.append(PolygonLine(polygon=marker, width=configuration['silk_line_width'], layer='F.SilkS'))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=fp_name, text_y_inside_position='center')
    
    model3d_path_prefix = configuration.get('3d_model_prefix','${KICAD8_3DMODEL_DIR}/')


    lib_name = configuration['lib_name_specific_function_format_string'].format(category=lib_name_category)
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=fp_name)
    
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=fp_name)
    kicad_mod.append(Model(filename=model_name))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for n_positions in pinrange:
        generate_one_footprint(n_positions=n_positions, variant=None, configuration=configuration)
