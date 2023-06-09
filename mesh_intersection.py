# This script uses trimesh as the main tool for processing the intersections.
# The lists are imported from blender and in here are reformatted as numpy arrays.
# The meshes are in GLB format as per recommended by trimesh on their website.

"""
Fragment of code that identifies the intersection point between the site
and rays with origin on a grid stationed above the bounds of the site.
The script works outside the frame of blender.
"""

import trimesh
import numpy as np

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research/"
# Constants

# load data from blender grid origin
top_grid_vtx = np.load(blender_file_path + 'top_grid_vtx.npy')

# function for generating intersection vtx  with trimesh


def intersection_trimesh(top_grid_vtx_input, blender_file_path_input):

    # import mesh representing the site from blender
    mesh_input = trimesh.load(blender_file_path_input + '/terrain.glb', force='mesh')

    # load data from blender grid origin
    top_data = top_grid_vtx_input

    # create some rays and find the intersection "rays - site"

    if mesh_input and top_data is not None:
        ray_origins = np.array(top_data)
        # print(ray_origins)
        # ray_directions pointing down
        ray_directions = np.array([[0, 0, -1]] * int(len(ray_origins)))

        # run trimesh to find the intersection between the rays and site
        locations, index_ray, index_tri = mesh_input.ray.intersects_location(

            ray_origins=ray_origins,
            ray_directions=ray_directions)

        # sorting the intersections based on the index of the rays to follow the order of the grid

        locations = np.array(locations)

        index_ray = np.array(index_ray)
        inds = index_ray.argsort()
        vtx_intersection_trimesh = locations[inds]

        # Verification
        if len(vtx_intersection_trimesh) == len(top_data):
            print(f"number of intersections ({str(len(vtx_intersection_trimesh))}) coincides with "
                  f"the number of grid vertex ({str(len(top_data))})")
            # saving the intersections as "vtx_intersection.npy" file
            np.save(blender_file_path_input + '/vtx_intersection', vtx_intersection_trimesh)
            print("vtx_intersection successfully saved as vtx_intersection.npy")

        else:
            print(f"number of intersections ({str(len(vtx_intersection_trimesh))}) doesn't coincide with "
                  f"the number of grid vertex ({str(len(top_data))})")
    else:
        print("mesh and data not found")

    return vtx_intersection_trimesh


vtx_intersection = intersection_trimesh(top_grid_vtx, blender_file_path)
