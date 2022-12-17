import bpy

bl_info = {
    "name": "CosmosisDev",
    "blender": (2, 80, 0),
    "category": "Object",
}

mesh_codes = []
code_menu_items = {}

mesh_codes.append(('undefined', 'Please select...', ''))
code_menu_items['undefined'] = []

mesh_codes.append(('areaLight', 'Area light', ''))
code_menu_items['areaLight'] = []
code_menu_items['areaLight'] = ['moduleHook', 'gfxqLight']


class ObjectCosmosisObjectProperties(bpy.types.Operator):
    """Cosmosis Object Properties"""
    bl_idname = 'object.cosmosis_object_properties'
    bl_label = 'Cosmosis Object Properties'
    bl_options = {'REGISTER', 'UNDO'}

    # --- Optional menu items section --- #

    # int example: bpy.props.IntProperty(name="", default=2, min=1, max=100)

    moduleHook: bpy.props.StringProperty(
        name="[Module hook]",
        description="Optional; examples: cockpitLights | externalLights"
    )

    gfxqLight: bpy.props.EnumProperty(
        name="[Lighting quality]",
        description="Used to prevent the light from rendering on certain GFX quality settings",
        items=(
            ('auto', 'Engine decides', ''),
            ('low', 'Only render if low quality', ''),
            ('low,medium', 'Only render if medium or lower quality', ''),
            ('medium', 'Only render if medium quality', ''),
            ('medium,high', 'Only render if medium or higher quality', ''),
            ('high', 'Only render if high quality', ''),
        )
    )

    # --- Optional menu items section end --- #

    obj_type: bpy.props.EnumProperty(
        name='Type',
        items=mesh_codes
    )

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location
        obj = context.active_object

        # Set object properties to the user-chosen type
        if self.obj_type == 'undefined' and "type" in context.object:
            del context.object['type']
        else:
            context.object['type'] = self.obj_type

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        # Always dray obj_type by default.
        layout.prop(self, 'obj_type')

        active_type = self.obj_type
        menu_items = code_menu_items[active_type]
        if len(menu_items) > 0:
            layout.label(text='Preferences')

        # Only draw menu items relevant to the selected type.
        for menu_item in menu_items:
            if menu_item == 'obj_type':
                # Disallow drawing obj_type a second time.
                continue
            # Draw the menu item.
            layout.prop(self, menu_item)

def menu_func(self, context):
    self.layout.operator(ObjectCosmosisObjectProperties.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ObjectCosmosisObjectProperties)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not
    # available either, so we have to check this to avoid nasty errors in
    # background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode',
                                             space_type='EMPTY')
        kmi = km.keymap_items.new(ObjectCosmosisObjectProperties.bl_idname,
                                  'INSERT', 'PRESS', ctrl=False, shift=False)
        kmi.properties.obj_type = 'undefined'
        addon_keymaps.append((km, kmi))


def unregister():
    # Note: when unregistering, it's usually good practice to do it in
    # reverse order you registered. Can avoid strange issues like keymap
    # still referring to operators already unregistered... handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(ObjectCosmosisObjectProperties)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == '__main__':
    register()
