from .cosmosis_mesh_base import CosmosisMeshBase


class FakeLight(CosmosisMeshBase):
    """
    Signals to the game engine that the mesh should be treated as an fake light.
    """
    bl_idname = 'object.csm_fake_light'
    bl_label = 'Fake Light'
    bl_description = (
            'Use this with emissive textures. An emissive texture will have its emissive intensity cycled between 0 '
            '(off) and 1 (on) when being switched off and on.\n\n'
            'Fake lights are meant to be used alongside real lights. For example, if you create an area light, '
            'switching it on and off won\'t affect any emissive materials of the light fixture meshes you have next to '
            'the real light. Your light fixture meshes should be tagged as fake lights; when toggled, light-handler '
            'modules will toggle its emissive intensity.\n\n' +
            'You\'ll want to adjust csmDriver if you want this hooked up to the game\'s power grid and light '
            'switches.\n\n'
            'Important note: if in Blender you use a single emissive material with multiple light fixtures, the game '
            'engine will assume all emissive textures are part of the same light circuit and power them all off even '
            'if you target just one'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Note: execute is called for both keypress launches and menu launches,
        # whereas invoke is for menu-based launches only (apparently).
        context.object['csmType'] = 'fakeLight'
        self.load_or_set_default(context, 'csmDriver', self.csmDriver)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, 'csmDriver')
