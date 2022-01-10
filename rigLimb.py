import maya.cmds as mc
import nurbsControllers as nControl

class RigLimb:
    
    joints = []
    base_chain = []
    ik_chain = []
    fk_chain = []
    stretch_chain = []
    limb_control = ""
    
    def __init__(self, joints):
        
        self.joints = joints
        
    def createChain(self):
        
        # create ik chain; index 0 is base, index -1 is tip
        self.ik_chain = mc.duplicate(self.joints[-1], po=True, n=self.joints[-1] + "_IK")
        temp_joint = mc.listRelatives(self.joints[-1], p=True)
        
        x = 0
        while temp_joint[0] != self.joints[0]:
            dup_joint = mc.duplicate(temp_joint[0], po=True, n=temp_joint[0] + "_IK")
            self.ik_chain.append(dup_joint[0])
            mc.parent(self.ik_chain[x], self.ik_chain[x+1])
            x += 1
            temp_joint = mc.listRelatives(temp_joint[0], p=True)
        
        dup_joint = mc.duplicate(self.joints[0], po=True, n=self.joints[0] + "_IK")
        self.ik_chain.append(dup_joint[0])
        mc.parent(self.ik_chain[-2], self.ik_chain[-1])

        if mc.listRelatives(self.ik_chain[-1], p=True):
            mc.parent(self.ik_chain[-1], w=True)
            
        temp_grp = mc.CreateEmptyGroup()
        limb_grp = mc.rename(temp_grp, self.ik_chain[-1] + "_chain_GRP")
        mc.matchTransform(limb_grp, self.ik_chain[-1], pos=True)
        mc.parent(self.ik_chain[-1], limb_grp)
        
        # create fk chain by duplicating ik chain and renaming
        self.fk_chain = mc.duplicate(self.ik_chain, rc=True)
        x = 0
        for i in self.fk_chain:
            name = self.fk_chain[x].rstrip("_IK1")
            rename = mc.rename(self.fk_chain[x], name + "_FK")
            self.fk_chain[x] = rename
            x += 1
        
        temp_grp = mc.CreateEmptyGroup()
        limb_grp = mc.rename(temp_grp, self.fk_chain[-1] + "_chain_GRP")
        mc.matchTransform(limb_grp, self.fk_chain[-1], pos=True)
        mc.parent(self.fk_chain[-1], limb_grp)
        
        # create stretch chain by duplicating ik chain
        self.stretch_chain = mc.duplicate(self.ik_chain, rc=True)
        x = 0
        for i in self.stretch_chain:
            name = self.stretch_chain[x].rstrip("_IK1")
            rename = mc.rename(self.stretch_chain[x], name + "_STRETCH")
            self.stretch_chain[x] = rename
            x += 1
        
        temp_grp = mc.CreateEmptyGroup()
        limb_grp = mc.rename(temp_grp, self.stretch_chain[-1] + "_chain_GRP")
        mc.matchTransform(limb_grp, self.stretch_chain[-1], pos=True)
        mc.parent(self.stretch_chain[-1], limb_grp)
        
        # create base chain array (holds a reference to the bind skeleton)
        x = 0
        for i in self.ik_chain:
            name = self.ik_chain[x].rstrip("_IK")
            self.base_chain.append(name)
            x += 1
        
        # create ik fk blend nodes
        x = 0
        for i in self.base_chain:
            #matrix_blend = mc.createNode("blendMatrix", n=self.base_chain[x] + "_blendMatrix")
            #matrix_mult_TS = mc.shadingNode("multMatrix", au=True, n=self.base_chain[x] + "_multMatrix_TS")
            #matrix_mult_R = mc.shadingNode("multMatrix", au=True, n=self.base_chain[x] + "_multMatrix_R")
            #matrix_inverse = mc.shadingNode("inverseMatrix", au=True, n=self.base_chain[x] + "_invMatrix")
            #TS_decomp = mc.createNode("decomposeMatrix", n=self.base_chain[x] + "_TS_decomposeMatrix")
            #R_decomp = mc.createNode("decomposeMatrix", n=self.base_chain[x] + "_R_decomposeMatrix")
            constraint = mc.parentConstraint(self.fk_chain[x], self.ik_chain[x], self.base_chain[x], n=self.base_chain[x] + "_parentConstraint")
            mc.connectAttr(self.limb_control + ".IK_FK_Blend", constraint[0] + "." + self.ik_chain[x] + "W1")
            mc.connectAttr(self.limb_control + "_reverse.outputX", constraint[0] + "." + self.fk_chain[x] + "W0")
            x += 1
        
        # follows end joint; holds overall controls like IK/FK blend
    def createLimbControl(self):
        nControl.limb_CTRL(self.joints[-1])
        self.limb_control = self.joints[-1] + "_CTRL"
        mc.addAttr(self.limb_control, at="float", max=1, min=0, ln="IK_FK_Blend", k=True)
        limb_group = mc.group(n=self.limb_control + "_GRP")
        mc.pointConstraint(self.joints[-1], limb_group, n=limb_group + "_pointConstraint")
        mc.move(0, 0, -10, self.limb_control, r=True)
        
        #pick_matrix = mc.createNode("pickMatrix", n=self.limb_control + "_pickMatrix")
        #mc.setAttr(pick_matrix + ".useScale", False)
        #mc.setAttr(pick_matrix + ".useShear", False)
        #mc.setAttr(pick_matrix + ".useRotate", False)
        #mc.connectAttr(self.joints[-1] + ".worldMatrix[0]", pick_matrix + ".inputMatrix")
        #mc.connectAttr(pick_matrix + ".outputMatrix", self.limb_control + ".offsetParentMatrix")
        
        reverse_node = mc.shadingNode("reverse", au=True, n=self.limb_control + "_reverse")
        mc.connectAttr(self.limb_control + ".IK_FK_Blend", reverse_node + ".inputX")
        
    def createIkControl(self, limb, side, primaryAxis):
        if limb == "Arm":
            nControl.ik_arm_CTRL(self.ik_chain[0])
            ik_control = self.ik_chain[0] + "_CTRL"
            ik_control_grp = mc.group(ik_control, n=ik_control + "_GRP")
            mc.matchTransform(ik_control_grp, self.ik_chain[0], pos=True, rot=True)
        else:
            nControl.ik_leg_CTRL(self.ik_chain[0])
            ik_control = self.ik_chain[0] + "_CTRL"
            ik_control_grp = mc.group(ik_control, n=ik_control + "_GRP")
            mc.matchTransform(ik_control_grp, self.ik_chain[0], pos=True)
        mc.connectAttr(self.limb_control + ".IK_FK_Blend", ik_control_grp + ".visibility")
        mc.addAttr(ik_control, at="float", ln="Aim_Auto_Follow", k=True, max=1, min=0)
        
        pick_matrix = mc.createNode("pickMatrix", n=ik_control + "_pickMatrix")
        mc.setAttr(pick_matrix + ".useScale", False)
        mc.setAttr(pick_matrix + ".useShear", False)
        mc.setAttr(pick_matrix + ".useRotate", False)
        blend_matrix = mc.createNode("blendMatrix", n=ik_control + "_blendMatrix")
        mc.connectAttr(ik_control + ".matrix", pick_matrix + ".inputMatrix")
        mc.connectAttr(pick_matrix + ".outputMatrix", blend_matrix + ".target[0].targetMatrix")
        mc.connectAttr(ik_control + ".Aim_Auto_Follow", blend_matrix + ".envelope")
        
        mc.ikHandle(sj=self.ik_chain[-1], ee=self.ik_chain[0], sol="ikRPsolver", n=self.ik_chain[0] + "_ikHandle")
        mc.parent(self.ik_chain[0] + "_ikHandle", ik_control)
        
        nControl.pole_vector_CTRL(self.base_chain[-2] + "_aim")
        pole_vector_control = self.base_chain[-2] + "_aim_CTRL"
        pole_vector_control_grp = mc.group(pole_vector_control, n=pole_vector_control + "_GRP")
        mc.matchTransform(pole_vector_control_grp, self.base_chain[-2], pos=True, rot=True)
        mc.poleVectorConstraint(pole_vector_control, self.ik_chain[0] + "_ikHandle")
        mc.connectAttr(blend_matrix + ".outputMatrix", pole_vector_control + ".offsetParentMatrix")
        mc.connectAttr(self.limb_control + ".IK_FK_Blend", pole_vector_control_grp + ".visibility")
        
        nControl.square_CTRL(self.ik_chain[-1])
        shoulder_control = self.ik_chain[-1] + "_CTRL"
        shoulder_control_grp = mc.group(shoulder_control, n=shoulder_control + "_GRP")
        mc.matchTransform(shoulder_control_grp, self.base_chain[-1], pos=True, rot=True)
        mc.parentConstraint(shoulder_control, self.ik_chain[-1], n=self.ik_chain[-1] + "_parentConstraint")
        mc.connectAttr(self.limb_control + ".IK_FK_Blend", shoulder_control_grp + ".visibility")
        
        if side == "Right":
            mc.select(pole_vector_control_grp, r=True)
            mc.select(shoulder_control_grp, add=True)
            mc.scale(-1, -1, -1)
            mc.select(ik_control_grp, r=True)
            if limb == "Leg":
                mc.scale(-1, 1, 1)
            else:
                mc.scale(-1, -1, -1)
    
    def createFkControl(self, side, primaryAxis):
        normal = [1, 0, 0]
        if primaryAxis == "y":
            normal = [0, 1, 0]
        elif primaryAxis == "z":
            normal = [0, 0, 1]
        
        temp_control = mc.circle(nr=normal, n=self.fk_chain[0] + "_CTRL")
        temp_control_grp = mc.group(temp_control[0], n=temp_control[0] + "_GRP")
        mc.matchTransform(temp_control_grp, self.fk_chain[0])
        mc.parentConstraint(temp_control[0], self.fk_chain[0], n = self.fk_chain[0] + "_parentConstraint")
        x = 1
        while True:
            control = mc.circle(nr=normal, n=self.fk_chain[x] + "_CTRL")
            control_grp = mc.group(control[0], n=control[0] + "_GRP")
            mc.matchTransform(control_grp, self.fk_chain[x])
            if side == "Right":
                mc.select(control_grp, r=True)
                mc.scale(-1, -1, -1)
            mc.parentConstraint(control[0], self.fk_chain[x], n=self.fk_chain[x] + "_parentConstraint")
            mc.parent(temp_control_grp, control[0])
            temp_control_grp = control_grp
            if self.fk_chain[x] == self.fk_chain[-1]:
                break
            x += 1
        mc.connectAttr(self.limb_control + "_reverse.outputX", temp_control_grp + ".visibility")
    
    def createLimbRigWindow(self):
        
        side=""
        limb=""
        windowID = "rigWindow"
        
        if mc.window(windowID, ex=True):
            mc.deleteUI(windowID)
            
        def cancelCallback(*args):
            if mc.window(windowID, ex=True):
                mc.deleteUI(windowID)
        
        def applyCallback(*args):
            rig_limb.createLimbControl()
            rig_limb.createChain()
            side = mc.optionMenu(side_menu, q=True, v=True)
            limb = mc.optionMenu(limb_menu, q=True, v=True)
            primaryAxis = mc.optionMenu(primary_axis_menu, q=True, v=True)
            rig_limb.createIkControl(limb, side, primaryAxis)
            rig_limb.createFkControl(side, primaryAxis)
            mc.deleteUI(windowID, window=True)
            
        myWindow = mc.window(windowID, title="Limb Creation", width=300, height=100)
        mc.columnLayout()
        mc.columnLayout(columnAttach=["left", 40], rowSpacing=5)
        mc.separator(height=20, style="none")
        
        side_menu = mc.optionMenu(label="Side:")
        mc.menuItem(label="Left", data=0)
        mc.menuItem(label="Right", data=1)
        
        limb_menu = mc.optionMenu(label="Limb:")
        mc.menuItem(label="Arm", data=0)
        mc.menuItem(label="Leg", data=1)
        
        primary_axis_menu = mc.optionMenu(l="Primary Axis:")
        mc.menuItem(label="x", data=0)
        mc.menuItem(label="y", data=1)
        mc.menuItem(label="z", data=2)
        
        mc.separator(height=20, style="none")
        mc.setParent("..")
        mc.rowLayout(numberOfColumns=2)
        mc.button(label="Apply", command=applyCallback)
        mc.button(label="Cancel", command=cancelCallback)
        
        mc.showWindow(myWindow)

selection = mc.ls(sl=True)
rig_limb = RigLimb(selection)
rig_limb.createLimbRigWindow()