import bpy
from ..utils.get_animation_actions import get_animation_actions
from .cosmosis_mesh_base import CosmosisMeshBase

presets = {
    'Presets': {},
    'Door': {'csmDriver': 'yourSwitchName'},
    'Landing Gear': {'csmDriver': 'deployLandingGear'},
}

preset_items = [(name, name, '') for name in presets.keys()]


class ActuatorAnimation(CosmosisMeshBase):
    """
    Used to animation in-game flight sticks.
    """
    bl_idname = 'object.csm_actuator_animation'
    bl_label = 'Actuator Animation'
    bl_description = (
        'Triggers an animation, usually after a keypress.'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'DRIVER'
    mesh_code = 'actuatorAnimation'

    csmPresetMenu: bpy.props.EnumProperty(
        name='Presets',
        description='Example presets',
        items=preset_items,
    )

    csmDriverAnimation: bpy.props.EnumProperty(
        name='Driver-Triggered Animation',
        description='Animations triggered by a driver. Useful for items such as small switches',
        items=lambda self, context: get_animation_actions()
    )

    def get_animation_types(self):
        obj = bpy.context.active_object
        if not obj or not obj.animation_data:
            return []
        return [f"Action: {action.name}" for action in bpy.data.actions if
                action in obj.animation_data.nla_tracks[0].strips]

    def update_animation_data(self, context):
        self.report({'INFO'}, f"Selected Animation: {self.csmPitchAnimation}")

    def execute(self, context):
        self.prepare_class(context, presets)

        self.load_or_set_default(context, 'csmDriverAnimation', self.csmDriverAnimation)
        self.load_or_set_default(context, 'csmDevHelper', self.csmDevHelper)

        # Prevents edits from being lost.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        # Preset selection
        layout.prop(self, 'csmPresetMenu')

        self.draw_required_items_heading()
        layout.prop(self, 'csmDriverAnimation')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDevHelper')
        self.draw_defaults(layout)
