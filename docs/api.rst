API
===

Public Interface
----------------


.. function:: create_scene(build_ele)

   Creates a canvas. All objects should be placed on Scene.

   :param build_ele: Given by Allplan ``BuildingElement`` object

   :return: :class:`Scene <Scene>` object

    Usage:

        >>> import pythonparts as pp
        >>> c = pp.create_cuboid(200, 1000, 100)
        >>> scene = pp.create_scene('build_ele')
        >>> scene.place(c)
        >>> scene
        Scene(children=[Cuboid(width=200, length=1000, height=100)]) 


.. function:: create_cuboid(width, length, height)

   Constructs :class:`Cuboid <Cuboid>` object with start global point = ``Point3D(0, 0, 0)``.

   :param width: Width of Cuboid. Goes along X axis in Allplan.
   :param length: Length of Cuboid. Goes along Y axis in Allplan.
   :param height: Height of Cuboid. Goes along Z axis in Allplan.

   :return: :class:`Cuboid <Cuboid>` object
   :rtype: pythonparts.Cuboid

   Usage:

      >>> import pythonparts as pp
      >>> c = pp.create_cuboid(200, 1000, 100)
      >>> c
      Cuboid(width=200, length=1000, height=100) 


.. function:: create_cuboid_from_pyp(pyp_name)

   Constructs :class:`Cuboid <Cuboid>` object fetching 
   width, length, and height from the according pyp file.

   :param pyp_name: According pyp file has to have three following parameters: 
   
                              - *pyp_name + 'Width'*
                              - *pyp_name + 'Length'*
                              - *pyp_name + 'Height'*

   :return: :class:`Cuboid <Cuboid>` object
   :rtype: pythonparts.Cuboid

   Inside pyp file::

      <Parameter>
         <Name>ColumnWidth</Name>
         <Text>Column Width</Text>
         <Value>200.</Value>
         <ValueType>Length</ValueType>
      </Parameter>
      
      <Parameter>
         <Name>ColumnLength</Name>
         <Text>Column Length</Text>
         <Value>1000.</Value>
         <ValueType>Length</ValueType>
      </Parameter>
      
      <Parameter>
         <Name>ColumnHeight</Name>
         <Text>Column Height</Text>
         <Value>100.</Value>
         <ValueType>Length</ValueType>
      </Parameter>

   Usage:

      >>> import pythonparts as pp
      >>> c = pp.create_cuboid_from_pyp('Column')
      >>> c
      Cuboid(width=200, length=1000, height=100)   


Classes
-------

.. autoclass:: pythonparts.geometry.Scene
   :members:
   :inherited-members:

.. autoclass:: pythonparts.geometry.Cuboid
   :members:
   :special-members: __init__
   :private-members: _children
   :inherited-members:
   