import bpy
import mathutils as mu
import math

# delete all existing
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, enter_editmode=False, location=(0, 1, 0))


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

## Create the object
## pc = point_cloud("point-cloud", [(0.0, 0.0, 1.0)])

## Link object to the active collection
## bpy.context.collection.objects.link(pc)

## Alternatively Link object to scene collection
##bpy.context.scene.collection.objects.link(pc)

base = point_cloud("base", [(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, -1.0, 0.0)], [(0,1), (1,2), (2,3)], [(0,1,2,3)])
bpy.context.collection.objects.link(base)

def draw_segment(name, starting_joint, ending_joint):
    segment = point_cloud(name, [starting_joint, ending_joint], [(0,1)])
    bpy.context.collection.objects.link(segment)
    # draw an edge from starting xyz coords to ending xyz coords

def draw_joint(joints=[]):
    # draw sphere(joint[0])
    # draw sphere(joint[1])
    # draw sphere(joint[2])
    # draw sphere(joint[3])
    pass

def draw_leg(leg_name, joints=[]):
    draw_segment(leg_name+"_coxia", joints[0], joints[1])
    draw_segment(leg_name+"_femur", joints[1], joints[2])
    draw_segment(leg_name+"_tibia", joints[2], joints[3])

def add_tuple(tuple1, tuple2):
    listcv1 = list(tuple1)
    listcv2 = list(tuple2)
    
    newlist = [0] * len(listcv1)
    i = 0
    for elm in newlist:
        newlist[i] = listcv1[i] + listcv2[i]
        i += 1
    
    newtuple = tuple(newlist)
    return newtuple

def subt_tuple(tuple1, tuple2):
    listcv1 = list(tuple1)
    listcv2 = list(tuple2)
    
    newlist = [0] * len(listcv1)
    i = 0
    for elm in newlist:
        newlist[i] = listcv1[i] - listcv2[i]
        i += 1
    
    newtuple = tuple(newlist)
    return newtuple


def roty(coords, theta):
    maty = [[math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]]
    mult = [maty[0][0]*coords[0] + maty[0][1]*coords[1] + maty[0][2]*coords[2],
            maty[1][0]*coords[0] + maty[1][1]*coords[1] + maty[1][2]*coords[2],
            maty[2][0]*coords[0] + maty[2][1]*coords[1] + maty[2][2]*coords[2]]
    return mult

def rotx_tuple(coords, theta):
    coords = list((coords))
    matx = [[1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)]]
    mult = [matx[0][0]*coords[0] + matx[0][1]*coords[1] + matx[0][2]*coords[2],
            matx[1][0]*coords[0] + matx[1][1]*coords[1] + matx[1][2]*coords[2],
            matx[2][0]*coords[0] + matx[2][1]*coords[1] + matx[2][2]*coords[2]]
    return tuple(mult)

def roty_tuple(coords, theta):
    coords = list((coords))
    maty = [[math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]]
    mult = [maty[0][0]*coords[0] + maty[0][1]*coords[1] + maty[0][2]*coords[2],
            maty[1][0]*coords[0] + maty[1][1]*coords[1] + maty[1][2]*coords[2],
            maty[2][0]*coords[0] + maty[2][1]*coords[1] + maty[2][2]*coords[2]]
    return tuple(mult)

def rotz_tuple(coords, theta):
    coords = list((coords))
    matz = [[math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1]]
    mult = [matz[0][0]*coords[0] + matz[0][1]*coords[1] + matz[0][2]*coords[2],
            matz[1][0]*coords[0] + matz[1][1]*coords[1] + matz[1][2]*coords[2],
            matz[2][0]*coords[0] + matz[2][1]*coords[1] + matz[2][2]*coords[2]]
    return tuple(mult)

def trans_tuple(coords, Tx, Ty, Tz):
    coords = list((coords))
    matz = [[1, 0, 0, Tx],
            [0, 1, 0, Ty],
            [0, 0, 1, Tz]]
    mult = [matz[0][0]*coords[0] + matz[0][1]*coords[1] + matz[0][2]*coords[2] + matz[0][3]*coords[3],
            matz[1][0]*coords[0] + matz[1][1]*coords[1] + matz[1][2]*coords[2] + matz[1][3]*coords[3],
            matz[2][0]*coords[0] + matz[2][1]*coords[1] + matz[2][2]*coords[2] + matz[2][3]*coords[3]]
    return tuple(mult)


#leg_test = [0] * 4
#leg_test[0] = (0,0,0)
#leg_test[1] = (1,1,1)
#leg_test[2] = (2,2,2)
#leg_test[3] = (3,3,3)

#draw_leg("test leg", leg_test)
coxia_angles = [0, 45, 135, 180, 225, 315]

def draw_pose():
    radius = 1
    hex_height = 10
    
#    front = 100
#    side = 100
#    middle = 100

    coxia = 1
    femur = 1
    tibia = 1
    # angle, 90 is declared as pi/2
    
    rf_angle = math.radians(0)
    rf_c = math.radians(0)
    rf_f = math.radians(-90)
    rf_t = math.radians(0)
    
    rm_angle = math.radians(0)
    rm_c = math.radians(0)
    rm_f = math.radians(0)
    rm_t = math.radians(0)
    
    rb_angle = math.radians(0)
    rb_c = math.radians(0)
    rb_f = math.radians(0)
    rb_t = math.radians(0)
    
    lb_angle = math.radians(180)
    lf_c = math.radians(180)
    lf_f = math.radians(0)
    lf_t = math.radians(0)
    
    lm_c = math.radians(180)
    lm_f = math.radians(0)
    lm_t = math.radians(0)
    
    lb_c = math.radians(180)
    lb_f = math.radians(0)
    lb_t = math.radians(0)
    


    leg_rf = [0] * 4
    leg_rf[0] = (1.0, 2.0, 0.0)

    leg_rf[1] = (coxia*math.cos(rf_angle+rf_c), coxia*math.sin(rf_angle+rf_c), 0.0)
    leg_rf[1] = add_tuple(leg_rf[0], leg_rf[1])
    
    leg_rf[2] = (femur*math.cos(rf_angle+rf_c), femur*math.sin(rf_angle+rf_c), 0.0)
    leg_rf[2] = roty_tuple(leg_rf[2], -rf_c)
    leg_rf[2] = add_tuple(leg_rf[1], leg_rf[2])

    leg_rf[3] = (tibia*math.cos(rf_angle+rf_c), tibia*math.sin(rf_angle+rf_c), 0.0)
    leg_rf[3] = add_tuple(leg_rf[2], leg_rf[3])
    draw_leg("rf", leg_rf)
    
    
    
    leg_rm = [0] * 4
    leg_rm[0] = (1.0, 1.0, 0.0)

    leg_rm[1] = (coxia*math.cos(rm_angle+rm_c), coxia*math.sin(rm_angle+rm_c), 0.0)
    leg_rm[1] = add_tuple(leg_rm[0], leg_rm[1])
    
    leg_rm[2] = (femur*math.cos(rm_angle+rm_c), femur*math.sin(rm_angle+rm_c), 0.0)
    leg_rm[2] = roty_tuple(leg_rm[2], -rm_f)
    leg_rm[2] = add_tuple(leg_rm[1], leg_rm[2])
    
    print(leg_rm[2])

    leg_rm[3] = (tibia*math.cos(rm_angle), tibia*math.sin(rm_angle), 0.0)
    leg_rm[3] = roty_tuple(leg_rm[3], -rm_t)
    leg_rm[3] = add_tuple(leg_rm[2], leg_rm[3])
    draw_leg("rm", leg_rm)
    
    
    
    leg_rb = [0] * 4
    leg_rb[0] = (1.0, -1.0, 0.0)

    leg_rb[1] = (coxia*math.cos(rb_c), coxia*math.sin(rb_c), 0.0)
    leg_rb[1] = add_tuple(leg_rb[0], leg_rb[1])
    
    leg_rb[2] = (femur*math.cos(rb_c), femur*math.sin(rb_c), 0.0)
    leg_rb[2] = roty_tuple(leg_rb[2], rb_f)
    leg_rb[2] = add_tuple(leg_rb[1], leg_rb[2])

    leg_rb[3] = (tibia*math.cos(rb_c), tibia*math.sin(rb_c), 0.0)
    leg_rb[3] = roty_tuple(leg_rb[3], rb_t)
    leg_rb[3] = add_tuple(leg_rb[2], leg_rb[3])
    draw_leg("rb", leg_rb)
    
    
    
    leg_lf = [0] * 4
    leg_lf[0] = (-1.0, 2.0, 0.0)

    leg_lf[1] = (coxia*math.cos(lf_c), coxia*math.sin(lf_c), 0.0)
    leg_lf[1] = add_tuple(leg_lf[0], leg_lf[1])
    
    leg_lf[2] = (femur*math.cos(lf_c), femur*math.sin(lf_c), 0.0)
    leg_lf[2] = roty_tuple(leg_lf[2], lf_f)
    leg_lf[2] = add_tuple(leg_lf[1], leg_lf[2])
    

    leg_lf[3] = (tibia*math.cos(lf_c), tibia*math.sin(lf_c), 0.0)
    leg_lf[3] = roty_tuple(leg_lf[3], lf_t)
    leg_lf[3] = add_tuple(leg_lf[2], leg_lf[3])
    draw_leg("lf", leg_lf)
    
    
    
    leg_lm = [0] * 4
    leg_lm[0] = (-1.0, 1.0, 0.0)

    leg_lm[1] = (coxia*math.cos(lm_c), coxia*math.sin(lm_c), 0.0)
    leg_lm[1] = add_tuple(leg_lm[0], leg_lm[1])
    
    leg_lm[2] = (femur*math.cos(lm_c), femur*math.sin(lm_c), 0.0)
    leg_lm[2] = roty_tuple(leg_lm[2], lm_f)
    leg_lm[2] = add_tuple(leg_lm[1], leg_lm[2])
    

    leg_lm[3] = (tibia*math.cos(lm_c), tibia*math.sin(lm_c), 0.0)
    leg_lm[3] = roty_tuple(leg_lm[3], lm_t)
    leg_lm[3] = add_tuple(leg_lm[2], leg_lm[3])
    draw_leg("lm", leg_lm)
    
    
    
    leg_lb = [0] * 4
    leg_lb[0] = (-1.0, -1.0, 0.0)

    leg_lb[1] = (coxia*math.cos(lb_c), coxia*math.sin(lb_c), 0.0)
    leg_lb[1] = add_tuple(leg_lb[0], leg_lb[1])
    
    leg_lb[2] = (femur*math.cos(lb_c), femur*math.sin(lb_c), 0.0)
    leg_lb[2] = roty_tuple(leg_lb[2], lb_f)
    leg_lb[2] = add_tuple(leg_lb[1], leg_lb[2])

    leg_lb[3] = (tibia*math.cos(lb_c), tibia*math.sin(lb_c), 0.0)
    leg_lb[3] = roty_tuple(leg_lb[3], lb_t)
    leg_lb[3] = add_tuple(leg_lb[2], leg_lb[3])
    draw_leg("lb", leg_lb)
draw_pose()

bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')



## 3rd arg shows how to make edges
## pc = point_cloud("point-cloud", [(-10.0, 10.0, 0), (10.0, 10.0, 0), (10.0, -10.0, 0), (-10.0, -10.0, 0)], [(0,1), (1,2), (2,3), (3,0)], [(0,1,2,3)]) 

#hex_height = 1

#coxia_len = 1
#femur_len = 1
#tibia_len = 1

## angle between coxia and femur
#beta = 45

#radius = 1
#coxia_angles = [0, 45, 135, 180, 225, 315]

#coxia_axes = [0, 0, 0, 0, 0, 0]
#coxia_axes[0] = (radius, 0.0, hex_height) # x0
#coxia_axes[1] = (radius*math.cos(math.pi/4), radius*math.sin(math.pi/4), hex_height) # x1
#coxia_axes[2] = (-radius*math.cos(math.pi/4), radius*math.sin(math.pi/4), hex_height) # x2
#coxia_axes[3] = (-radius, 0.0, hex_height) # x3
#coxia_axes[4] = (-radius*math.cos(math.pi/4), -radius*math.sin(math.pi/4), hex_height) # x4
#coxia_axes[5] = (radius*math.cos(math.pi/4), -radius*math.sin(math.pi/4), hex_height) # x5

#p0 = [0, 0, 0, 0, 0, 0]
#p0[0] = (coxia_len, 0.0, hex_height)

#p1 = [0, 0, 0, 0, 0, 0]
#p1[0] = (radius+coxia_len, 0.0, hex_height)

#p2 = [0, 0, 0, 0, 0, 0]
#p2[0] = (coxia_len+radius+(radius*math.cos(math.pi/4)), 0.0, hex_height-(radius*math.cos(math.pi/4)))

#p3 = [0, 0, 0, 0, 0, 0]
#p3[0] = (coxia_len+radius, 0.0, hex_height-(radius*math.cos(math.pi/4))-(radius*math.cos(math.pi/4)))

#legs_points = [0, 0, 0, 0, 0, 0]
#legs_points[0] = [p0[0], p1[0], p2[0], p3[0]]


##TODO: move cursor, make legs
##base = point_cloud("point-cloud", [(-10.0, 10.0, 0), (10.0, 10.0, 0), (10.0, -10.0, 0), (-10.0, -10.0, 0)], [], [(0,1,2,3)])

#bpy.context.scene.cursor.location = (0, 0, 0)
#base = point_cloud("base", [(0.0, 0.0, 1.0)])
#bpy.context.collection.objects.link(base)

#x = point_cloud("x0", legs_points[0], [(0,1), (1, 2), (2,3)])
#bpy.context.collection.objects.link(x)

##index = 0
##for leg in coxia_axes:
##    bpy.context.scene.cursor.location = coxia_axes[index]
##    
##    x = point_cloud("x" + str(index), [coxia_axes[index]])
##    bpy.context.collection.objects.link(x)
##    
##    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
##    index += 1
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
#bpy.context.scene.cursor.location = (0, 0, 0)

## create length by extrude
##bpy.data.objects["x0"].select_set(True)
##bpy.context.view_layer.objects.active = bpy.data.objects["x0"]
##bpy.ops.object.editmode_toggle()
##bpy.ops.mesh.extrude_context(use_normal_flip=False, mirror=False)