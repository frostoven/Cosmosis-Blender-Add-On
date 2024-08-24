import bpy
from .mesh_types import csm_unknown, area_light, parent_menu, clear_mesh_type

bl_info = {
    "name": "CosmosisDev",
    "description": "Spaceship configuration add-on. To activate, click an "
                   "object and press Insert.",
    "author": "Frostoven contributors",
    "version": (0, 74, 0, 100, 1, 2, 0),
    "blender": (2, 80, 0),
    "location": "Object > Cosmosis Object Properties",
    "support": "OFFICIAL",
    "doc_url": "https://github.com/frostoven/Cosmosis-Blender-Add-On",
    "tracker_url": "https://github.com/frostoven/Cosmosis-Blender-Add-On/issues",
    "category": "Game Engine",
}

classes = [
    parent_menu.CosmosisParentMenu,
    csm_unknown.CSMUnknown,
    area_light.AreaLight,
    clear_mesh_type.ClearMeshType,
]

addon_keymaps = []

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Append the parent menu to the object menu
    bpy.types.VIEW3D_MT_object.append(parent_menu.menu_func)

    # Handle keymap registration
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu', 'INSERT', 'PRESS')
        kmi.properties.name = parent_menu.CosmosisParentMenu.bl_idname
        addon_keymaps.append((km, kmi))

def unregister():
    # Remove the parent menu from the object menu
    bpy.types.VIEW3D_MT_object.remove(parent_menu.menu_func)

    # Remove keymaps
    for km, kmi in reversed(addon_keymaps):
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
