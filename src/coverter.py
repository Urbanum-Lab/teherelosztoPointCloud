import numpy as np
import open3d as o3d
import pandas as pd
import pye57

cartesianXs = np.empty([0,0], float)
cartesianYs = np.empty([0,0], float)
cartesianZs = np.empty([0,0], float)
intensities = np.empty([0,0], float)

e57 = pye57.E57("data/raw/OVT_2020_AC_optimized.e57")
for i in range(e57.scan_count):
    try:
        data = e57.read_scan_raw(i)
        header = e57.get_header(i)
        cartesianXs = np.append(cartesianXs, data["cartesianX"])
        cartesianYs = np.append(cartesianYs, data["cartesianY"])
        cartesianZs = np.append(cartesianZs, data["cartesianZ"])
        intensities = np.append(intensities, data["intensity"])
    except Exception as e:
        print(e)
        continue

# assert len(cartesianXs) == len(cartesianYs) == len(cartesianZs) == len(intensities)
print("assert finished")
data = {}
data["cartesianX"] = cartesianXs
data["cartesianY"] = cartesianYs
data["cartesianZ"] = cartesianZs
data["intensity"] = intensities
print("data dict is ready")

df = pd.DataFrame(data)
df.drop_duplicates(inplace=True, subset=["cartesianX", "cartesianY", "cartesianZ"]) # just check if we have duplicates
print("deduped")
# grayscale_values = pd.to_numeric(df["intensity"], downcast="integer")
# df["intensity"] = grayscale_values
rgb_values = np.array([[e/255.0]*3 for e in df["intensity"]])
print("rgb values are ready")

df.to_csv("data/converted/tehereloszto_points.tsv", index=False)
print("ascii data saved")
#
xyz = df.drop(["intensity"], axis=1).to_numpy()
print("xyz is ready")

device = o3d.core.Device("CUDA:0")
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)
pcd.colors = o3d.utility.Vector3dVector(rgb_values)

lower = pcd.uniform_down_sample(5)
print("filtered")

o3d.io.write_point_cloud("data/converted/tehereloszto_full.ply", pcd)
o3d.io.write_point_cloud("data/converted/tehereloszto_sample.ply", lower)
print("ply saved")
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(lower, voxel_size=0.15)
print("voxel is ready")
o3d.io.write_voxel_grid("data/converted/tehereloszto_voxel.ply", voxel_grid)
print("voxel saved")
# vis = o3d.visualization.Visualizer()
#
# # Create a window, name it and scale it
# # Add the voxel grid to the visualizer
# vis.create_window(window_name='Bunny Visualize', width=1600, height=1200)
# vis.add_geometry(voxel_grid)
#
# # We run the visualizater
# vis.run()# new_data = {}
# # new_data["cartesianX"] = df["cartesianX"]
# # new_data["cartesianY"] = df["cartesianY"]
# # new_data["cartesianZ"] = df["cartesianZ"]
# # new_data["intensity"] = df["intensity"]
# #
#
# # Once the visualizer is closed destroy the window and clean up
# vis.destroy_window()
