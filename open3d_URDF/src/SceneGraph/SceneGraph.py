from .SceneNode import SceneNode
import open3d as o3d
import numpy as np

import pdb

class SceneGraph:
    def __init__(self, rootLink, joint_names, joint_angles):
        self.root = SceneNode()
        self.constructNode(self.root, rootLink, joint_names, joint_angles)
        self.joint_names = joint_names
        self.joint_angles = joint_angles

    def update(self):
        self.root.update()

    def getMesh(self):
        self.update()
        meshes = self.root.getMesh()
        new_meshes = []
        mesh_without_texture = o3d.geometry.TriangleMesh()
        for mesh in meshes:
            if mesh.has_textures() == True:
                new_meshes.append(mesh)
            else:
                mesh.paint_uniform_color([0.5,0.5,0.5])
                mesh_without_texture += mesh
        if len(mesh_without_texture.vertices) != 0:
            new_meshes.append(mesh_without_texture)
        return new_meshes

    def constructNode(self, node, link, joint_names, joint_angles):
        node.name = link.link.link_name
        node.joint = link.joint
        if node.joint != None:
            # Construct the joint node firstly; Deal with xyz and rpy of the node
            joint_xyz = node.joint.origin["xyz"]
            joint_rpy = node.joint.origin["rpy"]
            node.rotateXYZ(joint_rpy)
            node.translate(joint_xyz)
            if node.joint.joint_name in joint_names:
                angle = joint_angles[joint_names.index(node.joint.joint_name)]
                if angle == 0.0:
                    pass
                else:
                    if node.joint.joint_type == 'prismatic':
                        node.translate(node.joint.axis * angle)
                    else:
                        node.rotate(node.joint.axis, angle)
        # Construct the mesh nodes for multiple visuals in link
        visuals = link.link.visuals
        # pdb.set_trace()
        for visual in visuals:
            visual_node = SceneNode(node)
            node.addChild(visual_node)
            # visual_node.name = node.name + "_mesh:" + visual.visual_name
            visual_node.name = node.name + "_mesh"
            if visual.geometry_mesh["filename"] == None:
                raise RuntimeError("Invalid File path")
            visual_node.addMeshFile(visual.geometry_mesh["filename"])
            # Deal with xyz and rpy of the visual node
            visual_xyz = visual.origin["xyz"]
            visual_rpy = visual.origin["rpy"]
            visual_node.rotateXYZ(visual_rpy)
            visual_node.translate(visual_xyz)

        # Construct node for the children
        for child in link.children:
            child_node = SceneNode(node)
            node.addChild(child_node)
            self.constructNode(child_node, child, joint_names, joint_angles)
