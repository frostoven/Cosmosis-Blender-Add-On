import bpy
from ..utils.get_animation_actions import get_animation_actions
from .cosmosis_mesh_base import CosmosisMeshBase


class AnimatedCockpitPeripheral(CosmosisMeshBase):
    """
    Used to animation in-game flight sticks.
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
    icon = 'DRIVER'

    csmPitchAnimation: bpy.props.EnumProperty(
        name='Pitch Animation',
        description='Select animation used to convey pitch',
        items=get_animation_actions
    )

    csmYawAnimation: bpy.props.EnumProperty(
        name='Yaw Animation',
        description='Select animation used to convey yaw',
        items=get_animation_actions
    )

    csmRollAnimation: bpy.props.EnumProperty(
        name='Roll Animation',
        description='Select animation used to convey roll',
        items=get_animation_actions
    )

    csmDriverAnimation: bpy.props.EnumProperty(
        name='Driver-Triggered Animation',
        description='Rotations triggered by a driver. Useful for items such as small switches',
        items=get_animation_actions
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
        # Note: execute is called for both keypress launches and menu launches,
        # whereas invoke is for menu-based launches only (apparently).
        context.object['csmType'] = 'animatedCockpitPeripheral'
        self.load_or_set_default(context, 'csmPitchAnimation', self.csmPitchAnimation)
        self.load_or_set_default(context, 'csmYawAnimation', self.csmYawAnimation)
        self.load_or_set_default(context, 'csmRollAnimation', self.csmRollAnimation)
        self.load_or_set_default(context, 'csmDriverAnimation', self.csmDriverAnimation)
        self.load_or_set_default(context, 'csmDriver', self.csmDriver)
        self.load_or_set_default(context, 'csmDevHelper', self.csmDevHelper)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()
        layout.prop(self, 'csmPitchAnimation')
        layout.prop(self, 'csmYawAnimation')
        layout.prop(self, 'csmRollAnimation')
        layout.prop(self, 'csmDriverAnimation')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
        layout.prop(self, 'csmDevHelper')
