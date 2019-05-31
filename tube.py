from solid import *
from solid.utils import *
from math import pi, cos

render_tube = True
render_sled = True

side_count = 6

token_diameter = 25.0
token_radius = token_diameter / 2.0
token_thickness = 2.0
token_count = 40

override_internal_sled_length = 0
sled_internal_length = override_internal_sled_length or token_thickness * token_count
sled_wall_thickness = 2.0

# fudge factor to make polygon lie outside the token circle, instead of inside
# taken from the openscad documentation
sled_internal_radius_fudge_factor = 1.0 / cos(pi / side_count)

sled_internal_radius = token_radius * sled_internal_radius_fudge_factor
sled_external_radius = sled_internal_radius + sled_wall_thickness
sled_external_length = sled_internal_length + sled_wall_thickness

tube_wall_thickness = 2.0
tube_external_radius = sled_external_radius + tube_wall_thickness
tube_external_length = sled_external_length + tube_wall_thickness
tube_window_width = 5.0
tube_window_height_margin = 5.0

door_lip = 3.0
door_radius = tube_external_radius + door_lip
door_thickness = 2.0
door_roundness = 0.5

# ~~~~~~ main ~~~~~~

sled_interior = up(sled_wall_thickness)(cylinder(h=sled_internal_length, r=sled_internal_radius, segments=side_count))
sled_flattener = cube([sled_external_radius * 2, sled_external_radius, sled_internal_length])
sled_flattener = translate([-sled_external_radius, 0, sled_wall_thickness])(sled_flattener)

tube = cylinder(h=tube_external_length, r=tube_external_radius, segments=side_count)

door = up(door_roundness)(minkowski()(
  cylinder(h=door_thickness - door_roundness * 2, r=door_radius - door_roundness, segments=side_count),
  sphere(door_roundness)
))

# distance from origin to sled external flat wall
sled_external_flat_wall_radius = sled_external_radius * cos(pi / side_count)
door_flattener = cube([door_radius*2, door_lip, door_thickness])
door_flattener = translate([-door_radius, -sled_external_flat_wall_radius - door_lip])(door_flattener)
door += door_flattener

tokens = color(Transparent)(cylinder(r=token_diameter / 2.0, h=token_thickness * token_count))

sled = cylinder(h=sled_external_length, r=sled_external_radius, segments=side_count)
sled = sled - sled_flattener - sled_interior
sled += up(sled_wall_thickness)(tokens)
sled += up(sled_external_length)(door)
sled = rotate([90, 0, 90])(sled)
sled = up(sled_external_flat_wall_radius)(sled)


# scad_render_to_file(tube, 'tube.scad', file_header='$fn=40;')
# scad_render_to_file(left(tube_external_radius * 2)(sled), 'sled.scad', file_header='$fn=40;')
# scad_render_to_file(tube + left(tube_external_radius * 2)(sled), 'tube.scad', file_header='$fn=40;')
# scad_render_to_file(sled, 'tube.scad', file_header='$fn=40;')
scad_render_to_file(sled, 'tube.scad', file_header='$fn=40;')
