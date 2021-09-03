#!/usr/bin/env python3

from src import  URDFParser, URDFTree, SceneGraph


import pdb
import open3d as o3d

if __name__ == "__main__":
    URDF_file = "/home/rocky/moveit_vkc_ws/src/robot_description/husky_ur_description/open3d/blender_use_2.urdf"
    # Parse the URDF file
    parser = URDFParser(URDF_file)
    parser.parse()
    # Construct the URDF tree
    links = parser.links
    joints = parser.joints
    tree = URDFTree(links, joints)
    # Construct the scene graph
    scene = SceneGraph(tree.root)
    mesh = scene.getMesh()
    # mesh.paint_uniform_color([0.5, 0.5, 0.5])
    print(mesh)
    o3d.visualization.draw_geometries(mesh)