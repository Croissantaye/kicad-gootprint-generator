#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is derived from a cadquery script for generating PDIP models in X3D format
#
# from https://bitbucket.org/hyOzd/freecad-macros
# author hyOzd
#
# Dimensions are from Microchips Packaging Specification document:
# DS00000049BY. Body drawing is the same as QFP generator#
#
## Requirements
## CadQuery 2.1 commit e00ac83f98354b9d55e6c57b9bb471cdf73d0e96 or newer
## https://github.com/CadQuery/cadquery
#
## To run the script just do: ./generator.py --output_dir [output_directory]
## e.g. ./generator.py --output_dir /tmp
#
#* These are cadquery tools to export                                       *
#* generated models in STEP & VRML format.                                  *
#*                                                                          *
#* cadquery script for generating QFP/SOIC/SSOP/TSSOP models in STEP AP214  *
#* Copyright (c) 2016                                                       *
#*     Rene Poeschl https://github.com/poeschlr                             *
#* Copyright (c) 2022                                                       *
#*     Update 2022                                                          *
#*     jmwright (https://github.com/jmwright)                               *
#*     Work sponsored by KiCAD Services Corporation                         *
#*          (https://www.kipro-pcb.com/)                                    *
#*                                                                          *
#* All trademarks within this guide belong to their legitimate owners.      *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU General Public License (GPL)             *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#****************************************************************************

__title__ = "make 4UCON 17809 series connector 3D models exported to STEP and VRML"
__author__ = "scripts: maurice and hyOzd; models: see cq_model files; update: jmwright"
__Comment__ = '''This generator loads cadquery model scripts and generates step/wrl files for the official kicad library.'''

___ver___ = "2.0.0"

import os

import cadquery as cq
from _tools import shaderColors, parameters, cq_color_correct
from _tools import cq_globals
from _tools.parameters import load_aux_parameters
from exportVRML.export_part_to_VRML import export_VRML

from .cq_models.conn_4ucon_17809 import generate_part

def make_models(model_to_build=None, output_dir_prefix=None, enable_vrml=True):
    """
    Main entry point into this generator.
    """
    models = []

    all_params = parameters.load_parameters("4UCON_17809")

    if all_params == None:
        print("ERROR: Model parameters must be provided.")
        return

    # Handle the case where no model has been passed
    if model_to_build is None:
        print("No variant name is given! building: {0}".format(model_to_build))

        model_to_build = all_params.keys()[0]

    # Handle being able to generate all models or just one
    if model_to_build == "all":
        models = all_params
    else:
        models = { model_to_build: all_params[model_to_build] }
    # Step through the selected models
    for model in models:
        if output_dir_prefix == None:
            print("ERROR: An output directory must be provided.")
            return
        else:
            # Load the global parameters
            globals = load_aux_parameters(__file__, "global_parameters.yaml")

            # Construct the final output directory
            output_dir = os.path.join(output_dir_prefix, globals['globals']['destination_dir'])

        # Safety check to make sure the selected model is valid
        if not model in all_params.keys():
            print("Parameters for %s doesn't exist in 'all_params', skipping." % model)
            continue

        # Load the appropriate colors
        body_color = shaderColors.named_colors[globals['globals']["body_color_key"]].getDiffuseFloat()
        pin_color = shaderColors.named_colors[globals['globals']["pin_color_key"]].getDiffuseFloat()
        contact_color = shaderColors.named_colors[globals['globals']["contact_color_key"]].getDiffuseFloat()

        # Make the parts of the model
        (pins, body, contacts) = generate_part(all_params[model], globals['globals'])
        # body = body.rotate((0, 0, 0), (0, 0, 1), all_params[model]['rotation'])
        # pins = pins.rotate((0, 0, 0), (0, 0, 1), all_params[model]['rotation'])
        # contacts = contacts.rotate((0, 0, 0), (0, 0, 1), all_params[model]['rotation'])

        # Used to wrap all the parts into an assembly
        component = cq.Assembly()

        # Add the parts to the assembly
        component.add(body, color=cq_color_correct.Color(body_color[0], body_color[1], body_color[2]))
        component.add(pins, color=cq_color_correct.Color(pin_color[0], pin_color[1], pin_color[2]))
        component.add(contacts, color=cq_color_correct.Color(contact_color[0], contact_color[1], contact_color[2]))

        # Create the output directory if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Assemble the filename
        file_name = all_params[model]['file_name']

        # Export the assembly to STEP
        component.save(os.path.join(output_dir, file_name + ".step"), cq.exporters.ExportTypes.STEP, write_pcurves=False)

        # Update license author info
        from _tools import add_license
        add_license.STR_int_licAuthor = "Ray Benitez"
        add_license.STR_int_licEmail = "hackscribble@outlook.com"

        # Export the assembly to VRML
        if enable_vrml:
            export_VRML(os.path.join(output_dir, file_name + ".wrl"), [body, pins, contacts], [globals['globals']["body_color_key"], globals['globals']["pin_color_key"], globals['globals']["contact_color_key"]])

        # Update the license
        add_license.addLicenseToStep(output_dir, file_name + ".step",
                                        add_license.LIST_int_license,
                                        add_license.STR_int_licAuthor,
                                        add_license.STR_int_licEmail,
                                        add_license.STR_int_licOrgSys,
                                        add_license.STR_int_licPreProc)
