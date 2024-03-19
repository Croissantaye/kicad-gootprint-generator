# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
# (C) 2018 by Rene Poeschl, github @poeschlr

from __future__ import division

import unittest
import pytest

from KicadModTree import *

# Trick pycodestyle into not assuming tab indents
if False:
    pass

RESULT_ROUNDRECT_FP = """(footprint "roundrect_pad"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "3" smd roundrect
		(at 5 0 45)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(roundrect_rratio 0.1)
	)
	(pad "2" smd roundrect
		(at -5 0)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(roundrect_rratio 0.5)
	)
	(pad "1" smd rect
		(at 0 0)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
)"""  # NOQA: W191

RESULT_ROUNDRECT_FP2 = """(footprint "roundrect_pad2"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "3" smd roundrect
		(at 5 0 45)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(roundrect_rratio 0.25)
	)
	(pad "2" smd roundrect
		(at -5 0)
		(size 1 2)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(roundrect_rratio 0.25)
	)
	(pad "1" smd roundrect
		(at 0 0)
		(size 2 4)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(roundrect_rratio 0.125)
	)
)"""  # NOQA: W191

RESULT_SIMPLE_POLYGON_PAD = """(footprint "polygon_pad"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 0)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -1 -1)
					(xy 2 -1)
					(xy 1 1)
					(xy -1 2)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_SIMPLE_OTHER_CUSTOM_PAD = """(footprint "custom_pad_other"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 0)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_arc
				(start -1 0.5)
				(mid -1.5 0)
				(end -1 -0.5)
				(width 0.15)
			)
			(gr_line
				(start -1 -0.5)
				(end 1.25 -0.5)
				(width 0.15)
			)
			(gr_line
				(start 1.25 -0.5)
				(end 1.25 0.5)
				(width 0.15)
			)
			(gr_line
				(start 1.25 0.5)
				(end -1 0.5)
				(width 0.15)
			)
		)
	)
	(pad "2" smd custom
		(at 0 3)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_arc
				(start -1 0.5)
				(mid -1.5 0)
				(end -1 -0.5)
				(width 0.15)
			)
			(gr_line
				(start -1 -0.5)
				(end 1.25 -0.5)
				(width 0.15)
			)
			(gr_line
				(start 1.25 -0.5)
				(end 1.25 0.5)
				(width 0.15)
			)
			(gr_line
				(start 1.25 0.5)
				(end -1 0.5)
				(width 0.15)
			)
		)
	)
	(pad "3" smd custom
		(at 0 -3)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_circle
				(center 0.5 0.5)
				(end 1 0.5)
				(width 0.15)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CUT_POLYGON = """(footprint "cut_polygon"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 0)
		(size 0.5 0.5)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -2 -2)
					(xy 2 -2)
					(xy 2 2)
					(xy 1 1)
					(xy 1 0)
					(xy 0 0)
					(xy 0 1)
					(xy 1 1)
					(xy 2 2)
					(xy -2 2)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CHAMFERED_PAD = """(footprint "chamfered_pad"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 0)
		(size 0.764298 0.764298)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.166667)
					(xy -0.166667 -0.5)
					(xy 0.166667 -0.5)
					(xy 0.5 -0.166667)
					(xy 0.5 0.166667)
					(xy 0.166667 0.5)
					(xy -0.166667 0.5)
					(xy -0.5 0.166667)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 2 2)
		(size 1.357538 1.357538)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -1.05 -0.5)
					(xy -0.55 -1.55)
					(xy 0.55 -1.55)
					(xy 1.05 -0.5)
					(xy 1.05 0.5)
					(xy 0.55 1.55)
					(xy -0.55 1.55)
					(xy -1.05 0.5)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CHAMFERED_PAD_AVOID_CIRCLE = """(footprint "avoid_circle"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(fp_circle
		(center 3 3.5)
		(end 3.3 3.5)
		(stroke
			(width 0.01)
			(type solid)
		)
		(layer "F.SilkS")
	)
	(pad "1" smd custom
		(at 2 2.5)
		(size 1.445 1.445)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.875 -0.693665)
					(xy -0.443665 -1.125)
					(xy 0.443665 -1.125)
					(xy 0.875 -0.693665)
					(xy 0.875 0.693665)
					(xy 0.443665 1.125)
					(xy -0.443665 1.125)
					(xy -0.875 0.693665)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CHAMFERED_PAD_GRID = """(footprint "chamfered_grid"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 -1.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.75)
					(xy -0.25 -1)
					(xy 0.5 -1)
					(xy 0.5 1)
					(xy -0.25 1)
					(xy -0.5 0.75)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 0 1.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.75)
					(xy -0.25 -1)
					(xy 0.5 -1)
					(xy 0.5 1)
					(xy -0.25 1)
					(xy -0.5 0.75)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 0 3.75)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.75)
					(xy -0.25 -1)
					(xy 0.5 -1)
					(xy 0.5 1)
					(xy -0.25 1)
					(xy -0.5 0.75)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 0 6.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.75)
					(xy -0.25 -1)
					(xy 0.5 -1)
					(xy 0.5 1)
					(xy -0.25 1)
					(xy -0.5 0.75)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 1.5 -1.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.75)
					(xy -0.25 -1)
					(xy 0.25 -1)
					(xy 0.5 -0.75)
					(xy 0.5 1)
					(xy -0.5 1)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd rect
		(at 1.5 1.25)
		(size 1 2)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at 1.5 3.75)
		(size 1 2)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd custom
		(at 1.5 6.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -1)
					(xy 0.5 -1)
					(xy 0.5 0.75)
					(xy 0.25 1)
					(xy -0.25 1)
					(xy -0.5 0.75)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 3 -1.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -1)
					(xy 0.25 -1)
					(xy 0.5 -0.75)
					(xy 0.5 0.75)
					(xy 0.25 1)
					(xy -0.5 1)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 3 1.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -1)
					(xy 0.25 -1)
					(xy 0.5 -0.75)
					(xy 0.5 0.75)
					(xy 0.25 1)
					(xy -0.5 1)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 3 3.75)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -1)
					(xy 0.25 -1)
					(xy 0.5 -0.75)
					(xy 0.5 0.75)
					(xy 0.25 1)
					(xy -0.5 1)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 3 6.25)
		(size 0.823223 0.823223)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -1)
					(xy 0.25 -1)
					(xy 0.5 -0.75)
					(xy 0.5 0.75)
					(xy 0.25 1)
					(xy -0.5 1)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CHAMFERED_PAD_GRID_AVOID_CIRCLE = """(footprint "chamfered_grid_corner_only"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(fp_circle
		(center 2 2.5)
		(end 2.2 2.5)
		(stroke
			(width 0.01)
			(type solid)
		)
		(layer "F.SilkS")
	)
	(pad "1" smd custom
		(at -1.4 -2.1)
		(size 0.795 0.795)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.210086)
					(xy -0.210086 -0.5)
					(xy 0.5 -0.5)
					(xy 0.5 0.5)
					(xy -0.5 0.5)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd rect
		(at -1.4 -0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at -1.4 0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd custom
		(at -1.4 2.1)
		(size 0.795 0.795)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.5)
					(xy 0.5 -0.5)
					(xy 0.5 0.5)
					(xy -0.210086 0.5)
					(xy -0.5 0.210086)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd rect
		(at 0 -2.1)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at 0 -0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at 0 0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at 0 2.1)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd custom
		(at 1.4 -2.1)
		(size 0.795 0.795)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.5)
					(xy 0.210086 -0.5)
					(xy 0.5 -0.210086)
					(xy 0.5 0.5)
					(xy -0.5 0.5)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd rect
		(at 1.4 -0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd rect
		(at 1.4 0.7)
		(size 1 1)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "1" smd custom
		(at 1.4 2.1)
		(size 0.795 0.795)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -0.5 -0.5)
					(xy 0.5 -0.5)
					(xy 0.5 0.210086)
					(xy 0.210086 0.5)
					(xy -0.5 0.5)
				)
				(width 0)
			)
		)
	)
)"""  # NOQA: W191

RESULT_CHAMFERED_ROUNDED_PAD = """(footprint "chamfered_round_pad"
	(version 20240108)
	(generator "kicad-footprint-generator")
	(layer "F.Cu")
	(attr smd)
	(pad "1" smd custom
		(at 0 0)
		(size 3.646447 3.646447)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -2 -1.5)
					(xy -1.5 -2)
					(xy 1.5 -2)
					(xy 2 -1.5)
					(xy 2 1.5)
					(xy 1.5 2)
					(xy -1.5 2)
					(xy -2 1.5)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd roundrect
		(at 0 0)
		(size 4 4)
		(layers "B.Cu")
		(roundrect_rratio 0.25)
	)
	(pad "1" smd custom
		(at 0 5)
		(size 2.292893 2.292893)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -2 -0.5)
					(xy -1 -1.5)
					(xy 1 -1.5)
					(xy 2 -0.5)
					(xy 2 0.5)
					(xy 1 1.5)
					(xy -1 1.5)
					(xy -2 0.5)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 0 5)
		(size 2.292893 2.292893)
		(layers "B.Cu")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -1.292893 -0.207107)
					(xy -0.707107 -0.792893)
					(xy 0.707107 -0.792893)
					(xy 1.292893 -0.207107)
					(xy 1.292893 0.207107)
					(xy 0.707107 0.792893)
					(xy -0.707107 0.792893)
					(xy -1.292893 0.207107)
				)
				(width 1.414214)
			)
		)
	)
	(pad "1" smd custom
		(at 5 0)
		(size 2.292893 2.292893)
		(layers "F.Cu" "F.Mask" "F.Paste")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -2 -0.5)
					(xy -1 -1.5)
					(xy 2 -1.5)
					(xy 2 0.5)
					(xy 1 1.5)
					(xy -2 1.5)
				)
				(width 0)
			)
		)
	)
	(pad "1" smd custom
		(at 5 0)
		(size 2.292893 2.292893)
		(layers "B.Cu")
		(options
			(clearance outline)
			(anchor circle)
		)
		(primitives
			(gr_poly
				(pts
					(xy -1.292893 -0.207107)
					(xy -0.707107 -0.792893)
					(xy 1.292893 -0.792893)
					(xy 1.292893 0.207107)
					(xy 0.707107 0.792893)
					(xy -1.292893 0.792893)
				)
				(width 1.414214)
			)
		)
	)
)"""  # NOQA: W191


class Kicad5PadsTests(unittest.TestCase):

    def testRoundRectPad(self):
        kicad_mod = Footprint("roundrect_pad", FootprintType.SMD)

        kicad_mod.append(Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[5, 0], rotation=45, size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.1))

        kicad_mod.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[-5, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.5))

        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_roundrect_pad.kicad_mod')
        self.assertEqual(result, RESULT_ROUNDRECT_FP)

    def testRoundRectPad2(self):
        kicad_mod = Footprint("roundrect_pad2", FootprintType.SMD)

        kicad_mod.append(Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[5, 0], rotation=45, size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.25, maximum_radius=0.25))

        kicad_mod.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[-5, 0], size=[1, 2], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.25, maximum_radius=0.25))

        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[0, 0], size=[2, 4], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.25, maximum_radius=0.25))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_roundrect_pad2.kicad_mod')
        self.assertEqual(result, RESULT_ROUNDRECT_FP2)

    def testPolygonPad(self):
        kicad_mod = Footprint("polygon_pad", FootprintType.SMD)

        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                             at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             primitives=[Polygon(nodes=[(-1, -1), (2, -1), (1, 1), (-1, 2)])]
                             ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_polygon_pad.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_POLYGON_PAD)

    def testCustomPadOtherPrimitives(self):
        kicad_mod = Footprint("custom_pad_other", FootprintType.SMD)

        kicad_mod.append(
            Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                primitives=[
                     Arc(center=(-1, 0), start=(-1, -0.5), angle=-180, width=0.15),
                     Line(start=(-1, -0.5), end=(1.25, -0.5), width=0.15),
                     Line(start=(1.25, -0.5), end=(1.25, 0.5), width=0.15),
                     Line(start=(1.25, 0.5), end=(-1, 0.5), width=0.15)
                     ]
                ))

        kicad_mod.append(
            Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                at=[0, 3], size=[1, 1], layers=Pad.LAYERS_SMT,
                primitives=[
                     Arc(center=(-1, 0), start=(-1, -0.5), angle=-180, width=0.15),
                     PolygonLine(nodes=[(-1, -0.5), (1.25, -0.5), (1.25, 0.5), (-1, 0.5)], width=0.15)
                     ]
                ))

        kicad_mod.append(
            Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                at=[0, -3], size=[1, 1], layers=Pad.LAYERS_SMT,
                primitives=[
                        Circle(center=(0.5, 0.5), radius=0.5, width=0.15)
                     ]
                ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_custom_pad_other.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_OTHER_CUSTOM_PAD)

    @pytest.mark.filterwarnings("ignore:No geometry checks")
    def testCutPolygon(self):
        kicad_mod = Footprint("cut_polygon", FootprintType.SMD)

        p1 = Polygon(nodes=[(0, 0), (1, 0), (1, 1), (0, 1)])
        p2 = Polygon(nodes=[(-2, -2), (2, -2), (2, 2), (-2, 2)])
        p2.cut(p1)

        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                             at=[0, 0], size=[0.5, 0.5], layers=Pad.LAYERS_SMT,
                             primitives=[p2]
                             ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_cut_polygon.kicad_mod')
        self.assertEqual(result, RESULT_CUT_POLYGON)

    def testChamferedPad(self):
        kicad_mod = Footprint("chamfered_pad", FootprintType.SMD)

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT, chamfer_size=[1/3, 1/3],
                         corner_selection=[1, 1, 1, 1]
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[2, 2], size=[2.1, 3.1], layers=Pad.LAYERS_SMT, chamfer_size=[0.5, 1.05],
                         corner_selection=[1, 1, 1, 1]
                         ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_chamfered_pad.kicad_mod')
        self.assertEqual(result, RESULT_CHAMFERED_PAD)

    def testChamferedPadAvoidCircle(self):
        kicad_mod = Footprint("avoid_circle", FootprintType.SMD)

        pad = ChamferedPad(
                    number=1, type=Pad.TYPE_SMT, at=[2, 2.5],
                    size=[1.75, 2.25], layers=Pad.LAYERS_SMT, chamfer_size=[0.25, 0.25],
                    corner_selection=[1, 1, 1, 1]
                    )

        c = [3, 3.5]
        d = 0.6

        kicad_mod.append(Circle(center=c, radius=d/2, width=0.01))
        pad.chamferAvoidCircle(center=c, diameter=d, clearance=0.005)
        kicad_mod.append(pad)

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_avoid_circle.kicad_mod')
        self.assertEqual(result, RESULT_CHAMFERED_PAD_AVOID_CIRCLE)

    def testChamferedPadGrid(self):
        kicad_mod = Footprint("chamfered_grid", FootprintType.SMD)

        kicad_mod.append(
            ChamferedPadGrid(
                        number=1, type=Pad.TYPE_SMT,
                        center=[1.5, 2.5], size=[1, 2], layers=Pad.LAYERS_SMT,
                        chamfer_size=[0.25, 0.25], chamfer_selection=1,
                        pincount=[3, 4], grid=[1.5, 2.5]
                        ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_chamfered_grid.kicad_mod')
        self.assertEqual(result, RESULT_CHAMFERED_PAD_GRID)

    def testChamferedPadGridCornerOnly(self):
        kicad_mod = Footprint("chamfered_grid_corner_only", FootprintType.SMD)

        chamfer_select = ChamferSelPadGrid(0)
        chamfer_select.setCorners()

        pad = ChamferedPadGrid(
                        number=1, type=Pad.TYPE_SMT,
                        center=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                        chamfer_size=[0.25, 0.25], chamfer_selection=chamfer_select,
                        pincount=[3, 4], grid=[1.4, 1.4]
                        )

        c = [2.0, 2.5]
        d = 0.4

        kicad_mod.append(Circle(center=c, radius=d/2, width=0.01))
        pad.chamferAvoidCircle(center=c, diameter=d, clearance=0.005)
        kicad_mod.append(pad)

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_chamfered_grid_corner_only.kicad_mod')
        self.assertEqual(result, RESULT_CHAMFERED_PAD_GRID_AVOID_CIRCLE)

    def testChamferedRoundedPad(self):
        kicad_mod = Footprint("chamfered_round_pad", FootprintType.SMD)

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[0, 0], size=[4, 4], layers=Pad.LAYERS_SMT, chamfer_size=[0.5, 0.5],
                         corner_selection=[1, 1, 1, 1]
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[0, 0], size=[4, 4], layers=["B.Cu"], chamfer_size=[0.5, 0.5],
                         corner_selection=[1, 1, 1, 1], radius_ratio=0.25
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[0, 5], size=[4, 3], layers=Pad.LAYERS_SMT, chamfer_size=[1, 1],
                         corner_selection=[1, 1, 1, 1]
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[0, 5], size=[4, 3], layers=["B.Cu"], chamfer_size=[1, 1],
                         corner_selection=[1, 1, 1, 1], radius_ratio=0.25
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[5, 0], size=[4, 3], layers=Pad.LAYERS_SMT, chamfer_size=[1, 1],
                         corner_selection=[1, 0, 1, 0]
                         ))

        kicad_mod.append(
            ChamferedPad(number=1, type=Pad.TYPE_SMT,
                         at=[5, 0], size=[4, 3], layers=["B.Cu"], chamfer_size=[1, 1],
                         corner_selection=[1, 0, 1, 0], radius_ratio=0.25
                         ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test_chamfered_round_pad.kicad_mod')
        self.assertEqual(result, RESULT_CHAMFERED_ROUNDED_PAD)
