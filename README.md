# yarn-fiber-generation

This code generates a parametric stockinette stitch pattern. This is the yarn-level geometry. It also generates the fibers that loop around the yarn.

See YarnCurve.pdf for the formulation. And see the stitchmesh paper on how this can be used.  
http://www.cs.cmu.edu/~kmcrane/Projects/Other/YarnCurve.pdf

Two generative interfaces are coded. 1) using jupyter lab, a .obj file is generated for the yarn, and another is generated for the fibers. These are polyline descriptions (of vertices and connectivities). 2) a grasshopper component is included to change the parameters and visualize the resulting fiber + yarn in Rhino 3D. 
