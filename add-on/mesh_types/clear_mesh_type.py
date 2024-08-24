import bpy


class ClearMeshType(bpy.types.Operator):
    """
    This isn't by itself a mesh code. This used to clear mesh code information.
    """
    bl_idname = 'object.csm_clear_mesh_type'
    bl_label = 'Clear Type Info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Clear mesh code information from the selected object.
        if context.object:
            if 'csmType' in context.object:
                del context.object['csmType']

        return {'FINISHED'}
