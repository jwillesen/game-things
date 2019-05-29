from solid import *
from solid.utils import *

tray_depth = 20
tray_walls = 2
tray_roundness = 2

tray_width = 100
tray_height = 100
dimensions = 'outer'
# dimensions = 'inner'
if dimensions == 'inner':
  tray_inner_width = tray_width
  tray_inner_height = tray_height
  tray_outer_width = tray_inner_width + tray_walls * 2
  tray_outer_height = tray_inner_height + tray_walls * 2
else:
  tray_outer_width = tray_width
  tray_outer_height = tray_height
  tray_inner_width = tray_outer_width - tray_walls * 2
  tray_inner_height = tray_outer_height - tray_walls * 2

magnet_diameter = 8
magnet_radius = magnet_diameter / 2
magnet_depth = 1
magnet_width_offset = tray_outer_width / 2
magnet_height_offset = tray_outer_height / 2

magnet_vertical_placement = 'centered'
# magnet_vertical_placement = 'fixed'
if magnet_vertical_placement == 'centered':
  magnet_vertical_offset = tray_depth / 2
else:
  magnet_vertical_offset = magnet_radius + tray_roundness + tray_walls

##### End Parameters #####

def tray_solid(width, height, depth, roundness):
  width = width - roundness * 2
  height = height - roundness * 2
  depth = depth - roundness
  solid = minkowski()(
    cube([width, height, depth]),
    sphere(roundness)
  )
  solid = translate([roundness] * 3)(solid)
  flattener = up(tray_depth)(cube([tray_outer_width, tray_outer_height, tray_roundness]))
  return solid - flattener

def tray_hollow(
  width=tray_outer_width,
  height=tray_outer_height,
  depth=tray_depth,
  roundness=tray_roundness,
  walls=tray_walls
):
  outside = tray_solid(tray_outer_width, tray_outer_height, depth, roundness)
  inside = tray_solid(tray_inner_width, tray_inner_height, depth, roundness)
  inside = translate([walls] * 3)(inside)
  return outside - inside

def magnet_cylinder(orientation):
  if orientation == "wide":
    rotation = rotate([90])
  else:
    rotation = rotate([90, 0, -90])
  return rotation(cylinder(magnet_radius, magnet_depth))

def magnet_hole(orientation, wall):
  fkey = [orientation, wall]
  if fkey == ['wide', 'near']:
    x, y = magnet_width_offset, magnet_depth
  elif fkey == ['wide', 'far']:
    x, y = magnet_width_offset, tray_outer_height
  elif fkey == ['high', 'near']:
    x, y = magnet_depth, magnet_height_offset
  else:
    x, y = tray_outer_width, magnet_height_offset
  translation = translate([x, y, magnet_vertical_offset])
  return translation(magnet_cylinder(orientation))

magnets = [
  magnet_hole('wide', 'near'),
  magnet_hole('wide', 'far'),
  magnet_hole('high', 'near'),
  magnet_hole('high', 'far'),
]

tray = tray_hollow()
for magnet in magnets:
  tray -= magnet

scad_render_to_file(tray, 'tray.scad', file_header='$fn=40;')
