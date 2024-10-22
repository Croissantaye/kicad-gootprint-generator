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
from math import sqrt

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "XAD"
manufacturer = 'JST'
orientation = 'V'
number_of_rows = 2
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eXAD1.pdf'

pitch = 2.5

#XAD : there are minor esthetic differences between 8-16pins and 18-40 pins, no dimensional change to footprint
pin_range=[*range(4,18+1),20] #number of pins in each row. No 38-pin version as of 2020
row_pitch = 2.5
drill = 0.95 # 0.9 +0.1/-0 -> 0.95+/-0.05
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15
mh_drill = 1.15	#(1.1 -0/+0.1)


variant_parameters = {
    'N-A': {
        'boss':True,
        'descr_str':', with boss'
        },
    'N': {
        'boss':False,
        'descr_str':''
        }
}
def generate_one_footprint(pins, variant, configuration):
    mpn = "B{n:02}B-XADSS-{suff}".format(n=pins*number_of_rows,suff=variant)
    boss = variant_parameters[variant]['boss']

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(series, mpn, datasheet))

    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation])
    if boss:
        tags += ' boss'
    kicad_mod.setTags(tags)


    #calculate fp dimensions
    A = (pins - 1) * pitch
    B = A + 7.5
    body_width = 10.1

    #draw the component outline
    x1 = A/2.0 - B/2.0
    x2 = x1 + B
    y2 = (body_width + row_pitch)/2	#validated from CAD : pins are centered in plastic body
    y1 = y2 - body_width
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}

    #draw simple outline on F.Fab layer
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=configuration['fab_line_width']))

    ########################### CrtYd #################################
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))


    ########################### Silkscreen ###########################
    #shroud wall thickness (from 3D CAD)
    t_short = 1.95 #short side
    t_long = 1.2 #long side (A/B dimension)

    silk_inner_left = x1+t_short
    silk_inner_right = x2-t_short
    silk_inner_top = y1+t_long
    silk_inner_bot = y2-t_long

    if boss:
        kicad_mod.append(PolygoneLine(polygone=[
            {'x': silk_inner_left+1,'y': silk_inner_top},
            {'x': silk_inner_right,'y': silk_inner_top},
            {'x': silk_inner_right,'y': silk_inner_bot},
            {'x': silk_inner_left,'y': silk_inner_bot},
            {'x': silk_inner_left,'y': -0.8},
        ], width=configuration['silk_line_width'], layer="F.SilkS"))
    else:
        kicad_mod.append(RectLine(start=[silk_inner_left,silk_inner_top],end=[silk_inner_right,silk_inner_bot],layer='F.SilkS',width=configuration['silk_line_width']))

    #offset off
    off = configuration['silk_fab_offset']

    #draw silk keying/polarity marks measured from 3D model on JST's site
    #short side : one deep cut line up with odd row (y=0), 1.1mm wide
    sidecut = 1.1/2
    kicad_mod.append(Line(start=[x1-off,sidecut],end=[x1+t_short,sidecut],layer='F.SilkS',width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[x2+off,sidecut],end=[x2-t_short,sidecut],layer='F.SilkS',width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[x1-off,-sidecut],end=[x1+t_short,-sidecut],layer='F.SilkS',width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[x2+off,-sidecut],end=[x2-t_short,-sidecut],layer='F.SilkS',width=configuration['silk_line_width']))

    # long side: non-latch side= one long indent; latch side=one or two recesses for lock. Guessed dims
    if pins <= 8:
        #8 to 16 pins: indent starts at second pin from ends
        kicad_mod.append(Line(start=[x1+(B+A)/2 - pitch,y1-off],end=[x1+(B+A)/2 - pitch,y1+t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B-A)/2 + pitch,y1-off],end=[x1+(B-A)/2 + pitch,y1+t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        #and one lock recess
        lock_width = 7.5    #not sure if constant for all pincounts, whatever
        kicad_mod.append(Line(start=[x1+(B+lock_width)/2,y2+off],end=[x1+(B+lock_width)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B-lock_width)/2,y2+off],end=[x1+(B-lock_width)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))
    else:
        kicad_mod.append(Line(start=[x1+(B+A)/2,y1-off],end=[x1+(B+A)/2,y1+t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B-A)/2,y1-off],end=[x1+(B-A)/2,y1+t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        # and 2 lock recesses, 2.1mm separation, 12.9mm total width
        lock_sep = 2.1
        locks_width = 12.9
        kicad_mod.append(Line(start=[x1+(B+lock_sep)/2,y2+off],end=[x1+(B+lock_sep)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B-lock_sep)/2,y2+off],end=[x1+(B-lock_sep)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B+locks_width)/2,y2+off],end=[x1+(B+locks_width)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x1+(B-locks_width)/2,y2+off],end=[x1+(B-locks_width)/2,y2-t_long],layer='F.SilkS',width=configuration['silk_line_width']))

    x1 -= off
    y1 -= off
    x2 += off
    y2 += off

    #draw silk outline
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],width=configuration['silk_line_width'],layer='F.SilkS'))

    #add p1 marker
    px = x1 - 0.2
    m = 0.3

    marker = [
    {'x': px,'y': 0},
    {'x': px-2*m,'y': m},
    {'x': px-2*m,'y': -m},
    {'x': px,'y': 0}
    ]

    kicad_mod.append(PolygoneLine(polygone=marker,width=configuration['silk_line_width'],layer='F.SilkS'))
    sl = 0.5
    marker =[
        {'x': body_edge['left'], 'y': sl},
        {'x': body_edge['left'] + (2*sl)/sqrt(2) , 'y': 0},
        {'x': body_edge['left'] , 'y': -sl}
    ]
    kicad_mod.append(PolygoneLine(polygone=marker,layer='F.Fab',width=configuration['fab_line_width']))

    #generate the pads (row 1)

    size = [pitch - pad_to_pad_clearance, row_pitch - pad_to_pad_clearance]
    if size[0] - drill < 2*min_annular_ring:
        size[0] = drill + 2*min_annular_ring
    if size[0] - drill > 2*pad_copper_y_solder_length:
        size[0] = drill + 2*pad_copper_y_solder_length

    if size[1] - drill < 2*min_annular_ring:
        size[1] = drill + 2*min_annular_ring
    if size[1] - drill > 2*pad_copper_y_solder_length:
        size[1] = drill + 2*pad_copper_y_solder_length

    if size[0] == size[1]:
        pad_shape = Pad.SHAPE_CIRCLE
    else:
        pad_shape = Pad.SHAPE_OVAL

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT


    for row_idx in range(2):
        kicad_mod.append(PadArray(
            pincount=pins, x_spacing=pitch,
            type=Pad.TYPE_THT, shape=pad_shape,
            start=[0, row_idx*row_pitch], initial=row_idx+1, increment=2,
            size=size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    #add mounting hole
    if boss:
        kicad_mod.append(Pad(at={'x': -1.7, 'y': -1.8}, type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH,
            drill=mh_drill, size=mh_drill))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

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
    parser.add_argument('--kicad4_compatible', action='store_true', help='Create footprints kicad 4 compatible')
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

    configuration['kicad4_compatible'] = args.kicad4_compatible

    for variant in variant_parameters:
        for pins in pin_range:
            generate_one_footprint(pins, variant, configuration)
