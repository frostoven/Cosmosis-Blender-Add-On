import bpy

class CSMUndefined(bpy.types.Operator):
    """CSM Undefined"""
    bl_idname = 'object.csm_undefined'
    bl_label = 'Not Set'
    bl_options = {'REGISTER', 'UNDO'}

    csmType: bpy.props.StringProperty(
        name='Type',
        description='Not Set'
    )

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "csmType")
