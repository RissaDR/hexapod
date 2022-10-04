import bpy

ob = bpy.data.objects["Cube"]
me = ob.data
print("faces:")
for face in me.faces:
    print(face)

print("
verts:")
for vert in me.vertices:
    new_location = vert.co
    new_location[0] = new_location[0] + 1   #X
    new_location[1] = new_location[1] + 1   #Y
    new_location[2] = new_location[2] + 1   #Z
    vert.co = new_location