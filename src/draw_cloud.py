# import bpy
import pandas as pd

df = pd.read_csv("/home/zoltanvarju/PycharmProjects/convertE57/data/converted/tehereloszto_points.tsv",
                 sep="\t")

for idx, row in df.iterrows():
    location = (row["X"], row["Y"], row["Z"])
    radius = 0.001
    bpy.ops.surface.primitive_nurbs_surface_sphere_add(
        radius=radius, location=location)
