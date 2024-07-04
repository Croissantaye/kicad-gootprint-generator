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

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from itertools import chain
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "JQ"
manufacturer = 'JST'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.jst-mfg.com/product/pdf/eng/eJQ.pdf'


pitch = 2.50
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

#FP name strings
part_base = "{n:02d}JQ-ST"  # JST part number format string

fab_pin1_marker_type = 2
fab_first_marker_w = 1.25
fab_first_marker_h = 1

#FP description and tags

variant_params = {
    None:{
        'back_protrusion': False,
        'pin_range': chain(range(3,14), [15]) # 14 not available according to datasheet
    },
}


def generate_one_footprint(pins, variant, configuration):
    V = 7.3
    #calculate fp dimensions
    A = (pins - 1) * pitch
    B = A + 5.0

    #Thickness of connector
    T = 9.5

    #corners
    x1 = -2.45
    x2 = x1 + B

    x_mid = (x1 + x2) / 2

    y2 = V
    y1= y2 - T


    #y at which the plastic tabs end
    y3 = y2 - 7

    #generate the name
    mpn = part_base.format(n=pins, variant=variant)
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name, FootprintType.THT)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(series, mpn, datasheet))

    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))


    if pins == 2:
        drill = 1.0
    else:
        drill = 0.95

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
        x_spacing=pitch, pincount=pincount,
        size=pad_size, drill=drill,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    #draw the courtyard
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    #offset the outline around the connector
    off = configuration['silk_fab_offset']

    xo1 = x1 - off
    yo1 = y1 - off

    xo2 = x2 + off
    yo2 = y2 + off

    #wall thickness of the outline
    wall = 1.2 # measured from 3d model
    
    # Width of the south part of the connector (socket only)
    socket_inset = 0.9 # measured from 3d model
    
    # Y end of socket part
    y_socket_end = yo1 + 2.2 + 2.6 # values from datasheet

    #draw the outline of the connector
    f_silk_outline = [
        {'x': x_mid,'y': yo2},
        {'x': xo1+socket_inset,'y': yo2},
        {'x': xo1+socket_inset,'y': y_socket_end + off},
        {'x': xo1,'y': y_socket_end + off},
        {'x': xo1,'y': yo1},
        {'x': xo1+wall+2*off,'y': yo1},
        {'x': xo1+wall+2*off,'y': y3 - off},
        {'x': A/2,'y': y3 - off},
        #{'x': -1.1,'y': y3 + off}
    ]
    kicad_mod.append(PolygonLine(polygon=f_silk_outline, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygonLine(polygon=f_silk_outline, x_mirror=x_mid, layer='F.SilkS', width=configuration['silk_line_width']))

    f_fab_outline = [
        {'x': x_mid,'y': y2},
        {'x': x1+socket_inset,'y': y2},
        {'x': x1+socket_inset,'y': y_socket_end},
        {'x': x1,'y': y_socket_end},
        {'x': x1,'y': y1},
        {'x': x1+wall,'y': y1},
        {'x': x1+wall,'y': y3},
        {'x': A/2,'y': y3},
        #{'x': -1.1,'y': y3 + off}
    ]
    kicad_mod.append(PolygonLine(polygon=f_fab_outline, layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygonLine(polygon=f_fab_outline, x_mirror=x_mid, layer='F.Fab', width=configuration['fab_line_width']))

    # Add "PCB edge" line & text
    pcb_edge_y = 2.6 # from datasheet. NOTE: Need to use receptacle variant here.
    kicad_mod.append(PolygonLine(polygon=[
        {'x': x1 - 0.5, 'y': pcb_edge_y},
        {'x': x2 + 0.5, 'y': pcb_edge_y},
    ], layer='Cmts.User', width=configuration['fab_line_width']))
    kicad_mod.append(Text(text='max PCB edge', at=[x1 + A/2 + 2.5, pcb_edge_y+1], size=[1.0, 1.0], layer='Cmts.User'))

    #draw line between each two pins
    for i in range(pins-1):
        x = i * pitch + 0.5*pitch
        kicad_mod.append(PolygonLine(polygon=[
            {'x': x, 'y':y3-off},
            {'x': x, 'y':y2+off},
        ], layer='F.SilkS', width=configuration['silk_line_width']))

    #add pin-1 designator
    px = 0
    py = -1.5
    m = 0.3

    pin1 = [
    {'x': px,'y': py},
    {'x': px-m,'y': py-2*m},
    {'x': px+m,'y': py-2*m},
    {'x': px,'y': py},
    ]

    kicad_mod.append(PolygonLine(polygon=pin1, layer='F.SilkS', width=configuration['silk_line_width']))
    if fab_pin1_marker_type == 1:
        kicad_mod.append(PolygonLine(polygon=pin1, layer='F.Fab', width=configuration['fab_line_width']))

    if fab_pin1_marker_type == 2:
        fab_marker_left = -fab_first_marker_w/2.0
        fab_marker_bottom = y3 - fab_first_marker_h
        poly_fab_marker = [
            {'x':fab_marker_left, 'y':y3},
            {'x':0, 'y':fab_marker_bottom},
            {'x':fab_marker_left + fab_first_marker_w, 'y':y3}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_fab_marker, layer='F.Fab', width=configuration['fab_line_width']))

    ######################### Text Fields ###############################
    text_center_y = 'center'
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}
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
