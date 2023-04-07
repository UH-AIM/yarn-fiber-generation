# yarn-fiber-generation

This code generates a parametric stockinette stitch pattern. This is the yarn-level geometry. It also generates the fibers that loop around the yarn.
/Users/tianchen/Library/CloudStorage/GoogleDrive-tianchen@uh.edu/.shortcut-targets-by-id/1fUusdMQzmNoBHwGgva_msJB-zcjFe1Ad/Haptic knits/Modeling/yarn_fiber_generation/readme.txt
See YarnCurve.pdf for the formulation. And see the stitchmesh paper on how this can be used.  

Two generative interfaces are coded. 1) using jupyter lab, a .obj file is generated for the yarn, and another is generated for the fibers. These are polyline descriptions (of vertices and connectivities).

2) a grasshopper component is included to change the parameters and visualize the resulting fiber + yarn in Rhino 3D. 
