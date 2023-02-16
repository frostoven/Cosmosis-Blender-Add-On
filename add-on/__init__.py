import bpy

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
    "tracker_url": "https://github.com/frostoven/Cosmosis-Blender-Add-On/issues", # noqa
    "category": "Game Engine",
}

# This is the dropdown that contains all mesh types.
mesh_code_types = []

# All menu items are disabled by default. This informs the menu builder
# which items should be visible for the given mesh code type.
required_menu_items = {}

# All menu items are disabled by default. This informs the menu builder
# which items should be visible for the given mesh code type.
optional_menu_items = {}

# Used to load mesh properties into the plugin.
allowed_external_keys = [
    'csmType', 'csmModuleHook', 'csmGfxqLight'
]

# -------------------------------------------------- #
# --- Mesh definitions and in-application manual --- #
# -------------------------------------------------- #

# Structure:
# menu_items['value__mesh_code'] = ['key__menu_item', 'key__menu_item']
# mesh_code_types.append(('game_engine_type', 'Friendly text', 'tooltip'))

required_menu_items['csmUndefined'] = []
optional_menu_items['csmUndefined'] = []
mesh_code_types.append(('csmUndefined', 'Not set', """
You may choose one of the dropdown items to specify that the game engine should deal with this component specially.
"""[1:-1]))  # noqa

# -------------------------------------------------- #

required_menu_items['areaLight'] = []
optional_menu_items['areaLight'] = ['csmModuleHook', 'csmGfxqLight',
                                    'csmDevHelper']
mesh_code_types.append(('areaLight', 'Area light', """
Creates a surface that emits light uniformly across a rectangular face.

You'll want to adjust csmModuleHook if you want this hooked up to the game's powergrid and light switches.

 - "I SAW THE FACE OF GOD, AND IT WAS SQUARE"
"""[1:-1]))  # noqa

# -------------------------------------------------- #

required_menu_items['fakeLight'] = ['csmModuleHook']
optional_menu_items['fakeLight'] = []
mesh_code_types.append(('fakeLight', 'Fake light', """
Use this with emissive textures. An emissive texture will have its emissive intensity cycled between 0 (off) and 1 (on) when being switched off and on.

Fake lights are meant to be used alongside real lights. For example, if you create an area light, switching it on and off won't affect any emissive materials of the light fixture meshes you have next to the real light. Your light fixture meshes should be tagged as fake lights; when toggled, light-handler modules will toggle its emissive intensity.

You'll want to adjust csmModuleHook if you want this hooked up to the game's power grid and light switches.

Important note: if in Blender you use a single emissive texture on multiple light fixtures, the game engine will assume all emissive textures are part of the same light circuit and power them all off even if you target just one. This is a performance optimisation that drastically reduces the amount of work involved with changing fake light power state. If you would like to avoid this optimisation for certain lights, clone their material in Blender and give them a different name.
"""[1:-1]))  # noqa

# -------------------------------------------------- #

required_menu_items['spotlight'] = []
optional_menu_items['spotlight'] = ['csmModuleHook', 'csmGfxqLight',
                                    'csmDevHelper']
mesh_code_types.append(('spotlight', 'Spotlight', """
Create a focussed light cone.

You'll want to adjust csmModuleHook if you want this hooked up to the game's power grid and light switches.
"""[1:-1]))  # noqa

# -------------------------------------------------- #
# --- HUD-specific definitions --------------------- #
# -------------------------------------------------- #

required_menu_items['hudProgressBlip'] = ['csmStepPosition']
optional_menu_items['hudProgressBlip'] = []
mesh_code_types.append(('hudProgressBlip', '[HUD] Progress blip', """
Used to indicate some sort of percentage. Useful for example with a ship throttle.

The exact use-case here is for blips fading in from dim to bright as they're activated.
"""[1:-1]))  # noqa

# -------------------------------------------------- #

required_menu_items['hudProgressAnimation'] = []
optional_menu_items['hudProgressAnimation'] = []
mesh_code_types.append(('hudProgressAnimation', '[HUD] Progress animation', """
Used to indicate some sort of percentage. Useful for example with a ship throttle.

For this item, the game engine will play the animation from 0-100 as in indication of completion.

This item has no configurable options.
"""[1:-1]))  # noqa

# -------------------------------------------------- #
# -------------------------------------------------- #

# --- PostSetup --- #

# Populated during first run for each object
all_menu_items = ['csmType']


# --- Add-on object --- #


class ObjectCosmosisObjectProperties(bpy.types.Operator):
    """Cosmosis Object Properties"""
    bl_idname = 'object.cosmosis_object_properties'
    bl_label = 'Cosmosis Object Properties'
    bl_options = {'REGISTER', 'UNDO'}
    has_initialized = False

    # --- Optional menu items section --- #

    # int example: bpy.props.IntProperty(name="", default=2, min=1, max=100)

    csmModuleHook: bpy.props.StringProperty(
        name='Module hook',
        description='Optional; examples: cockpitLights | externalLights'
    )

    csmGfxqLight: bpy.props.EnumProperty(
        name='Lighting quality',
        description='Used to prevent the light from rendering on certain GFX '
                    'quality settings',
        items=(
            ('auto', 'Engine decides', ''),
            ('low', 'Only render if low quality', ''),
            ('low,medium', 'Only render if medium or lower quality', ''),
            ('medium', 'Only render if medium quality', ''),
            ('medium,high', 'Only render if medium or higher quality', ''),
            ('high', 'Only render if high quality', ''),
        )
    )

    csmDevHelper: bpy.props.EnumProperty(
        # Note: we use string instead of bool here because Blender does not
        # appear to support storing bools in object properties. This also keeps
        # it consistent with how a user would manually maintain mesh codes.
        name='Dev helpers',
        description='Optional; if enabled, the game engine will draw hints ' +
                    'about the nature of the object, such as light ray ' +
                    'direction and cone size.',
        items=(
            ('true', 'Enable', ''),
            ('false', 'Disable', ''),
        )
    )

    csmStepPosition: bpy.props.FloatProperty(
        name='Step position',
        description='1-10'
    )

    # --- Optional menu items section end --- #

    csmType: bpy.props.EnumProperty(
        name='Mesh type',
        items=mesh_code_types
    )

    def execute(self, context):
        # self.csmModuleHookEnum.name = 'rewritten'

        # On first run, read all object properties and save them here.
        if not self.has_initialized:
            self.has_initialized = True
            for key in allowed_external_keys:
                try:
                    # Filthy hack, but could not find a cleaner way of doing
                    # this.
                    expression = 'if context.object["' + key + '"]: ' + \
                                 'self.' + key + \
                                 ' = context.object["' + key + '"] \n' + \
                                 'else: self.' + key + ' = ""'
                    exec(expression)
                except KeyError:
                    pass

                global all_menu_items
                required_items = required_menu_items.get(self.csmType)
                optional_items = optional_menu_items.get(self.csmType)
                if required_items is not None:
                    all_menu_items += required_menu_items[self.csmType]
                if optional_items is not None:
                    all_menu_items += optional_menu_items[self.csmType]

        # Set object properties to the user-chosen type
        if self.csmType == 'csmUndefined' and 'csmType' in context.object:
            del context.object['csmType']
        elif self.csmType:
            for key in all_menu_items: # noqa
                # TODO: continue from here - unsure how to store bool
                try:
                    # Filthy hack, but could not find a cleaner way of doing
                    # this.
                    expression = \
                        'if self.' + key + ' != "": ' + \
                        'context.object["' + key + '"]' + \
                        ' = self.' + key
                    exec(expression)
                except KeyError:
                    pass

        return {'FINISHED'}

    def draw(self, _context):
        layout = self.layout
        layout.use_property_split = True
        # Always dray type by default.
        layout.prop(self, 'csmType')

        active_type = self.csmType

        self.draw_section('Required properties', 'SNAP_VERTEX',
                          required_menu_items.get(active_type))
        self.draw_section('Optional properties', 'SNAP_EDGE',
                          optional_menu_items.get(active_type))

    def draw_section(self, label_text, icon, menu_items):
        if menu_items is None or len(menu_items) < 1:
            return

        layout = self.layout
        layout.separator()
        layout.label(text=label_text, icon=icon)

        # Only draw menu items relevant to the selected type.
        for menu_item in menu_items:
            if menu_item == 'csmType':
                # Disallow drawing type a second time.
                continue
            # Draw the menu item.
            # https://docs.blender.org/api/current/bpy.types.UILayout.html
            layout.prop(self, menu_item)

    @staticmethod
    def alert_info(message):
        bpy.context.window_manager.popup_menu(
            ObjectCosmosisObjectProperties.draw_modal,
            title=message, icon="INFO"
        )

    @staticmethod
    def alert_error(message):
        bpy.context.window_manager.popup_menu(
            ObjectCosmosisObjectProperties.draw_modal,
            title=message, icon="ERROR"
        )

    @staticmethod
    def draw_modal(self, context):
        pass


def menu_func(self, _context):
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

        # Note: anything that does not have a default value defined here will
        # inherit the value of whatever previous object you had selected. This
        # old value will then actively be injected into the new object if it
        # does not have that value already defined.
        kmi.properties.csmType = 'csmUndefined'
        kmi.properties.csmModuleHook = ''
        kmi.properties.csmGfxqLight = 'auto'
        kmi.properties.csmDevHelper = 'false'
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
