import bpy
import sys

import math
import numpy
from pyquaternion import Quaternion

#sys.path.append("~/Desktop/apps/blender-2.82a-linux64/2.82/scripts/modules/mymodules/hexapod_robot_simulator_master")
#sys.path.append("~/Desktop/apps/blender-2.82a-linux64/2.82/scripts/modules/mymodules/hexapod_robot_simulator_master/hexapod")
#sys.path.append("~/Desktop/apps/blender-2.82a-linux64/2.82/scripts/modules/mymodules/hexapod_robot_simulator_master/hexapod")
#sys.path.append("~/Desktop/apps/blender-2.82a-linux64/2.82/scripts/modules/mymodules/hexapod_robot_simulator_master/hexapod/ik_solver")

sys.path.append("/home/d15/Desktop/apps/blender-2.82a-linux64/modules/hexapod_robot_simulator_master")
#sys.path.append("/home/d15/Desktop/apps/blender-2.82a-linux64/modules/hexapod_robot_simulator_master/hexapod")
sys.path.append("/home/d15/Desktop/apps/blender-2.82a-linux64/modules/hexapod_robot_simulator_master/hexapod/ik_solver")

import models
import ik_solver2
from walkSequenceSolver import getWalkSequence
import pprint

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

def draw_segment(leg_name, segment_name, starting_joint, ending_joint):
    segment = point_cloud(leg_name+segment_name, [starting_joint, ending_joint], [(0,1)])
    bpy.context.collection.objects.link(segment)
    
    #draw_joint3(leg_name, segment_name, starting_joint, 0.05)
    
def draw_joint2(leg_name, segment_name, starting_joint, rad):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, enter_editmode=False, location=starting_joint)
    bpy.context.active_object.name = leg_name+segment_name+"_sphere"
    bpy.data.objects[leg_name+segment_name+"_sphere"].select_set(True)
    bpy.data.objects[leg_name+segment_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[leg_name+segment_name]
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

def draw_joint3(leg_name, segment_name, starting_joint, rad):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, enter_editmode=False, location=starting_joint)
    bpy.context.active_object.name = leg_name+segment_name+"_sphere"
    bpy.data.objects[leg_name+segment_name+"_sphere"].select_set(True)
    bpy.data.objects[leg_name+segment_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[leg_name+segment_name]
    bpy.ops.object.join()
#    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

def draw_joint(rad, joints=[]):
    for i in range(len(joints)):
        sphere = bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, enter_editmode=False, location=joints[i])
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        bpy.data.objects[join].select_set(True)


def draw_leg(leg_name, joints=[]):
    draw_segment(leg_name, "_coxia", joints[0], joints[1])
#    bpy.data.objects[leg_name+"_coxia"].select_set(True)
#    bpy.context.scene.cursor.location = (joints[0])
#    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
#    bpy.ops.object.select_all(action='DESELECT')

    draw_segment(leg_name, "_femur", joints[1], joints[2])
#    bpy.data.objects[leg_name+"_femur"].select_set(True)
#    bpy.context.scene.cursor.location = (joints[1])
#    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
#    bpy.ops.object.select_all(action='DESELECT')

    draw_segment(leg_name, "_tibia", joints[2], joints[3])
#    bpy.data.objects[leg_name+"_tibia"].select_set(True) 
#    bpy.context.scene.cursor.location = (joints[2])
#    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
#    bpy.ops.object.select_all(action='DESELECT')
    
    #draw_joint(leg_name, 0.05, joints)

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

def tuple_quaternion_rot(tuple, quaternion):
    make_list = list(tuple)
    make_list= numpy.array(make_list)
    rotate = quaternion.rotate(make_list)
    return rotate

def coxia_rot(coxia, leg, init, c, total_rot):

    leg[1] = (coxia*math.cos(init+c), coxia*math.sin(init+c), 0.0)
    
    leg[1] = tuple(tuple_quaternion_rot(leg[1], total_rot))
    
    return add_tuple(leg[0], leg[1])

def femur_rot(femur, leg, init, c, f, total_rot):

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
    
    leg[2] = tuple(tuple_quaternion_rot(leg[2], total_rot))
    
    # position at coxia
    return add_tuple(leg[1], leg[2])


def tibia_rot(tibia, leg, init, c, f, t, total_rot):
    
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
    
    leg[3] = tuple(tuple_quaternion_rot(leg[3], total_rot))
    
    # position at femur  
    return add_tuple(leg[2], leg[3])

def coxia_rot_offset(offset, coxia, leg, init, c, total_rot):

    leg[1] = (coxia*math.cos(init+c), coxia*math.sin(init+c), 0.0)
    
    leg[1] = tuple(tuple_quaternion_rot(leg[1], total_rot))
    #leg[1] = add_tuple(leg[1], (0, abs(list(offset[1])[1]), 0))
    #leg[1] = add_tuple(leg[1], (0, list(offset[1])[1], 0))
    
    return add_tuple(leg[0], leg[1])

def femur_rot_offset(offset, femur, leg, init, c, f, total_rot):

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
    
    leg[2] = tuple(tuple_quaternion_rot(leg[2], total_rot))
    
    #leg[2] = add_tuple(leg[2], (0, abs(list(offset[2])[1]), 0))
    
    # position at coxia
    return add_tuple(leg[1], leg[2])


def tibia_rot_offset(offset, tibia, leg, init, c, f, t, total_rot):
    
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
    
    leg[3] = tuple(tuple_quaternion_rot(leg[3], total_rot))
    #leg[3] = add_tuple(leg[3], (0, abs(list(offset[3])[1]), 0))
    
    # position at femur  
    return add_tuple(leg[2], leg[3])

def cft_rot(coxia, femur, tibia, leg, init, c, f, t, total_rot):
    leg[1] = coxia_rot(coxia, leg, init, c, total_rot)
    leg[2] = femur_rot(femur, leg, init, c, f, total_rot)
    leg[3] = tibia_rot(tibia, leg, init, c, f, t, total_rot)

def cft_rot_o(offset, coxia, femur, tibia, leg, init, c, f, t, total_rot):
    leg[1] = coxia_rot_offset(offset, coxia, leg, init, c, total_rot)
    leg[2] = femur_rot_offset(offset, femur, leg, init, c, f, total_rot)
    leg[3] = tibia_rot_offset(offset, tibia, leg, init, c, f, t, total_rot)
    
def make_leg(legname, bodyjoint, coxia, femur, tibia, leg, init, c, f, t):
    leg = [0] * 4
    leg[0] = bodyjoint

    cft_rot(coxia, femur, tibia, leg, init, c, f, t)
    
    draw_leg(legname, leg)

def get_ik(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z):
    dimensions = {}
    dimensions["coxia"] = coxia
    dimensions["femur"] = femur
    dimensions["tibia"] = tibia
    dimensions["front"] = front
    dimensions["middle"] = middle
    dimensions["side"] = side
    hexapod = models.VirtualHexapod(dimensions)

    ik_parameters = {}
    ik_parameters["hip_stance"] = hip_stance
    ik_parameters["leg_stance"] = leg_stance
    ik_parameters["percent_x"] = percent_x
    ik_parameters["percent_y"] = percent_y
    ik_parameters["percent_z"] = percent_z
    ik_parameters["rot_x"] = math.degrees(rot_x)
    ik_parameters["rot_y"] = math.degrees(rot_y)
    ik_parameters["rot_z"] = math.degrees(rot_z)

    poses, hexapod = ik_solver2.inverse_kinematics_update(hexapod, ik_parameters)

    return poses

def get_walk(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode):
    hexa = {
        "front": front,
        "side": side,
        "middle": middle,
        "coxia": coxia,
        "femur": femur,
        "tibia": tibia
    }

    params = {
        "tx": percent_x,
        "tz": percent_z,
        "rx": rot_x,
        "ry": rot_y,
        "legStance": leg_stance,
        "hipStance": hip_stance,
        "stepCount": stepCount,
        "hipSwing": hipSwing,
        "liftSwing": liftSwing,
    }

    gaitType = gaitType
    walkMode = walkMode

    poseSequence = getWalkSequence(hexa, params, gaitType, walkMode)
    return poseSequence

def draw_pose(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    leg_stance_dist = femur*math.sin(math.radians(leg_stance))
    
    rm = (middle, 0.0, height)
    rf = (front, side, height)
    lf = (-front, side, height)
    lm = (-middle, 0.0, height)
    lb = (-front, -side, height)
    rb = (front, -side, height)

    rm_rt = tuple(tuple_quaternion_rot(rm, total_rot_global))
    rf_rt = tuple(tuple_quaternion_rot(rf, total_rot_global))
    lf_rt = tuple(tuple_quaternion_rot(lf, total_rot_global))
    lm_rt = tuple(tuple_quaternion_rot(lm, total_rot_global))
    lb_rt = tuple(tuple_quaternion_rot(lb, total_rot_global))
    rb_rt = tuple(tuple_quaternion_rot(rb, total_rot_global))

    rm_rt = add_tuple(rm_rt, (percent_x, percent_y, percent_z))
    rf_rt = add_tuple(rf_rt, (percent_x, percent_y, percent_z))
    lf_rt = add_tuple(lf_rt, (percent_x, percent_y, percent_z))
    lm_rt = add_tuple(lm_rt, (percent_x, percent_y, percent_z))
    lb_rt = add_tuple(lb_rt, (percent_x, percent_y, percent_z))
    rb_rt = add_tuple(rb_rt, (percent_x, percent_y, percent_z))

    rm_rt = add_tuple(rm_rt, (0, 0, -leg_stance_dist))
    rf_rt = add_tuple(rf_rt, (0, 0, -leg_stance_dist))
    lf_rt = add_tuple(lf_rt, (0, 0, -leg_stance_dist))
    lm_rt = add_tuple(lm_rt, (0, 0, -leg_stance_dist))
    lb_rt = add_tuple(lb_rt, (0, 0, -leg_stance_dist))
    rb_rt = add_tuple(rb_rt, (0, 0, -leg_stance_dist))
    
    base = point_cloud("base", [rm_rt, rf_rt, lf_rt, lm_rt, lb_rt, rb_rt], [(0, 1), (1, 2), (2,     3), (3, 4), (4, 5), (5, 0)], [(0, 1, 2, 3, 4, 5)])
    bpy.context.collection.objects.link(base)

    rf_list = list(rf_rt)
    lf_list = list(lf_rt)
    sphere_list = [(rf_list[0]+lf_list[0])/2, (rf_list[1]+lf_list[1])/2, (rf_list[2]+lf_list[2])/2]

    #draw_joint2("", "base", sphere_list, 0.2)
    
        
    pose = get_ik(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    
    is_f_common = False
    common_f = math.radians(0)
    
    # 0
    rm_angle = math.radians(0)
    rm_c = math.radians(pose[0]["coxia"])
    rm_f = math.radians(pose[0]["femur"])
    rm_t = math.radians(pose[0]["tibia"])
    
    # 45
    rf_angle = math.radians(45)
    rf_c = math.radians(pose[1]["coxia"])
    rf_f = math.radians(pose[1]["femur"])
    rf_t = math.radians(pose[1]["tibia"])
    
    # 135
    lf_angle = math.radians(135)
    lf_c = math.radians(pose[2]["coxia"])
    lf_f = math.radians(pose[2]["femur"])
    lf_t = math.radians(pose[2]["tibia"])
    
    # 180
    lm_angle = math.radians(180)
    lm_c = math.radians(pose[3]["coxia"])
    lm_f = math.radians(pose[3]["femur"])
    lm_t = math.radians(pose[3]["tibia"])
    
    # 225
    lb_angle = math.radians(225)
    lb_c = math.radians(pose[4]["coxia"])
    lb_f = math.radians(pose[4]["femur"])
    lb_t = math.radians(pose[4]["tibia"])
    
    # 315
    rb_angle = math.radians(315)
    rb_c = math.radians(pose[5]["coxia"])
    rb_f = math.radians(pose[5]["femur"])
    rb_t = math.radians(pose[5]["tibia"])
    
    leg_rm = [0] * 4
    leg_rm[0] = rm_rt
    cft_rot(coxia, femur, tibia, leg_rm, rm_angle, rm_c, rm_f, rm_t, total_rot_global)
    draw_leg("rm", leg_rm)
    
    leg_rf = [0] * 4
    leg_rf[0] = rf_rt
    cft_rot(coxia, femur, tibia, leg_rf, rf_angle, rf_c, rf_f, rf_t, total_rot_global)
    draw_leg("rf", leg_rf)
    
    leg_lf = [0] * 4
    leg_lf[0] = lf_rt
    cft_rot(coxia, femur, tibia, leg_lf, lf_angle, lf_c, lf_f, lf_t, total_rot_global)
    draw_leg("lf", leg_lf)

    leg_lm = [0] * 4
    leg_lm[0] = lm_rt
    cft_rot(coxia, femur, tibia, leg_lm, lm_angle, lm_c, lm_f, lm_t, total_rot_global)
    draw_leg("lm", leg_lm)

    leg_lb = [0] * 4
    leg_lb[0] = lb_rt
    cft_rot(coxia, femur, tibia, leg_lb, lb_angle, lb_c, lb_f, lb_t, total_rot_global)
    draw_leg("lb", leg_lb)

    leg_rb = [0] * 4
    leg_rb[0] = rb_rt

    cft_rot(coxia, femur, tibia, leg_rb, rb_angle, rb_c, rb_f, rb_t, total_rot_global)
    
    draw_leg("rb", leg_rb)

def set_legs_verts(legname, leg):
    bpy.data.objects[legname + "_coxia"].data.vertices[0].co = leg[0]
    bpy.data.objects[legname + "_coxia"].data.vertices[1].co = leg[1]
    bpy.data.objects[legname + "_femur"].data.vertices[0].co = leg[1]
    bpy.data.objects[legname + "_femur"].data.vertices[1].co = leg[2]
    bpy.data.objects[legname + "_tibia"].data.vertices[0].co = leg[2]
    bpy.data.objects[legname + "_tibia"].data.vertices[1].co = leg[3]

def change_pose(pose, front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z):

    leg_stance_dist = femur*math.sin(math.radians(leg_stance))

    body_xrot = Quaternion(axis=[1, 0, 0], angle=rot_x)
    body_yrot = Quaternion(axis=[0, 1, 0], angle=rot_y)
    body_zrot = Quaternion(axis=[0, 0, 1], angle=rot_z)
    total_rot_global = body_xrot * body_yrot * body_zrot 

    rm = (middle, 0.0, height)
    rf = (front, side, height)
    lf = (-front, side, height)
    lm = (-middle, 0.0, height)
    lb = (-front, -side, height)
    rb = (front, -side, height)

    rm_rt = tuple(tuple_quaternion_rot(rm, total_rot_global))
    rf_rt = tuple(tuple_quaternion_rot(rf, total_rot_global))
    lf_rt = tuple(tuple_quaternion_rot(lf, total_rot_global))
    lm_rt = tuple(tuple_quaternion_rot(lm, total_rot_global))
    lb_rt = tuple(tuple_quaternion_rot(lb, total_rot_global))
    rb_rt = tuple(tuple_quaternion_rot(rb, total_rot_global))

    rm_rt = add_tuple(rm_rt, (percent_x, percent_y, percent_z))
    rf_rt = add_tuple(rf_rt, (percent_x, percent_y, percent_z))
    lf_rt = add_tuple(lf_rt, (percent_x, percent_y, percent_z))
    lm_rt = add_tuple(lm_rt, (percent_x, percent_y, percent_z))
    lb_rt = add_tuple(lb_rt, (percent_x, percent_y, percent_z))
    rb_rt = add_tuple(rb_rt, (percent_x, percent_y, percent_z))

    rm_rt = add_tuple(rm_rt, (0, 0, -leg_stance_dist))
    rf_rt = add_tuple(rf_rt, (0, 0, -leg_stance_dist))
    lf_rt = add_tuple(lf_rt, (0, 0, -leg_stance_dist))
    lm_rt = add_tuple(lm_rt, (0, 0, -leg_stance_dist))
    lb_rt = add_tuple(lb_rt, (0, 0, -leg_stance_dist))
    rb_rt = add_tuple(rb_rt, (0, 0, -leg_stance_dist))
    
    bpy.data.objects["base"].data.vertices[0].co = rm_rt
    bpy.data.objects["base"].data.vertices[1].co = rf_rt
    bpy.data.objects["base"].data.vertices[2].co = lf_rt
    bpy.data.objects["base"].data.vertices[3].co = lm_rt
    bpy.data.objects["base"].data.vertices[4].co = lb_rt
    bpy.data.objects["base"].data.vertices[5].co = rb_rt
    
    # 0
    rm_angle = math.radians(0)
    rm_c = math.radians(pose[0]["coxia"])
    rm_f = math.radians(pose[0]["femur"])
    rm_t = math.radians(pose[0]["tibia"])
    
    # 45
    rf_angle = math.radians(45)
    rf_c = math.radians(pose[1]["coxia"])
    rf_f = math.radians(pose[1]["femur"])
    rf_t = math.radians(pose[1]["tibia"])
    
    # 135
    lf_angle = math.radians(135)
    lf_c = math.radians(pose[2]["coxia"])
    lf_f = math.radians(pose[2]["femur"])
    lf_t = math.radians(pose[2]["tibia"])
    
    # 180
    lm_angle = math.radians(180)
    lm_c = math.radians(pose[3]["coxia"])
    lm_f = math.radians(pose[3]["femur"])
    lm_t = math.radians(pose[3]["tibia"])
    
    # 225
    lb_angle = math.radians(225)
    lb_c = math.radians(pose[4]["coxia"])
    lb_f = math.radians(pose[4]["femur"])
    lb_t = math.radians(pose[4]["tibia"])
    
    # 315
    rb_angle = math.radians(315)
    rb_c = math.radians(pose[5]["coxia"])
    rb_f = math.radians(pose[5]["femur"])
    rb_t = math.radians(pose[5]["tibia"])
    
    # select leg and change leg to x pos
    
    leg_rm = [0] * 4
    leg_rm[0] = rm_rt
    cft_rot(coxia, femur, tibia, leg_rm, rm_angle, rm_c, rm_f, rm_t, total_rot_global)
    
    #print(leg_rm[0])
    #print(bpy.data.objects["rm_coxia"].data.vertices[0].co)
    set_legs_verts("rm", leg_rm)
    
    leg_rf = [0] * 4
    leg_rf[0] = rf_rt
    cft_rot(coxia, femur, tibia, leg_rf, rf_angle, rf_c, rf_f, rf_t, total_rot_global)
    set_legs_verts("rf", leg_rf)
    
    leg_lf = [0] * 4
    leg_lf[0] = lf_rt
    cft_rot(coxia, femur, tibia, leg_lf, lf_angle, lf_c, lf_f, lf_t, total_rot_global)
    set_legs_verts("lf", leg_lf)

    leg_lm = [0] * 4
    leg_lm[0] = lm_rt
    cft_rot(coxia, femur, tibia, leg_lm, lm_angle, lm_c, lm_f, lm_t, total_rot_global)
    set_legs_verts("lm", leg_lm)

    leg_lb = [0] * 4
    leg_lb[0] = lb_rt
    cft_rot(coxia, femur, tibia, leg_lb, lb_angle, lb_c, lb_f, lb_t, total_rot_global)
    set_legs_verts("lb", leg_lb)

    leg_rb = [0] * 4
    leg_rb[0] = rb_rt

    cft_rot(coxia, femur, tibia, leg_rb, rb_angle, rb_c, rb_f, rb_t, total_rot_global)
    
    set_legs_verts("rb", leg_rb)
    offset = [leg_rm, leg_rf, leg_lf, leg_lm, leg_lb, leg_rb]
    return offset

def change_pose_based_on_offset(offsets, pose, front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z):

    leg_stance_dist = femur*math.sin(math.radians(leg_stance))

    body_xrot = Quaternion(axis=[1, 0, 0], angle=rot_x)
    body_yrot = Quaternion(axis=[0, 1, 0], angle=rot_y)
    body_zrot = Quaternion(axis=[0, 0, 1], angle=rot_z)
    total_rot_global = body_xrot * body_yrot * body_zrot 

    rm = (middle, 0.0, height)
    rf = (front, side, height)
    lf = (-front, side, height)
    lm = (-middle, 0.0, height)
    lb = (-front, -side, height)
    rb = (front, -side, height)

    rm_rt = tuple(tuple_quaternion_rot(rm, total_rot_global))
    rf_rt = tuple(tuple_quaternion_rot(rf, total_rot_global))
    lf_rt = tuple(tuple_quaternion_rot(lf, total_rot_global))
    lm_rt = tuple(tuple_quaternion_rot(lm, total_rot_global))
    lb_rt = tuple(tuple_quaternion_rot(lb, total_rot_global))
    rb_rt = tuple(tuple_quaternion_rot(rb, total_rot_global))

    rm_rt = add_tuple(rm_rt, (percent_x, percent_y, percent_z))
    rf_rt = add_tuple(rf_rt, (percent_x, percent_y, percent_z))
    lf_rt = add_tuple(lf_rt, (percent_x, percent_y, percent_z))
    lm_rt = add_tuple(lm_rt, (percent_x, percent_y, percent_z))
    lb_rt = add_tuple(lb_rt, (percent_x, percent_y, percent_z))
    rb_rt = add_tuple(rb_rt, (percent_x, percent_y, percent_z))

    rm_rt = add_tuple(rm_rt, (0, 0, -leg_stance_dist))
    rf_rt = add_tuple(rf_rt, (0, 0, -leg_stance_dist))
    lf_rt = add_tuple(lf_rt, (0, 0, -leg_stance_dist))
    lm_rt = add_tuple(lm_rt, (0, 0, -leg_stance_dist))
    lb_rt = add_tuple(lb_rt, (0, 0, -leg_stance_dist))
    rb_rt = add_tuple(rb_rt, (0, 0, -leg_stance_dist))
    
#    tryadd = abs(list(offsets[0][0])[1])
    rm_rt_o = (add_tuple(rm_rt, (0, abs(list(offsets[0][0])[1]), 0)))
    rf_rt_o = (add_tuple(rf_rt, (0, abs(list(offsets[1][0])[1]), 0)))
#    lf_rt = (add_tuple(lf_rt, (0, abs(list(offsets[1][0])[1]), 0)))
#    lm_rt = (add_tuple(lm_rt, (0, abs(list(offsets[1][0])[1]), 0)))
#    lb_rt = (add_tuple(lb_rt, (0, abs(list(offsets[1][0])[1]), 0)))
    rb_rt_o = (add_tuple(rb_rt, (0, abs(list(offsets[5][0])[1]), 0)))
    #print(rm_rt)

    
    bpy.data.objects["base"].data.vertices[0].co = rm_rt#_o
    bpy.data.objects["base"].data.vertices[1].co = rf_rt#_o
    bpy.data.objects["base"].data.vertices[2].co = lf_rt
    bpy.data.objects["base"].data.vertices[3].co = lm_rt
    bpy.data.objects["base"].data.vertices[4].co = lb_rt
    bpy.data.objects["base"].data.vertices[5].co = rb_rt#_o
    
    # 0
    rm_angle = math.radians(0)
    rm_c = math.radians(pose[0]["coxia"])
    rm_f = math.radians(pose[0]["femur"])
    rm_t = math.radians(pose[0]["tibia"])
    
    # 45
    rf_angle = math.radians(45)
    rf_c = math.radians(pose[1]["coxia"])
    rf_f = math.radians(pose[1]["femur"])
    rf_t = math.radians(pose[1]["tibia"])
    
    # 135
    lf_angle = math.radians(135)
    lf_c = math.radians(pose[2]["coxia"])
    lf_f = math.radians(pose[2]["femur"])
    lf_t = math.radians(pose[2]["tibia"])
    
    # 180
    lm_angle = math.radians(180)
    lm_c = math.radians(pose[3]["coxia"])
    lm_f = math.radians(pose[3]["femur"])
    lm_t = math.radians(pose[3]["tibia"])
    
    # 225
    lb_angle = math.radians(225)
    lb_c = math.radians(pose[4]["coxia"])
    lb_f = math.radians(pose[4]["femur"])
    lb_t = math.radians(pose[4]["tibia"])
    
    # 315
    rb_angle = math.radians(315)
    rb_c = math.radians(pose[5]["coxia"])
    rb_f = math.radians(pose[5]["femur"])
    rb_t = math.radians(pose[5]["tibia"])
    
    # select leg and change leg to x pos
    
    leg_rm = [0] * 4
    leg_rm[0] = rm_rt
    cft_rot(coxia, femur, tibia, leg_rm, rm_angle, rm_c, rm_f, rm_t, total_rot_global)
    offset0 = subt_tuple(offsets[0][0], leg_rm[0])
    offset1 = subt_tuple(offsets[0][1], leg_rm[0])
    offset2 = subt_tuple(offsets[0][2], leg_rm[0])
    leg_rm[0] = add_tuple(leg_rm[0], (0, list(offsets[0][0])[1], 0))
    leg_rm[1] = add_tuple(leg_rm[1], (0, list(offsets[0][1])[1], 0))
    leg_rm[2] = add_tuple(leg_rm[2], (0, list(offsets[0][2])[1], 0))
    
    #print(leg_rm[0])
    #print(bpy.data.objects["rm_coxia"].data.vertices[0].co)
    set_legs_verts("rm", leg_rm)
    
    leg_rf = [0] * 4
    leg_rf[0] = rf_rt
    cft_rot(coxia, femur, tibia, leg_rf, rf_angle, rf_c, rf_f, rf_t, total_rot_global)
    leg_rf[0] = add_tuple(leg_rf[0], (0, list(offsets[1][0])[1], 0))
    leg_rf[1] = add_tuple(leg_rf[1], (0, list(offsets[1][1])[1], 0))
    leg_rf[2] = add_tuple(leg_rf[2], (0, list(offsets[1][2])[1], 0))
    set_legs_verts("rf", leg_rf)
    
    leg_lf = [0] * 4
    leg_lf[0] = lf_rt
    cft_rot_o(offsets[2], coxia, femur, tibia, leg_lf, lf_angle, lf_c, lf_f, lf_t, total_rot_global)
    set_legs_verts("lf", leg_lf)

    leg_lm = [0] * 4
    leg_lm[0] = lm_rt
    cft_rot_o(offsets[3], coxia, femur, tibia, leg_lm, lm_angle, lm_c, lm_f, lm_t, total_rot_global)
    set_legs_verts("lm", leg_lm)

    leg_lb = [0] * 4
    leg_lb[0] = lb_rt
    cft_rot_o(offsets[4], coxia, femur, tibia, leg_lb, lb_angle, lb_c, lb_f, lb_t, total_rot_global)
    set_legs_verts("lb", leg_lb)

    leg_rb = [0] * 4
    leg_rb[0] = rb_rt

    cft_rot(coxia, femur, tibia, leg_rb, rb_angle, rb_c, rb_f, rb_t, total_rot_global)
    leg_rb[0] = add_tuple(leg_rb[0], (0, list(offsets[5][0])[1], 0))
    leg_rb[1] = add_tuple(leg_rb[1], (0, list(offsets[5][1])[1], 0))
    leg_rb[2] = add_tuple(leg_rb[2], (0, list(offsets[5][2])[1], 0))
    
    set_legs_verts("rb", leg_rb)
    offset = [leg_rm, leg_rf, leg_lf, leg_lm, leg_lb, leg_rb]
    return offset

def change_pos_through_ik(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z):
    pose = get_ik(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    
    change_pose(pose, front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    
def anim_walk_gait_offsets(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode):
    poses = get_walk(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode)
    poses_sorted = {}
    for j in range(len(poses[0]["coxia"])):
        poses_sorted.update({j: {}})
        for i in range(6):
            poses_sorted[j].update({i: 
                {"coxia": poses[i]["coxia"][j],
                 "femur": poses[i]["femur"][j],
                 "tibia": poses[i]["tibia"][j]}})
#    pprint.pprint(poses)
#    pprint.pprint(poses_sorted)
#    for i in range(20):
#        print(poses_sorted[i][0]["coxia"])
    bpy.context.scene.frame_end = len(poses_sorted) * 2
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.scene.frame_set(0)
    offsets = change_pose(poses_sorted[0], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    bpy.ops.anim.insert_keyframe_animall()
    frame = 0
    for i in range(1, len(poses_sorted)):
        bpy.context.scene.frame_set(i)
        offsets = change_pose_based_on_offset(offsets, poses_sorted[i], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
        bpy.ops.anim.insert_keyframe_animall()
        frame += 1
    
    for i in range(0, len(poses_sorted)):
        bpy.context.scene.frame_set(frame)
        offsets = change_pose_based_on_offset(offsets, poses_sorted[i], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
        bpy.ops.anim.insert_keyframe_animall()
        frame += 1

def anim_walk_gait(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode):
    poses = get_walk(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode)
    poses_sorted = {}
    for j in range(len(poses[0]["coxia"])):
        poses_sorted.update({j: {}})
        for i in range(6):
            poses_sorted[j].update({i: 
                {"coxia": poses[i]["coxia"][j],
                 "femur": poses[i]["femur"][j],
                 "tibia": poses[i]["tibia"][j]}})
#    pprint.pprint(poses)
#    pprint.pprint(poses_sorted)
#    for i in range(20):
#        print(poses_sorted[i][0]["coxia"])
    bpy.context.scene.frame_end = len(poses_sorted) - 1
    #offsets = change_pose(poses_sorted[0], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    bpy.ops.object.select_all(action='SELECT')
#    change_pose(poses_sorted[1], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    for i in range(len(poses_sorted)):
        
        bpy.context.scene.frame_set(i)
        change_pose(poses_sorted[i], front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
        bpy.ops.anim.insert_keyframe_animall()

    
    
    
height = 1.0

front = 1
side = 1
middle = 1

coxia = 1
femur = 1
tibia = 1

hip_stance = 1.5

leg_stance = 1.5

percent_x = 0.05
percent_y = 0.05
percent_z = 0.05

rot_x = math.radians(1.5) # pitch
rot_y = math.radians(1.5) # roll
rot_z = math.radians(1.5) # yaw

body_xrot = Quaternion(axis=[1, 0, 0], angle=rot_x)
body_yrot = Quaternion(axis=[0, 1, 0], angle=rot_y)
body_zrot = Quaternion(axis=[0, 0, 1], angle=rot_z)
total_rot_global = body_xrot * body_yrot * body_zrot 
    
#draw_pose(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)
    
#change_pos_through_ik(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, percent_x, percent_y, percent_z, rot_x, rot_y, rot_z)

percent_x = 0
percent_y = 0
leg_stance = 0
hip_stance = 25
stepCount = 5
hipSwing = 25
liftSwing = 40

gaitType = "tripod"
walkMode = "walking"
#bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

anim_walk_gait_offsets(front, middle, side, coxia, femur, tibia, hip_stance, leg_stance, stepCount, hipSwing, liftSwing, percent_x, percent_z, rot_x, rot_y, gaitType, walkMode)
