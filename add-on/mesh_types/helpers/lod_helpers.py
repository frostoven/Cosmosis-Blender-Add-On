import bpy


class CreateLodGroupButton(bpy.types.Operator):
    bl_idname = 'object.csm_create_lod_group_button'
    bl_label = 'Creates a new LOD group'

    def execute(self, context):
        print('request to create triggered')
        return {'FINISHED'}


class RenameLodGroupButton(bpy.types.Operator):
    bl_idname = 'object.csm_rename_lod_group_button'
    bl_label = 'Renames the selected LOD group'

    def execute(self, context):
        print('request to rename triggered')
        return {'FINISHED'}
