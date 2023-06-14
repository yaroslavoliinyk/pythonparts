from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, Geom, GeomVertexFormat, GeomVertexData
from panda3d.core import GeomTriangles, GeomVertexWriter, GeomNode

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Create a vertex format.
        format = GeomVertexFormat.get_v3() # 3D vertices
        vdata = GeomVertexData('vertices', format, Geom.UH_static)

        # Create a Geom, this will hold our primitives.
        geom = Geom(vdata)
        
        # Create a writer, this will allow us to add vertices to the Geom.
        vertex = GeomVertexWriter(vdata, 'vertex')
        
        # Create a triangle primitive, this will draw our vertices.
        prim = GeomTriangles(Geom.UH_static)

        # Initialize vertex count
        self.vertex_count = 0

        def add_cube(pos, size):
            base = self.vertex_count
            for i in (-1, 1):
                for j in (-1, 1):
                    for k in (-1, 1):
                        # Perform scalar multiplication on each component
                        new_pos = Point3(pos.x + size * i, pos.y + size * j, pos.z + size * k)
                        vertex.addData3(new_pos)
                        self.vertex_count += 1
            for x in range(-1, 2, 2):
                for y in range(-1, 2, 2):
                    for z in range(-1, 2, 2):
                        prim.addVertices(base + 0, base + (1-x)*(1+y)*(1+z)//2, base + (1+x)*(1+y)*(1-z)//2)
                        prim.addVertices(base + 0, base + (1+x)*(1+y)*(1-z)//2, base + (1+x)*(1-y)*(1+z)//2)
                        prim.addVertices(base + 0, base + (1+x)*(1-y)*(1+z)//2, base + (1-x)*(1-y)*(1-z)//2)
                        prim.addVertices(base + 0, base + (1-x)*(1-y)*(1-z)//2, base + (1-x)*(1+y)*(1+z)//2)

        # add outer cube
        add_cube(Point3(0, 0, 0), 1)
        # add inner cube
        add_cube(Point3(0, 0, 0), 0.5)

        # Add the primitive to the Geom.
        geom.addPrimitive(prim)

        # Create a node, add the Geom, add the Node to the scene graph.
        node = GeomNode('gnode')
        node.addGeom(geom)
        self.render.attachNewNode(node)

app = MyApp()
app.run()
