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

def generate_one_footprint(n_positions: int, variant: str, configuration):
    fp_name = f'CNJM_CNJMA_2006WV-S-2x{n_positions:02d}_P2.0mm'

    print("%s" % fp_name)
    kicad_mod = Footprint(fp_name, FootprintType.UNSPECIFIED)

    description = f"Dual-row 2.0mm SMD connector, 2x{n_positions:02d} contacts, 6.2mm height"
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
    
    # Create Pads. NOTE: For n_positions=3, we create 6 pads!
    for i in range(1, (n_positions*2)+1):
        x = x_pad_position(i, n_positions)
        y = y_pad_position(i, n_positions)
        print(f"Pad {i}: {x}, {y}")
        kicad_mod.append(Pad(number=i, type=Pad.TYPE_CONNECT, shape=Pad.SHAPE_ROUNDRECT,
            at=[x, y], size=list(pad_size), layers=Pad.LAYERS_CONNECT_FRONT)
        )

    ## create pads (and some numbers on silk for orientation)
    #fontsize = 0.75
    #start = -V[positions] / 2
    #for i in range(0, positions):
    #    off = 4.0 - pad_pitch if W[positions] and i > W[positions] else 0.0
    #    for idx, layer in enumerate([Pad.LAYERS_CONNECT_FRONT, Pad.LAYERS_CONNECT_BACK]):
    #        kicad_mod.append(Pad(number=2 * i + idx + 1, type=Pad.TYPE_CONNECT, shape=Pad.SHAPE_RECT,
    #                             at=[start + i * pad_pitch + off, bot - 3.8 + pad_size[1]/2], size=pad_size, layers=layer))
    #    if (i in [0, positions - 1]) or (W[positions] and (i - W[positions]) in [0, 1]):
    #        align = 0 if (i == 0 or i - 1 == W[positions]) else 1
    #        for idx, layer in enumerate(['F.SilkS', 'B.SilkS']):
    #            lbl = '%d' % (2 * i + idx + 1)
    #            kicad_mod.append(Text(text=lbl, at=[start + i * pad_pitch + off + (-1)**align * fontsize * (len(lbl) - 1) / 2, bot - 3.8 - fontsize], layer=layer, mirror=idx, size=[fontsize, fontsize]))

    ## create some useful additional information on User.Comments layer
    # kicad_mod.append(Text(text="Chamfer 30 degree 0.45 mm", at=[0, bot - 0.44], layer='Cmts.User', size=[fontsize, fontsize]))
    # if ('-BL' in option):
    #     mate_distance = zip([1.8], ['ref'])
    # else:
    #     mate_distance = zip([2.05, 3.69], ['min', 'max'])
    # for dist, name in mate_distance: # see https://suddendocs.samtec.com/prints/hsec8%20mated%20document-mkt.pdf Table 1
    #     kicad_mod.append(Line(start=[body_edge['left'], body_edge['bottom'] + dist], end=[body_edge['left'] + 2.5, body_edge['bottom'] + dist], width=configuration['fab_line_width'], layer='Cmts.User'))
    #     kicad_mod.append(Text(text="mated PCB distance: %.2f mm (%s)" % (dist, name), at=[left + 3, bot + dist], layer='Cmts.User', size=[fontsize, fontsize], justify='left'))

    # TODO: add keepout area on inner layers near chamfered edges
    # this requires to create a new Zone node in the KicadModTree to add something like:
    #
    #  kicad_mod.append(Zone(nodes=[[-Y[positions] / 2, bot - 1.0], [Y[positions] / 2, bot - 1.0], [Y[positions] / 2, bot], [-Y[positions] / 2, bot]], layer='Inner Layers', etc etc))
    #

    ######################### Text Fields ###############################
    #addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
    #              courtyard={'top':cy1, 'bottom':cy2}, fp_name=fp_name, text_y_inside_position=-2.54)

    lib_name = configuration['lib_name_specific_function_format_string'].format(category=lib_name_category)
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=fp_name)

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
