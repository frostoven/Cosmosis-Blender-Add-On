import bpy
from .cosmosis_mesh_base import CosmosisMeshBase
from .helpers import signal_receiver_helpers


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
    icon = 'SYSTEM'
    mesh_code = 'signalReceiver'

    # Define the collection property for multiple signal texts
    csmSignalTexts: bpy.props.CollectionProperty(
        type=signal_receiver_helpers.SignalStringItem
    )

    def execute(self, context):
        self.prepare_class(context)
        self.load_or_set_default_array(context, 'signalText', self.csmSignalTexts)

        # Prevents edits from being lost.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()

        hide_add_button = False

        # Draw each signal text in the collection.
        for i, signal_item in enumerate(self.csmSignalTexts):
            text = 'Signal Text (In)' if i == 0 else f'ST (In) Port {i + 1}'
            row = layout.row()
            row.prop(signal_item, 'item_text', text=text)
            row.operator('object.csm_remove_signal_string', text='', icon='X').index = i

            if i >= 31:
                hide_add_button = True

        # Add button for adding a new signal listener.
        if not hide_add_button:
            layout.separator()
            layout.operator(
                'object.csm_add_signal_string',
                text='Add Additional Listener',
            )

        self.draw_optional_items_heading()
        self.draw_defaults(layout)
