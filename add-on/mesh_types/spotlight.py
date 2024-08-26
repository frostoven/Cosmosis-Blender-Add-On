from .cosmosis_mesh_base import CosmosisMeshBase


class Spotlight(CosmosisMeshBase):
    """
    Signals to the game engine that the mesh should be treated as an spot light.
    """
    bl_idname = 'object.csm_spotlight'
    bl_label = 'Spotlight'
    bl_description = (
        'Creates a surface that emits light uniformly across a rectangular face.\n\n'
        'You\'ll want to adjust csmDriver if you want this hooked up to the game\'s power grid and light switches'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Note: execute is called for both keypress launches and menu launches,
        # whereas invoke is for menu-based launches only (apparently).
        context.object['csmType'] = 'spotlight'
        self.load_or_set_default(context, 'csmDriver', self.csmDriver)
        self.load_or_set_default(context, 'csmGfxqLight', self.csmGfxqLight)
        self.load_or_set_default(context, 'csmDevHelper', self.csmDevHelper)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
        layout.prop(self, 'csmGfxqLight')
        layout.prop(self, 'csmDevHelper')
