import bpy
from ..utils.get_animation_actions import get_animation_actions
from .cosmosis_mesh_base import CosmosisMeshBase

presets = {
    'Presets': {},
    'Primary Pilot Seat': {'csmStartingCamera': True, 'csmIsPilotCamera': True},
    'Copilot Seat': {'csmStartingCamera': False, 'csmIsPilotCamera': True},
    'Passenger Seat': {'csmStartingCamera': False, 'csmIsPilotCamera': False},
}

preset_items = [(name, name, '') for name in presets.keys()]


class SeatCamera(CosmosisMeshBase):
    """
    Indicates where the player\'s camera should be placed after sitting in a chair
    """
    bl_idname = 'object.csm_seat_camera'
    bl_label = 'Seat Camera'
    bl_description = (
        'Indicates where the player\'s camera should be placed after sitting in a chair. It also determines where the '
        '"Press [Key] to sit" prompt should appear.\n\n'
        'You can use any mesh for this (such as a cage), but an actual camera object is recommended'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'CON_CAMERASOLVER'
    mesh_code = 'seatCamera'

    csmPresetMenu: bpy.props.EnumProperty(
        name='Presets',
        description="Example presets",
        items=preset_items,
    )

    csmStartingCamera: bpy.props.BoolProperty(
        name='Starting Camera',
        description='If enabled, this is the seat the player will sit in when the game starts',
        default=False,
    )

    csmIsPilotCamera: bpy.props.BoolProperty(
        name='Is Pilot Seat',
        description='If enabled, this seat provides a pilot interface. Enable this for both pilot and copilot seats',
        default=False,
    )

    csmAnimateToNext: bpy.props.EnumProperty(
        name='Cam Anim Next',
        description='Animation to use on this camera when moving to the next cockpit camera',
        items=lambda self, context: get_animation_actions(),
    )

    csmAnimateToPrevious: bpy.props.EnumProperty(
        name='Cam Anim Prev',
        description='Animation to use on this camera when moving to the previous cockpit camera',
        items=lambda self, context: get_animation_actions(),
    )

    csmAnimationLeaveSeat: bpy.props.EnumProperty(
        name='Leave Seat Anim',
        description='Animation to use on this camera when moving to the previous cockpit camera',
        items=lambda self, context: get_animation_actions(),
    )

    def execute(self, context):
        self.prepare_class(context, presets)

        self.load_or_set_default(context, 'csmStartingCamera', self.csmStartingCamera)
        self.load_or_set_default(context, 'csmIsPilotCamera', self.csmIsPilotCamera)
        self.load_or_set_default(context, 'csmAnimateToNext', self.csmAnimateToNext)
        self.load_or_set_default(context, 'csmAnimateToPrevious', self.csmAnimateToPrevious)
        self.load_or_set_default(context, 'csmAnimationLeaveSeat', self.csmAnimationLeaveSeat)
        self.load_or_set_default(context, 'csmDevHelper', self.csmDevHelper)

        # Prevents edits from being lost.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, 'csmPresetMenu')

        self.draw_required_items_heading()
        layout.prop(self, 'csmStartingCamera')
        layout.prop(self, 'csmIsPilotCamera')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmAnimateToNext')
        layout.prop(self, 'csmAnimateToPrevious')
        layout.prop(self, 'csmAnimationLeaveSeat')
        layout.separator()
        layout.prop(self, 'csmDevHelper')
        self.draw_defaults(layout)
