import bpy


class ClearMeshType(bpy.types.Operator):
    """
    This isn't by itself a mesh code. This used to clear mesh code information.
    """
    bl_idname = 'object.csm_clear_mesh_type'
    bl_label = 'Clear Type Info'
    bl_description = 'Deletes the data associated with this mesh code from the selected object'
    bl_options = {'REGISTER', 'UNDO'}

    deletion_target: bpy.props.StringProperty(
        default=''
    )

    def execute(self, context):
        """
        Clears mesh code information from the selected object.
        """
        if self.deletion_target == '':
            print('[CosmosisDev] Warning: deletion_target not correctly defined.')
            return {'CANCELLED'}

        if not context.object:
            print('[CosmosisDev] Warning: deletion failed: context.object is falsy.')
            return {'CANCELLED'}

        if 'csmMeshCodes' not in context.object:
            print('[CosmosisDev] Warning: deletion failed: "csmMeshCodes" not in context.object.')
            return {'CANCELLED'}

        if self.deletion_target not in context.object['csmMeshCodes']:
            print(f'[CosmosisDev] Warning: deletion failed: "{self.deletion_target}" not in csmMeshCodes object.')
            return {'CANCELLED'}

        del context.object['csmMeshCodes'][self.deletion_target]

        return {'CANCELLED'}
