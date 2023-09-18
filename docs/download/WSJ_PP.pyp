<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PP_API\wsj_pp.py</Name>
        <Title>Joint</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Joint</Text>


        <Parameter>
            <Name>Separator1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnWidth</Name>
            <Text>Cuboid Width</Text>
            <Value>140.</Value>
            <MinValue>2</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnLength</Name>
            <Text>Cuboid Length</Text>
            <Value>3500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>SlabDist</Name>
            <Text>Distance to Slab</Text>
            <Value>1200.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator2</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>SlabWidth</Name>
            <Text>Slab Width</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>SlabHeight</Name>
            <Text>Slab Height</Text>
            <Value>300.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator2</Name>
            <ValueType>Separator</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>ColumnReinfConcreteGrade</Name>
            <Text>Concrete grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfConcreteGrade</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>ColumnReinfSteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfSteelGrade</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnReinfBendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4</Value>
            <ValueType>ReinfBendingRoller</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnHorLongbarsBotDiameter</Name>
            <Text>Bottom Longbars Diameter</Text>
            <Value>12</Value>
            <ValueType>ReinfBarDiameter</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>ColumnHorLongbarsBotCount</Name>
            <Text>Count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Parameter>

        
        <Parameter>
            <Name>Separator1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnHorLongbarsBotConcreteCoverFront</Name>
            <Text>Concrete cover - front</Text>
            <Value>30</Value>
            <ValueType>ReinfConcreteCover</ValueType>
        </Parameter>

        <Parameter>
            <Name>ColumnHorLongbarsBotConcreteCoverBack</Name>
            <Text>Concrete cover - back</Text>
            <Value>30</Value>
            <ValueType>ReinfConcreteCover</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>SelectShape</Name>
            <Text>Select Shape</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>Shape1RadioButton</Name>
                <Text>Shape 1</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            

            <Parameter>
                <Name>Shape2RadioButton</Name>
                <Text>Shape 2</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>


            <Parameter>
                <Name>Shape3RadioButton</Name>
                <Text>Shape 3</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>

            <Parameter>
                <Name>Shape4RadioButton</Name>
                <Text>Shape 4</Text>
                <Value>3</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>

           
        </Parameter>
    </Page>
</Element>
