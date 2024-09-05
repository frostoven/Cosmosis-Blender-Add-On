import bpy
from ..utils.get_animation_actions import get_animation_actions
from .cosmosis_mesh_base import CosmosisMeshBase

presets = {
    'Presets': {},
    'Yoke': {'csmDriver': '', 'csmDriverAnimation': 'csmUndefined'},
    'Throttle': {'csmDriver': '', 'csmDriverAnimation': 'csmUndefined'},
    'Rudder': {'csmDriver': '', 'csmDriverAnimation': 'csmUndefined'},
    'Cockpit Switch (General)': {'csmDriverAnimation': 'csmAutoAnimate'},
    'Cockpit Switch (Flight Assist)': {'csmDriver': 'toggleFlightAssist', 'csmDriverAnimation': 'csmAutoAnimate'},
}

preset_items = [(name, name, '') for name in presets.keys()]


class AnimatedCockpitPeripheral(CosmosisMeshBase):
    """
    Used to animation in-game flight sticks.

    Note: This is a special case of ActuatorAnimation; ActuatorAnimation defines animations from 0%-100%, whereas
    AnimatedCockpitPeripheral is concerned with convenience items that have obvious constraints and are used often.
    Within Cosmosis, AnimatedCockpitPeripheral handlers have preset values that cannot be easily expressed with
    ActuatorAnimation.
    """
    bl_idname = 'object.csm_animated_cockpit_peripheral'
    bl_label = 'Animated Cockpit Peripheral'
    bl_description = (
        'Used to animate in-game cockpit peripherals. This may include items such as yokes, throttles, and switches.\n\n'
        'Keyframed actions will show up in the peripheral animation dropdowns. If you do not have any animations, your '
        'choices are limited to "Not Set" and "Auto-Animate". Keyframed actions that are currently visible in the '
        'viewport will have a dot next to them in the dropdown'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'PIVOT_BOUNDBOX'
    mesh_code = 'animatedCockpitPeripheral'

    csmPresetMenu: bpy.props.EnumProperty(
        name='Presets',
        description="Example presets",
        items=preset_items,
    )

    csmPitchAnimation: bpy.props.EnumProperty(
        name='Pitch Animation',
        description='Select animation used to convey pitch',
        items=lambda self, context: get_animation_actions(True)
    )

    csmYawAnimation: bpy.props.EnumProperty(
        name='Yaw Animation',
        description='Select animation used to convey yaw',
        items=lambda self, context: get_animation_actions(True)
    )

    csmRollAnimation: bpy.props.EnumProperty(
        name='Roll Animation',
        description='Select animation used to convey roll',
        items=lambda self, context: get_animation_actions(True)
    )

    csmDriverAnimation: bpy.props.EnumProperty(
        name='Driver-Triggered Animation',
        description='Rotations triggered by a driver. Useful for items such as small switches',
        items=lambda self, context: get_animation_actions(True)
    )

    def get_animation_types(self):
        obj = bpy.context.active_object
        if not obj or not obj.animation_data:
            return []
        return [f"Action: {action.name}" for action in bpy.data.actions if
                action in obj.animation_data.nla_tracks[0].strips]

    def execute(self, context):
        self.prepare_class(context, presets)

        self.load_or_set_default(context, 'csmPitchAnimation', self.csmPitchAnimation)
        self.load_or_set_default(context, 'csmYawAnimation', self.csmYawAnimation)
        self.load_or_set_default(context, 'csmRollAnimation', self.csmRollAnimation)
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
        layout.prop(self, 'csmPitchAnimation')
        layout.prop(self, 'csmYawAnimation')
        layout.prop(self, 'csmRollAnimation')
        layout.prop(self, 'csmDriverAnimation')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
        layout.prop(self, 'csmDevHelper')
