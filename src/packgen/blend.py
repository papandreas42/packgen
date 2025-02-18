# Script by Andrea Insinga

import bpy
import random
import array as arr

# 1) Select "Scripting" workspace
# 2) In the "Text Editor" window, open this script and click "Run Script"
# 3) Select "Animation" workspace
# 4) In the "Timeline" press "Play"
# 5) Erase the cube and export as stl.

GlobalScaleFactor = 2.5
# The two arrays must be the same number of elements
# (they represent COMBINATIONS of radius and height)
CombinationsRadii = arr.array(
    "d", [0.0500, 0.0750, 0.1000, 0.1250, 0.1500, 0.1750, 0.2000, 0.2250, 0.2500]
)
CombinationsHeights = arr.array(
    "d", [0.0500, 0.0750, 0.1000, 0.1250, 0.1500, 0.1750, 0.2000, 0.2250, 0.2500]
)
CombinationsFractions = arr.array("d", [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])
CombinationsCumSum = arr.array("d", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
CombinationRed = arr.array("d", [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])
CombinationGreen = arr.array("d", [0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.8])
CombinationBlue = arr.array("d", [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.5])
TheSum = sum(CombinationsFractions)

# Normalize array
for i in range(len(CombinationsFractions)):
    CombinationsFractions[i] = CombinationsFractions[i] / TheSum

# Cumulative Sum
CumulativeSum = 0.0
for i in range(len(CombinationsFractions)):
    CumulativeSum = CumulativeSum + CombinationsFractions[i]
    CombinationsCumSum[i] = CumulativeSum


def create_cube_without_top_face(thesize):
    bpy.ops.mesh.primitive_cube_add(
        size=thesize, enter_editmode=False, location=(0, 0, 0)
    )
    cube = bpy.context.active_object

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.mesh.select_mode(type="FACE")

    bpy.ops.object.mode_set(mode="OBJECT")
    top_face = [face for face in cube.data.polygons if face.normal.z > 0.9]
    for face in top_face:
        face.select = True

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.delete(type="FACE")
    bpy.ops.object.mode_set(mode="OBJECT")

    return cube


def add_solidify_modifier(cube, thickness):
    modifier = cube.modifiers.new(name="Solidify", type="SOLIDIFY")
    modifier.thickness = thickness


def add_passive_rigidbody(cube):
    bpy.ops.rigidbody.object_add(type="PASSIVE")
    cube.rigid_body.collision_shape = "MESH"


# Customize the following parameters for your array of cubes
num_cubes_x = 2  # Number of cubes along the X axis
num_cubes_y = 2  # Number of cubes along the Y axis
num_cubes_z = 50  # Number of   cubes along the Z axis
distance = 2.5  # Distance between the cubes
mu = 0  # Mean of the log-normal distribution
sigma = 0.1  # Standard deviation of the log-normal distribution
random.seed(42)  # Optional: set a seed for reproducible results

# Delete all existing mesh objects
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()

# Create an array of cubes with random sizes determined by the log-normal distribution
for x in range(num_cubes_x):
    for y in range(num_cubes_y):
        for z in range(num_cubes_z):
            ThisRandomNumber = random.uniform(0.0, 1.0)
            LastI = -1
            for i in range(len(CombinationsFractions)):
                if ThisRandomNumber > CombinationsCumSum[i]:
                    LastI = i
            LastI = LastI + 1

            bpy.ops.mesh.primitive_cylinder_add(
                vertices=6,
                radius=GlobalScaleFactor * CombinationsRadii[LastI],
                depth=GlobalScaleFactor * CombinationsHeights[LastI],
                enter_editmode=False,
                location=(
                    (x - num_cubes_x / 2 + 0.5) * distance,
                    (y - num_cubes_y / 2 + 0.5) * distance,
                    z * distance,
                ),
            )

            # Get the active object (the newly created cube)
            cube = bpy.context.active_object

            # Assign a random rotation to the cube
            cube.rotation_euler = (
                random.uniform(0, 6.283185),
                random.uniform(0, 6.283185),
                random.uniform(0, 6.283185),
            )

            # Add rigid body physics to the cube
            bpy.ops.rigidbody.object_add(type="ACTIVE")
            cube.rigid_body.friction = 0.5
            cube.rigid_body.restitution = 0.5

            mat = bpy.data.materials.new("PKHG")
            mat.diffuse_color = (
                float(CombinationRed[LastI]),
                float(CombinationGreen[LastI]),
                float(CombinationBlue[LastI]),
                1.0,
            )
            mat.specular_intensity = 0

            cube.active_material = mat

thickness = -0.2

cube = create_cube_without_top_face((num_cubes_x) * distance)
add_solidify_modifier(cube, thickness)

add_passive_rigidbody(cube)
