import bpy
import math

def point_cloud(ob_name, coords, edges=[], faces=[]):
    """Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    me.update()
    return ob

# Create the object
# pc = point_cloud("point-cloud", [(0.0, 0.0, 1.0)])

# Link object to the active collection
# bpy.context.collection.objects.link(pc)

# Alternatively Link object to scene collection
#bpy.context.scene.collection.objects.link(pc)

# 3rd arg shows how to make edges
# pc = point_cloud("point-cloud", [(-10.0, 10.0, 0), (10.0, 10.0, 0), (10.0, -10.0, 0), (-10.0, -10.0, 0)], [(0,1), (1,2), (2,3), (3,0)], [(0,1,2,3)]) 

hex_height = 1

coxia_len = 10
femur_len = 1
tibia_len = 1

radius = 10
coxia_angles = [0, 45, 135, 180, 225, 315]

coxia_axes = [0, 0, 0, 0, 0, 0]
coxia_axes[0] = (radius, 0.0, hex_height) # x0
coxia_axes[1] = (radius*math.cos(math.pi/4), radius*math.sin(math.pi/4), hex_height) # x1
coxia_axes[2] = (-radius*math.cos(math.pi/4), radius*math.sin(math.pi/4), hex_height) # x2
coxia_axes[3] = (-radius, 0.0, hex_height) # x3
coxia_axes[4] = (-radius*math.cos(math.pi/4), -radius*math.sin(math.pi/4), hex_height) # x4
coxia_axes[5] = (radius*math.cos(math.pi/4), -radius*math.sin(math.pi/4), hex_height) # x5

p0 = [0, 0, 0, 0, 0, 0]
p0[0] = (radius, 0.0, hex_height)

p1 = [0, 0, 0, 0, 0, 0]
p1[0] = (radius+coxia_len, 0.0, hex_height)

p2 = [0, 0, 0, 0, 0, 0]
p2[0] = (coxia_len+radius+(radius*math.cos(math.pi/4)), 0.0, hex_height-(radius*math.cos(math.pi/4)))

p3 = [0, 0, 0, 0, 0, 0]
p3[0] = (coxia_len+radius, 0.0, hex_height-(radius*math.cos(math.pi/4))-(radius*math.cos(math.pi/4)))

legs_points = [0, 0, 0, 0, 0, 0]
legs_points[0] = [p0[0], p1[0], p2[0], p3[0]]


#TODO: move cursor, make legs
#base = point_cloud("point-cloud", [(-10.0, 10.0, 0), (10.0, 10.0, 0), (10.0, -10.0, 0), (-10.0, -10.0, 0)], [], [(0,1,2,3)])
#i've got this funny story

bpy.context.scene.cursor.location = (0, 0, 0)
base = point_cloud("base", [(0.0, 0.0, 1.0)])
bpy.context.collection.objects.link(base)

x = point_cloud("x0", legs_points[0], [(0,1), (1, 2), (2,3)])
bpy.context.collection.objects.link(x)

#index = 0
#for leg in coxia_axes:
#    bpy.context.scene.cursor.location = coxia_axes[index]
#    
#    x = point_cloud("x" + str(index), [coxia_axes[index]])
#    bpy.context.collection.objects.link(x)
#    
#    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
#    index += 1
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
bpy.context.scene.cursor.location = (0, 0, 0)

# create length by extrude
#bpy.data.objects["x0"].select_set(True)
#bpy.context.view_layer.objects.active = bpy.data.objects["x0"]
#bpy.ops.object.editmode_toggle()
#bpy.ops.mesh.extrude_context(use_normal_flip=False, mirror=False)