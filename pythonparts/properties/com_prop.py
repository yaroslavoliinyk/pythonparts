import NemAll_Python_BaseElements as AllplanBaseElements


def global_properties():
    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()
    return com_prop


def local_properties(build_ele):
    com_prop                    = AllplanBaseElements.CommonProperties()
    com_prop.Color              = build_ele.Color.value
    com_prop.ColorByLayer       = build_ele.ColorByLayer.value
    com_prop.Pen                = build_ele.Pen.value
    com_prop.PenByLayer         = build_ele.PenByLayer.value
    com_prop.Stroke             = build_ele.Stroke.value
    com_prop.StrokeByLayer      = build_ele.StrokeByLayer.value
    com_prop.Layer              = build_ele.Layer.value
    com_prop.use_global_props   = build_ele.UseGlobalProperties.value
    com_prop.HelpConstruction   = build_ele.UseConstructionLineMode.value
    return com_prop
