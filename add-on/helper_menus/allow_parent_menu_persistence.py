import bpy


class AllowParentMenuRedraw(bpy.types.Operator):
    """This is a hack that allows the parent menu to stay open when we un/check 'Enable Adding Multiple Mesh Codes'"""
    bl_idname = 'object.csm_reshow_parent_menu'
    bl_label = 'Show Cosmosis Menu'

    def execute(self, context):
        context.area.tag_redraw()
        bpy.ops.wm.call_menu(name='VIEW3D_MT_cosmosis_parent_menu')
        return {'FINISHED'}


def init():
    def update_enable_multiple_mesh_codes(self, context):
        # Re-open the parent menu.
        context.area.tag_redraw()
        bpy.ops.object.csm_reshow_parent_menu()

    # This tracks whether or not to display options to add additional mesh codes.
    bpy.types.Scene.enable_multiple_mesh_codes = bpy.props.BoolProperty(
        name='Enable Adding Multiple Mesh Codes',
        description='Disabled by default to keep the UI minimal while editing objects',
        default=False,
        update=update_enable_multiple_mesh_codes
    )
