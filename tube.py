from solid import *
from solid.utils import *
from math import pi, cos

render_tube = True
render_sled = True

side_count = 6

base_tolerance = 0.2

# taken from the openscad documentation
# fudge factor to make polygon lie outside of a circle, instead of inside
# multiply by this to go from vertex radius to flat wall radius
# divide by this to go from flat wall radius to vertex radius
radius_fudge_factor = cos(pi / side_count)

token_diameter = 22.0
token_radius = token_diameter / 2.0
token_thickness = 3.0
token_count = 10
token_diameter_tolerance = base_tolerance # additional distance between tokens and sled
token_length_tolerance = base_tolerance # additional distance around tokens front to back

# if you want to specify the internal length instead of tokens, set this
override_internal_sled_length = 0
sled_internal_length = (
  override_internal_sled_length or
  token_thickness * token_count + token_length_tolerance
)
sled_wall_thickness = 2.0

tube_wall_thickness = 2.0
tube_window_width = 5.0
tube_window_height_margin = 5.0
tube_tolerance = base_tolerance # extra distance between tube and sled

door_lip = 3.0
door_thickness = 2.0
door_roundness = 0.5

sled_external_length = sled_internal_length + sled_wall_thickness

sled_flat_wall_internal_radius = token_radius + token_diameter_tolerance
sled_flat_wall_external_radius = sled_flat_wall_internal_radius + sled_wall_thickness
sled_internal_radius = sled_flat_wall_internal_radius / radius_fudge_factor
sled_external_radius = sled_flat_wall_external_radius / radius_fudge_factor

tube_external_length = sled_external_length + tube_wall_thickness + tube_tolerance
tube_flat_wall_internal_radius = sled_flat_wall_external_radius + tube_tolerance
tube_flat_wall_external_radius = tube_flat_wall_internal_radius + tube_wall_thickness
tube_internal_radius = tube_flat_wall_internal_radius / radius_fudge_factor
tube_external_radius = tube_flat_wall_external_radius / radius_fudge_factor

door_flat_wall_radius = tube_flat_wall_external_radius + door_lip

# ~~~~~~ main ~~~~~~

# distance from origin to sled external flat wall
sled_external_flat_wall_radius = sled_external_radius * radius_fudge_factor

def door():
  mink_door_radius = (door_flat_wall_radius - door_roundness) / radius_fudge_factor
  door = up(door_roundness)(minkowski()(
    cylinder(h=door_thickness - door_roundness * 2, r=mink_door_radius, segments=side_count),
    sphere(door_roundness)
  ))
  door_radius = door_flat_wall_radius / radius_fudge_factor
  door_lip_from_sled = door_flat_wall_radius - sled_external_flat_wall_radius
  door_flattener = cube([door_radius*2, door_lip_from_sled, door_thickness])
  door_flattener = translate([-mink_door_radius, -sled_external_flat_wall_radius - door_lip_from_sled])(door_flattener)
  door -= door_flattener
  return door

def sled():
  sled_interior = up(sled_wall_thickness)(cylinder(h=sled_internal_length, r=sled_internal_radius, segments=side_count))
  sled_flattener = cube([sled_external_radius * 2, sled_external_radius, sled_internal_length])
  sled_flattener = translate([-sled_external_radius, 0, sled_wall_thickness])(sled_flattener)
  # add door thickness so the tube overlaps the door to make a cleaner union for printing
  sled = cylinder(h=sled_external_length + door_thickness, r=sled_external_radius, segments=side_count)
  sled = sled - sled_flattener - sled_interior
  # tokens = color(Transparent)(cylinder(r=token_diameter / 2.0, h=token_thickness * token_count))
  # sled += up(sled_wall_thickness)(tokens)
  sled += up(sled_external_length)(door())
  sled = rotate([90, 0, 90])(sled)
  sled = up(sled_external_flat_wall_radius)(sled)
  return sled

def tube_window():
  window_radius = tube_window_width / 2.0
  window_length = tube_external_length - tube_wall_thickness - tube_window_height_margin * 2
  # seems we need a little extra thickness for floating point errors so the window will punch all the way through
  window_end_fudge_height = 0.1
  window_end = cylinder(h=tube_wall_thickness + window_end_fudge_height, r=window_radius),
  window = hull()(window_end, right(window_length)(window_end))
  window = rotate([0, -90])(window)
  window = translate([window_end_fudge_height / 2, 0, tube_window_height_margin + tube_wall_thickness])(window)
  return window

def tube():
  tube = cylinder(h=tube_external_length, r=tube_external_radius, segments=side_count)
  tube_hollow = up(tube_wall_thickness)(cylinder(h=tube_external_length, r=tube_internal_radius, segments=side_count))
  tube -= tube_hollow
  tube = rotate([0, 0, 180.0 / side_count])(tube)
  window = right(tube_flat_wall_external_radius)(tube_window())
  tube -= window
  return tube


scad_render_to_file(sled(), 'sled.scad', file_header='$fn=40;')
scad_render_to_file(tube(), 'tube.scad', file_header='$fn=40;')
