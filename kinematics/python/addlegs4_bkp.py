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

def draw_joint(rad, joints=[]):
    for i in range(len(joints)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, enter_editmode=False, location=joints[i])

def draw_leg(leg_name, joints=[]):
    draw_segment(leg_name+"_coxia", joints[0], joints[1])
    draw_segment(leg_name+"_femur", joints[1], joints[2])
    draw_segment(leg_name+"_tibia", joints[2], joints[3])
    draw_joint(0.05, joints)

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

def coxia_rot(coxia, leg, init, c):
    leg[1] = (coxia*math.cos(init+c), coxia*math.sin(init+c), 0.0)
    return add_tuple(leg[0], leg[1])

def femur_rot(femur, leg, init, c, f):
    
    # rotate femur angle
    xB1 = femur*math.cos(f) #x
    yB1 = 0.0 #z
    zB1 = femur*math.sin(f) #y
    
    leg[2] = (xB1, yB1, zB1)
    
    # rotate coxia angle to match
    xB2 = xB1*math.cos(init+c) #x
    yB2 = xB1*math.sin(init+c) #z
    zB2 = zB1 #y
    
    leg[2] = (xB2, yB2, zB1)
    
    # position at coxia
    return add_tuple(leg[1], leg[2])


def tibia_rot(tibia, leg, init, c, f, t):
    
    # perpendicular
    t += math.radians(-90)

    # rotate tibia then femur
    xC1 = tibia*math.cos(t+f)
    yC1 = 0.0
    zC1 = tibia*math.sin(t+f) 
    
    leg[3] = (xC1, yC1, zC1)
    
    # rotate coxia angle to match
    xC2 = xC1*math.cos(init+c)
    yC2 = xC1*math.sin(init+c)
    zC2 = zC1
   
    leg[3] = (xC2, yC2, zC2)
    
    # position at femur  
    return add_tuple(leg[2], leg[3])
    
    


def cft_rot(coxia, femur, tibia, leg, init, c, f, t):
    leg[1] = coxia_rot(coxia, leg, init, c)
    leg[2] = femur_rot(femur, leg, init, c, f)
    leg[3] = tibia_rot(tibia, leg, init, c, f, t)
    

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
    
    is_f_common = False
    common_f = math.radians(0)
    
    # 45
    rf_angle = math.radians(45)
    rf_c = math.radians(0)
    rf_f = common_f if is_f_common else math.radians(0)
    rf_t = math.radians(0)

    # 0
    rm_angle = math.radians(0)
    rm_c = math.radians(0)
    rm_f = common_f if is_f_common else math.radians(0)
    rm_t = math.radians(0)
    
    # 315
    rb_angle = math.radians(315)
    rb_c = math.radians(0)
    rb_f = common_f if is_f_common else math.radians(0)
    rb_t = math.radians(0)
    
    # 135
    lf_angle = math.radians(135)
    lf_c = math.radians(0)
    lf_f = common_f if is_f_common else math.radians(0)
    lf_t = math.radians(0)
    
    # 180
    lm_angle = math.radians(180)
    lm_c = math.radians(0)
    lm_f = common_f if is_f_common else math.radians(0)
    lm_t = math.radians(0)
    
    # 225
    lb_angle = math.radians(225)
    lb_c = math.radians(0)
    lb_f = common_f if is_f_common else math.radians(0)
    lb_t = math.radians(0)
    


    leg_rf = [0] * 4
    leg_rf[0] = (1.0, 1.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_rf, rf_angle, rf_c, rf_f, rf_t)
    
    draw_leg("rf", leg_rf)
    
    
    
    
    leg_rm = [0] * 4
    leg_rm[0] = (1.0, 0.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_rm, rm_angle, rm_c, rm_f, rm_t)
    
    draw_leg("rm", leg_rm)
    
    
    
    
    leg_rb = [0] * 4
    leg_rb[0] = (1.0, -1.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_rb, rb_angle, rb_c, rb_f, rb_t)
    
    draw_leg("rb", leg_rb)
    
    
    
    
    leg_lf = [0] * 4
    leg_lf[0] = (-1.0, 1.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_lf, lf_angle, lf_c, lf_f, lf_t)
    
    draw_leg("lf", leg_lf)
    
    
    
    
    leg_lm = [0] * 4
    leg_lm[0] = (-1.0, 0.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_lm, lm_angle, lm_c, lm_f, lm_t)

    draw_leg("lm", leg_lm)
    
    
    
    
    leg_lb = [0] * 4
    leg_lb[0] = (-1.0, -1.0, 0.0)

    cft_rot(coxia, femur, tibia, leg_lb, lb_angle, lb_c, lb_f, lb_t)
    
    draw_leg("lb", leg_lb)
    
draw_pose()

#bpy.ops.object.select_all(action='SELECT')
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
