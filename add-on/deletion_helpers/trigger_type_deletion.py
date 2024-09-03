import bpy


class TriggerTypeDeletion(bpy.types.Operator):
    """
    Triggers the dialog window that deletes the specified mesh code info
    """
    bl_idname = 'object.csm_trigger_type_deletion'
    bl_label = 'Clear Type Info'
    bl_description = 'Deletes the data associated with this mesh code from the selected object'
    bl_options = {'REGISTER', 'UNDO'}

    deletion_target: bpy.props.StringProperty(
        default=''
    )

    @staticmethod
    def alert_deletion_error(message):
        bpy.context.window_manager.popup_menu(
            lambda self, context: None,
            title=message, icon="ERROR"
        )

    def execute(self, context):
        # This was all initially one class, but unfortunately the invoke() function isn't called when the menu is
        # launched via keybinding. The class has since been split in two so that we can more easily trigger invoke
        # while still keeping things somewhat clean.
        bpy.ops.wm.csm_confirm_and_delete(
            'INVOKE_DEFAULT',
            deletion_target=self.deletion_target,
        )

        return {'CANCELLED'}
