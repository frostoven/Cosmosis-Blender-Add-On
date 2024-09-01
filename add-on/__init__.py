import bpy
from .enabled_menu_items import enabled_menu_items
from .helper_menus import allow_parent_menu_persistence, parent_menu, clear_mesh_type

bl_info = {
    "name": "CosmosisDev",
    "description": "Spaceship configuration add-on. To activate, click an object and press Insert.",
    "author": "Frostoven contributors",
    "version": (0, 74, 0, 100, 1, 2, 0),
    "blender": (2, 80, 0),
    "location": "Object > Cosmosis Object Properties",
    "support": "OFFICIAL",
    "doc_url": "https://github.com/frostoven/Cosmosis-Blender-Add-On",
    "tracker_url": "https://github.com/frostoven/Cosmosis-Blender-Add-On/issues",
    "category": "Game Engine",
}

addon_keymaps = []

allow_parent_menu_persistence.init()


def register():
    # This menu shows all available mesh code types when the user presses Insert.
    bpy.utils.register_class(parent_menu.CosmosisParentMenu)
    bpy.utils.register_class(allow_parent_menu_persistence.AllowParentMenuRedraw)

    # Register all enabled menu items.
    for menu_item in enabled_menu_items:
        # We skip strings; they're used special commands in the parent menu.
        if not isinstance(menu_item, str):
            bpy.utils.register_class(menu_item)

    # This menu allows clearing type information.
    bpy.utils.register_class(clear_mesh_type.ClearMeshType)

    # Append the parent menu to the object menu.
    bpy.types.VIEW3D_MT_object.append(parent_menu.menu_func)

    # Handle keymap registration.
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu', 'INSERT', 'PRESS')
        kmi.properties.name = parent_menu.CosmosisParentMenu.bl_idname
        addon_keymaps.append((km, kmi))


def unregister():
    # Remove the parent menu from the object menu.
    bpy.types.VIEW3D_MT_object.remove(parent_menu.menu_func)

    # Remove keymaps.
    for km, kmi in reversed(addon_keymaps):
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Unregister menu items.
    for menu_item in reversed(enabled_menu_items):
        # We skip strings; they're used special commands in the parent menu.
        if not isinstance(menu_item, str):
            bpy.utils.unregister_class(menu_item)


if __name__ == "__main__":
    register()
