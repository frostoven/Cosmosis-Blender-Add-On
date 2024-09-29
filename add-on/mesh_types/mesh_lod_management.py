import bpy
import re


def get_lod_groups():
    if 'csm_lod_cache' not in bpy.context.scene:
        return (('Detached (Not in Group)', 'Loading...', ''))

    lod_cache = bpy.context.scene['csm_lod_cache']
    return tuple((key, key, '') for key in lod_cache.keys())


class MeshLodManagement(bpy.types.Operator):
    """
    Manages scene LODs. LODs are a bit different from other mesh codes in that LODs are a group of objects rather than
    an object owning the mesh code.
    """
    bl_idname = 'object.csm_lod_management'
    bl_label = 'LOD Configuration'
    bl_description = (
        'Manages mesh LOD groups'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'FILE_VOLUME'
    mesh_code = 'lod'

    csmLodGroup: bpy.props.EnumProperty(
        name='',
        description='',
        items=lambda self, context: get_lod_groups()
    )

    def invoke(self, context, event):
        print('invocation')

    def execute(self, context):
        if 'csm_lod_cache' not in context.scene:
            context.scene['csm_lod_cache'] = {
                'Detached (Not in Group)': ['']
            }
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.label(text='Showing LOD Group:')
        layout.prop(self, 'csmLodGroup')

        layout.operator('object.csm_create_lod_group_button', text='Create New LOD Group')
        layout.operator('object.csm_rename_lod_group_button', text='Rename This LOD Group')

        layout.use_property_split = True
