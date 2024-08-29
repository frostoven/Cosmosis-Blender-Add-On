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
        'Used to animation in-game flight sticks.\n\n'
        'Informs the game engine that this mesh\'s animations follow the ship\'s pitch/yaw/roll values'
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

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
        layout.prop(self, 'csmDevHelper')
