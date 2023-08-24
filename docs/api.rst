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

.. class:: pythonparts.geometry.Scene

   The `Scene` class represents a 3D scene and provides methods for adding model elements and
   reinforcement elements to the scene.
   
   .. property:: model_ele_list -> List[AllplanBasisElements.ModelElement3D]

      :return: Returns a list of AllplanBasisElements.ModelElement3D objects.

   .. property:: reinf_ele_list

      :return: a list of reinforcement elements.

   .. property:: pythonpart

      Creates a Python part by adding 2D/3D views and reinforcement elements to
      the model element list and then creating the Python part using the build element.
      :return: an instance of the PythonPart.

   .. function:: place(self, child_space: Space, center=False, **concov_sides)

      See explanation in :py:func:`pythonparts.geometry.Space.place`


.. class:: pythonparts.geometry.Cuboid
   
   Essentially a Polyhedron3D that's flexible because of child-parent relations with other ``Cuboid`` .
   Can be easily adjusted on a ``Scene`` and built or used as space/boundary for other objects(like Reinforcement).

   .. function:: __init__(self, width, length, height, global_start_pnt=None, com_prop=None)

      Assignes *width*, *length* and *height* of child objects :py:class:`pythonparts.geometry.Scene`,
      :py:class:`pythonparts.geometry.Cuboid`

      In future versions you will be able to *hide* or *subtract* ``Space`` objects

      :param width: Set a width of an object.
      :type width: float value >= 0.
      :param length: Set a length of an object.
      :type length: float value >= 0. 
      :param height: Set a length of an object.
      :type height: float value >= 0.
      :param global_start_pnt: Set Global Start Point on coordinate axis. If not set, it will be ``AllplanGeo.Point3D(0, 0, 0)`` 
      :type global_start_pnt: ``None`` or ``AllplanGeo.Point3D``

   .. property:: polyhedron

      :return: ``AllplanGeo.Polyhedron3D`` created with ``AllplanGeo.Polyhedron3D.CreateCuboid``

   .. property:: com_prop

      :return: Returning the basic set ``CommonProperties`` object of given ``Cuboid``
   
   .. property:: local

      :return: Local coordinates of this ``Space`` object.
      :rtype: :py:class:`pythonparts.geometry.coords.Coords`
   
   .. property:: global_

      :return: Global coordinates of this ``Space`` object.
      :rtype: :py:class:`pythonparts.geometry.coords.Coords`

   .. function:: build(self) -> List[AllplanBasisElements.ModelElement3D]

      Recursively builds a list of `AllplanBasisElements.ModelElement3D` objects for itselt
      and all its :py:func:`children <pythonparts.geometry.Space._children>`
      :return: a list of AllplanBasisElements.ModelElement3D objects.
   
   .. function:: place(self, child_space: "Space", center: bool=False, **concov_sides,)

      Position a child space inside a parent space, with options for
        centering and specifying the position of each side.

        :info: If you don't define *center* and *sides* , child global start point will be
            equal parent global start point.

        :param child_space: Represents the space that will be placed inside the parent space
        :type child_space: "Space"
        :param center: A boolean value indicating whether the child space should be centered within the
            parent space. If set to True, the left, front, and bottom shifts will be redefined by the
            center_calc function, defaults to False
        :type center: bool (optional)
        :type sides: 6 different sides that you can add to place child space inside parent:
            - left
            - right
            - front
            - back
            - top
            - bottom
        :type sides: float (optional)

        :warning: Opposite sides(*left* and *right*; *front* and *back*; *top* and *bottom*) 
            are not allowed to have values at same time.
        
        :Example:

            Let's first create two cubes. One with sides 200x200x200, another 1000x1000x1000:
                >>> import pythonparts as pp
                >>> small_cube = pp.create_cuboid(200, 200, 200)
                >>> big_cube = pp.create_cuboid(1000, 1000, 1000)

            And place small cube inside big one with left shift = 300

                >>> big_cube.place(small_cube, left=300)

            After creating scene inside ``create_element()`` and returning pythonpart, we 
            will obtain the following result:

                >>> def create_element(build_ele, doc):
                >>>     scene  = pp.create_scene(build_ele)
                >>>     scene.place(big_cube)
                >>>     return scene.pythonpart

            .. image:: images/place_001.png
                :alt: Resulting image with shift left=300

        :Example:

            If we place small cube inside very center, we will obtain the following:

                >>> big_cube.place(small_cube, center=True)

            ** Other code is the same **

            .. image:: images/place_002.png
                :alt: Centered cube
            
        :Example:

            Placing center and shift right=20 will give us:

                >>> big_cube.place(small_cube, center=Ture, right=20)

            ** Other code is the same **

            .. image:: images/place_003.png
                :alt: Center + right=20

        :Example:

            You can also adjust starting point, placing main object on a scene with parameters:

                >>> scene.place(big_cube, center=True, bottom=0)

            ** Other code is the same **

            .. image:: images/place_004_1.png
                :alt: Perspective view scene place settings

            .. image:: images/place_004_2.png
                :alt: Profile view scene place settings
   