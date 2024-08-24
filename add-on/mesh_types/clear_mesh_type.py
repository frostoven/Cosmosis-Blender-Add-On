import bpy


class ClearMeshType(bpy.types.Operator):
    """Clear Mesh Type Information"""
    bl_idname = 'object.clear_mesh_type'
    bl_label = 'Clear Type Info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Clear the type information from the selected object
        if context.object:
            if 'csmType' in context.object:
                del context.object['csmType']

        # Clear the mesh type from the scene properties
        context.scene["csmType"] = None

        return {'FINISHED'}
