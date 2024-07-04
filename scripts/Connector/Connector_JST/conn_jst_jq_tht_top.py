#!/usr/bin/env python3

'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
'''

import sys
import os

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

from itertools import chain

series = "JQ"
manufacturer = 'JST'
orientation = 'V'
number_of_rows = 1
datasheet = 'https://www.jst-mfg.com/product/pdf/eng/eJQ.pdf'

pitch = 2.50
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

#FP name strings
part_base = "{n:02d}JQ-BT"  # JST part number format string

variant_params = {
    None:{
        'back_protrusion': False,
        'pin_range': chain(range(3,14), [15]) # 14 not available according to datasheet
    },
}

fab_first_marker_w = 1.25
pin1_marker_linelen = 1.25
fab_first_marker_h = 1
fab_pin1_marker_type = 2
pin1_marker_offset = 0.3

#FP description and tags

def generate_one_footprint(pins, variant, configuration):
    #calculate fp dimensions
    A = (pins - 1) * pitch
    B = A + 4.9

    #connector thickness
    T = 6

    #corners
    x1 = -2.45
    x2 = x1 + B

 
    x_mid = (x1 + x2) / 2

    y1 = -3.3 # Y coordinate of the pin row, relative to the F.Fab corner (6.0 - smaller datasheet value)
    y2 = y1 + T

    #generate the name
    mpn = part_base.format(n=pins, variant=variant)
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name, FootprintType.THT)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(
        series, mpn, datasheet))

    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation])
    #set the FP tags
    kicad_mod.setTags(tags)

    #draw simple outline on F.Fab layer
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab', width=configuration['fab_line_width']))

    # set general values
    #kicad_mod.append(Property(name=Property.REFERENCE, text='REF**', at=[x_mid,-3.5], layer='F.SilkS'))

    drill = 0.95 # Datasheet: 0.9 +0.1/-0 => center tolerance 0.95 +/- 0.05

    pad_size = [pitch - pad_to_pad_clearance, drill + 2*pad_copper_y_solder_length]
    if pad_size[0] - drill < 2*min_annular_ring:
        pad_size[0] = drill + 2*min_annular_ring

    #generate the pads
    ############################# Pads ##################################
    # kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
    #                     at=[0, 0], size=pad_size,
    #                     drill=drill, layers=Pad.LAYERS_THT))

    optional_pad_params = {}
    optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(initial=1, start=[0, 0],
        x_spacing=pitch, pincount=pins,
        size=pad_size, drill=drill,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    out = RectLine(start=[x1,y1], end=[x2,y2], offset=configuration['silk_fab_offset'],
        layer='F.SilkS', width=configuration['silk_line_width'])
    kicad_mod.append(out)
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}

    #draw the courtyard
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    #draw the connector outline


    if fab_pin1_marker_type == 2:
        fab_marker_left = -fab_first_marker_w/2.0
        fab_marker_bottom = y1 + fab_first_marker_h
        poly_fab_marker = [
            {'x':fab_marker_left, 'y':y1},
            {'x':0, 'y':fab_marker_bottom},
            {'x':fab_marker_left + fab_first_marker_w, 'y':y1}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_fab_marker, layer='F.Fab', width=configuration['fab_line_width']))

    #wall thickness w
    wall_thickness = 1.2 # measured from 3d model

    #gap size g
    g = 1.0 # measured from 3d model

    off = 0.1

    x1 -= off
    y1 -= off

    x2 += off
    y2 += off
    
    # NOTE: Adjusted so that gap start matches wall thickness for JQ connector
    gap_x_offset = -0.7 # Relative to the X coord of the first/last pin. Inverted for last pin.

    #draw the center tab
    kicad_mod.append(RectLine(start=[g/2+gap_x_offset,y1], end=[A-g/2-gap_x_offset,y1+wall_thickness], layer='F.SilkS', width=configuration['silk_line_width']))

    #add vertical lines signifying the part of the plastic contacting the PCB
    line = [
        {'x': x1+wall_thickness,'y': y1},
        {'x': x1+wall_thickness,'y': y2},
    ]
    kicad_mod.append(PolygonLine(polygon=line, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygonLine(polygon=line, x_mirror=A / 2, layer='F.SilkS', width=configuration['silk_line_width']))

    # plastic part cutout on the south side
    south_side_gap_size = 1.0 # mm, measured from 3d model
    kicad_mod.append(PolygonLine(polygon=[
        # Between the two vertical lines
        {'x': x1+wall_thickness, 'y': y2-south_side_gap_size},
        {'x': x2-wall_thickness, 'y': y2-south_side_gap_size},
    ], layer='F.SilkS', width=configuration['silk_line_width']))

    #pin-1 marker
    y =  -2.75
    m = 0.3

    poly_pin1_marker = [
        {'x':x1-pin1_marker_offset+pin1_marker_linelen, 'y':y1-pin1_marker_offset},
        {'x':x1-pin1_marker_offset, 'y':y1-pin1_marker_offset},
        {'x':x1-pin1_marker_offset, 'y':y1-pin1_marker_offset+pin1_marker_linelen}
    ]
    if fab_pin1_marker_type == 2:
        kicad_mod.append(PolygonLine(polygon=poly_pin1_marker, layer='F.SilkS', width=configuration['silk_line_width']))
    if fab_pin1_marker_type == 3:
        kicad_mod.append(PolygonLine(polygon=poly_pin1_marker, layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygonLine(polygon=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))

    pin = [
    {'x': 0,'y': y},
    {'x': -m,'y': y-2*m},
    {'x': m,'y': y-2*m},
    {'x': 0,'y': y},
    ]


    if fab_pin1_marker_type == 1:
        kicad_mod.append(PolygonLine(polygon=pin, layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygonLine(polygon=pin, layer='F.Fab', width=configuration['fab_line_width']))

    ######################### Text Fields ###############################
    text_center_y = 'bottom'
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position=text_center_y)


    model3d_path_prefix = configuration.get('3d_model_prefix','${KICAD8_3DMODEL_DIR}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

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

    for variant in variant_params:
        for pincount in variant_params[variant]['pin_range']:
            generate_one_footprint(pincount, variant, configuration)
