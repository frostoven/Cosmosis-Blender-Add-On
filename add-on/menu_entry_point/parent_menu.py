import bpy
import re

from ..enabled_menu_items import enabled_menu_items


# Convert camelCase to snake_case.
def to_snake_case(str_name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', str_name).lower()


class CosmosisParentMenu(bpy.types.Menu):
    """
    Parent Menu for Cosmosis Mesh Types
    """
    bl_idname = 'VIEW3D_MT_cosmosis_parent_menu'
    bl_label = 'Cosmosis Mesh Types'
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout

        # Check if a specific mesh type is selected.
        mesh_codes = context.object.get('csmMeshCodes', None)
        if mesh_codes:
            self.draw_edit_existing(context, mesh_codes)

        else:
            self.draw_create_new(context)

    def draw_create_new(self, context):
        layout = self.layout
        scene = context.scene

        # Show all enabled mesh code type menu items.
        layout.label(
            text='Type to search...',
            icon='VIEWZOOM'
        )
        layout.separator()
        for menu_item in enabled_menu_items:
            if menu_item == 'separator':
                layout.separator()
            else:
                layout.operator(menu_item.bl_idname, icon=menu_item.icon)

    def draw_edit_existing(self, context, mesh_codes):
        layout = self.layout
        scene = context.scene
        for mesh_code in mesh_codes:
            # We store types as camelCase. Convert to a snake_case to follow Blender standards.
            snake_name = to_snake_case(mesh_code)
            op_idname = f'object.csm_{snake_name}'

            # Create a row for each mesh code.
            row = layout.row(align=True)

            # Draw the edit button.
            col1 = row.column(align=True)
            edit_button = row.column(align=True).operator(
                op_idname,
                icon='OUTLINER_DATA_GP_LAYER'  # or: GREASEPENCIL for a thicker icon
            )

            # This can happen if the plugin is out of date, or if a modder did something weird.
            if edit_button is None:
                col1.scale_x = 1.5
                col1.label(
                    text=f'Unknown mesh code type "{mesh_code}"; is the plugin up to date?',
                    icon='ERROR'
                )

            # For some reason using a separator looks glitchy, so we're using a label instead.
            col2 = row.column(align=True)
            col2.scale_x = 0.4
            col2.label(text=' ')

            # Draw the delete button.
            col3 = row.column(align=True)
            col3.scale_x = 0.65
            col3.operator(
                'object.csm_trigger_type_deletion',
                text='Delete',
                icon='TRASH'
            ).deletion_target = mesh_code

            layout.separator()

        # This is a checkbox. It's unchecked by default. If checked, allows the user to add multiple mesh codes to one
        # object.
        row = layout.row()
        row.prop(
            scene,
            'enable_multiple_mesh_codes',
            text='Enable Adding Multiple Mesh Codes',
        )

        # Show add-new mesh codes menu if the above checkbox is checked.
        if scene.enable_multiple_mesh_codes:
            layout.separator()
            self.draw_create_new(context)


def menu_func(self, context):
    self.layout.menu(CosmosisParentMenu.bl_idname)
