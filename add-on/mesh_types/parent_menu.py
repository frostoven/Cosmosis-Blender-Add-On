import bpy


class CosmosisParentMenu(bpy.types.Menu):
    """Parent Menu for Cosmosis Mesh Types"""
    bl_idname = "VIEW3D_MT_cosmosis_parent_menu"
    bl_label = "Cosmosis Mesh Types"

    def draw(self, context):
        layout = self.layout

        # Check if a specific mesh type is selected
        selected_type = context.object.get("csmType", None)
        if selected_type:
            # Show the specific menu for the selected mesh type
            if selected_type == 'areaLight':
                layout.operator("object.area_light", text="Area Light")
            else:
                layout.operator("object.csm_unknown", text="CSM Unknown")

            # Add a button to clear the type information
            layout.operator("object.clear_mesh_type", text="Clear Type Info")
        else:
            # Show the main menu with options to select a mesh type
            layout.operator("object.csm_unknown", text="CSM Unknown")
            layout.operator("object.area_light", text="Area Light")
            layout.operator("object.clear_mesh_type", text="Clear Type Info")


def menu_func(self, context):
    self.layout.menu(CosmosisParentMenu.bl_idname)
