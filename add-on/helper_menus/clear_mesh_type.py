import bpy


class ClearMeshType(bpy.types.Operator):
    """
    This isn't by itself a mesh code. This used to clear mesh code information.
    """
    bl_idname = 'object.csm_clear_mesh_type'
    bl_label = 'Clear Type Info'
    bl_description = 'The "Clear Type Info" option is used to clear mesh code type info, and isn\'t itself a mesh code'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """
        Clears mesh code information from the selected object.
        """

        if context.object:
            if 'csmType' in context.object:
                del context.object['csmType']

        if 'csmAllCodes' in context.object:
            all_codes = list(context.object['csmAllCodes'])
            for key in all_codes:
                if key in context.object:
                    del context.object[key]
            del context.object['csmAllCodes']
        else:
            print('[CosmosisDev] Warning: Attempting to clear object that doesn\'t have "csmAllCodes" defined.')

        return {'FINISHED'}
