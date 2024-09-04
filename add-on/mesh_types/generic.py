from .cosmosis_mesh_base import CosmosisMeshBase


class Generic(CosmosisMeshBase):
    """
    The simplest of all mesh codes.
    """
    bl_idname = 'object.csm_generic'
    bl_label = 'Generic'
    bl_description = (
        'Useful for cases where the game cannot fully understand the type upfront, such as with community-made '
        'mods and ships'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = "DISC"
    mesh_code = 'generic'

    def execute(self, context):
        self.create_structure_if_needed(context)

        self.load_or_set_default(context, 'csmDriver', self.csmDriver)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()
        layout.prop(self, 'csmDriver')
