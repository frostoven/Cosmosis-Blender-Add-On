import bpy
import re
from ..enabled_menu_items import enabled_menu_items


# Convert cameCase to snake_case.
# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
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
        selected_type = context.object.get('csmType', None)
        if selected_type:
            # We store types as camelCase. Convert to a snake_case to follow Blender standards.
            snake_name = to_snake_case(selected_type)

            # Show the specific menu for the selected mesh type.
            menu_object = layout.operator(
                f'object.csm_{snake_name}',
                icon='OUTLINER_DATA_GP_LAYER'  # or: GREASEPENCIL for a thicker icon
            )

            # This can happen if the plugin is out of date, or if a modder did something weird.
            if menu_object is None:
                layout.label(
                    text=f'Unknown mesh code type "{selected_type}"; is the plugin up to date?',
                    icon='ERROR'
                )

            # Add a button to clear the type information
            layout.operator('object.csm_clear_mesh_type', text='Clear Type Info', icon='PANEL_CLOSE')
        else:
            # Show all enable mesh code type menu items.
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


def menu_func(self, context):
    self.layout.menu(CosmosisParentMenu.bl_idname)
