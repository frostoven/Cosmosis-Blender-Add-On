import bpy


class CSMUnknown(bpy.types.Operator):
    """
    Used as a fallback if the plugin version is too old or the modder made an
    invalid manual edit to a mesh.
    """
    bl_idname = 'object.csm_unknown'
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
        layout.prop(self, 'csmType')
