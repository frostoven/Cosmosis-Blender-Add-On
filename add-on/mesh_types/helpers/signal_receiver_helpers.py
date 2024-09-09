import bpy


class SignalStringItem(bpy.types.PropertyGroup):
    """Defined a property group to store individual signal strings."""
    item_text: bpy.props.StringProperty(
        name='Signal Text',
        description='The command signal text'
    )


class AddSignalStringOperator(bpy.types.Operator):
    """Adds a string to the signal list."""
    bl_idname = 'object.csm_add_signal_string'
    bl_label = 'Add Signal String'
    bl_description = 'Add another listener. These are exported as a string array'

    def execute(self, context):
        # Reference the operator itself to add a signal to the collection.
        operator = context.active_operator
        operator.csmSignalTexts.add()
        return {'FINISHED'}


class RemoveSignalStringOperator(bpy.types.Operator):
    """Removes a string from the signal list."""
    bl_idname = 'object.csm_remove_signal_string'
    bl_label = 'Remove Signal String'

    index: bpy.props.IntProperty()

    def execute(self, context):
        operator = context.active_operator
        operator.csmSignalTexts.remove(self.index)
        return {'FINISHED'}
