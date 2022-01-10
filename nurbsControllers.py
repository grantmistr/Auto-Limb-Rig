import maya.cmds as mc

def ik_arm_CTRL(name="temp_name"):
    crv1 = mc.curve(d=1, p=[(0, 0, 3), (0, 2, 2), (0, 3, 0), (0, 2, -2), (0, 0, -3), (0, -2, -2), (0, -3, 0), (0, -2, 2), (0, 0, 3)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8], name=name + "_CTRL")
    crv_shapes = mc.listRelatives(shapes=True)
    mc.rename(crv_shapes[0], name + "_CTRLShape")
    crv2 = mc.duplicate(name=name + "_CTRL_temp")
    mc.rotate(45, 0, 0)
    mc.scale(1.06, 1.06, 1.06)
    mc.makeIdentity(apply=True, rotate=True, scale=True)
    crv_shapes = mc.listRelatives(shapes=True)
    mc.rename(crv_shapes[0], name + "_CTRL_tempShape")
    mc.parent(crv_shapes[0], crv1, shape=True, relative=True)
    mc.delete(crv2)
    mc.delete(crv1, constructionHistory=True)

def ik_leg_CTRL(name="temp_name"):
	crv1 = mc.curve(d=1, p=[(-1, 0, 2), (-1, 0, -1), (1, 0, -1), (1, 0, 2), (-1, 0, 2)], k=[0, 1, 2, 3, 4], name=name + "_CTRL")
	crv_shapes = mc.listRelatives(shapes=True)
	mc.rename(crv_shapes[0], name + "_CTRLShape")
	mc.delete(crv1, constructionHistory=True)
	mc.CenterPivot()

def pole_vector_CTRL(name="temp_name"):
    crv1 = mc.curve(d=1, p=[(-1, 0, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1), (0, 1.25, 0), (-1, 0, -1), (1, 0, -1), (0, 1.25, 0), (1, 0, 1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name=name + "_CTRL")
    crv_shapes = mc.listRelatives(shapes=True)
    mc.rename(crv_shapes[0], name + "_CTRLShape")
    crv2 = mc.curve(d=1, p=[(-1, 0, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1), (0, -1.25, 0), (-1, 0, -1), (1, 0, -1), (0, -1.25, 0), (1, 0, 1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name=name + "_CTRL_temp")
    crv_shapes = mc.listRelatives(shapes=True)
    temp_crv = mc.rename(crv_shapes[0], name + "_CTRL_tempShape")
    mc.parent(temp_crv, crv1, shape=True, relative=True)
    mc.delete(crv2)
    mc.delete(crv1, constructionHistory=True)

def limb_CTRL(name="temp_name"):
	crv1 = mc.curve(d=1, p=[(3, 0, 0), (0, 1, 0), (-3, 0, 0), (0, -1, 0), (3, 0, 0)], k=[0, 1, 2, 3, 4], n=name + "_CTRL")
	crv_shape = mc.listRelatives(s=True)
	mc.rename(crv_shape[0], name + "_CTRLShape")
	crv2 = mc.curve(d=1, p=[(4, 0, 0), (0, 1.5, 0), (-4, 0, 0), (0, -1.5, 0), (4, 0, 0)], k=[0, 1, 2, 3, 4], n=name + "_CTRL")
	crv_shape = mc.listRelatives(s=True)
	crv_temp_shape = mc.rename(crv_shape[0], name + "_CTRLShape2")
	mc.parent(crv_temp_shape, crv1, s=True, r=True)
	mc.delete(crv2)
	mc.delete(crv1, constructionHistory=True)

def square_CTRL(name="temp_name"):
	crv1 = mc.curve(d=1, p=[(-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)], k=[0, 1, 2, 3, 4], n=name + "_CTRL")
	crv_shapes = mc.listRelatives(shapes=True)
	mc.rename(crv_shapes[0], name + "_CTRLShape")
	mc.delete(crv1, constructionHistory=True)