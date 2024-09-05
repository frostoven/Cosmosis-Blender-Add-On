import bpy
from .cosmosis_mesh_base import CosmosisMeshBase


class SignalSwitch(CosmosisMeshBase):
    """
    A switch that sends a signal other modules listen for.
    """
    bl_idname = 'object.csm_signal_switch'
    bl_label = 'Switch'
    bl_description = (
        'Sends out a command signal. Items such as doors receive these signals, which trigger their open or close '
        'animations'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = "MEMORY"
    mesh_code = 'signalSwitch'

    csmSignalTextOut: bpy.props.StringProperty(
        name='Signal Text (Out)',
        description='The command signal text that this switch broadcasts. Example: "cockpit door switch left"'
    )

    csmSwitchType: bpy.props.EnumProperty(
        name='Switch Type',
        description='Used by the engine to figure out what kind of user interaction is required',
        items=(
            ('button', 'Button', ''),
            ('keypad', 'Keypad', ''),
            ('level', 'Mechanical Lever', ''),
        ),
        default='button',
    )

    def execute(self, context):
        self.create_structure_if_needed(context)

        self.load_or_set_default(context, 'csmDriver', self.csmDriver)
        self.load_or_set_default(context, 'csmSignalTextOut', self.csmSignalTextOut)
        self.load_or_set_default(context, 'csmSwitchType', self.csmSwitchType)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()
        layout.prop(self, 'csmSignalTextOut')
        layout.prop(self, 'csmSwitchType')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
