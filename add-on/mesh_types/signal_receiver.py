import bpy
from .cosmosis_mesh_base import CosmosisMeshBase


class SignalReceiver(CosmosisMeshBase):
    """
    Used to open and close door meshes.
    """
    bl_idname = 'object.csm_signal_receiver'
    bl_label = 'Signal Receiver'
    bl_description = (
        'Used for items that are expected to respond to a signal.\n\n'
        'Example use-case: Attach this to a door and specify the signal text of a nearby switch. '
        'Attach the actuator animation for opening the door, and the door will open when the switch is triggered'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = "SYSTEM"
    mesh_code = 'signalReceiver'

    csmSignalTextIn: bpy.props.StringProperty(
        name='Signal Text (In)',
        description='The command signal text that this object responds to. Example: "cockpit door switch left"'
    )

    def execute(self, context):
        self.create_structure_if_needed(context)

        self.load_or_set_default(context, 'csmDriver', self.csmDriver)
        self.load_or_set_default(context, 'csmSignalTextIn', self.csmDriver)

        # Prevents edits from being lost. This is a tad spaghetti though, need
        # to create a cleaner solution.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()
        layout.prop(self, 'csmSignalTextIn')

        self.draw_optional_items_heading()
        layout.prop(self, 'csmDriver')
