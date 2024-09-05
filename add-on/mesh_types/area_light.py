from .cosmosis_mesh_base import CosmosisMeshBase


class AreaLight(CosmosisMeshBase):
    """
    Signals to the game engine that the mesh should be treated as an area light.
    """
    bl_idname = 'object.csm_area_light'
    bl_label = 'Area Light'
    bl_description = (
        'Creates a surface that emits light uniformly across a rectangular face.\n\n'
        'You\'ll want to adjust csmDriver if you want this hooked up to the game\'s power grid and light switches'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'LIGHT_AREA'
    mesh_code = 'areaLight'

    def execute(self, context):
        self.prepare_class(context)

        self.load_or_set_default(context, 'csmGfxqLight', self.csmGfxqLight)
        self.load_or_set_default(context, 'csmDevHelper', self.csmDevHelper)

        # Prevents edits from being lost.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_optional_items_heading()
        layout.prop(self, 'csmGfxqLight')
        layout.prop(self, 'csmDevHelper')
        self.draw_defaults(layout)
