import bpy


class ClearMeshType(bpy.types.Operator):
    """
    This isn't by itself a mesh code. This used to clear mesh code information.
    """
    bl_idname = 'object.csm_clear_mesh_type'
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
        """
        Clears mesh code information from the selected object.
        """
        bpy.ops.wm.confirm_dialog(
            'INVOKE_DEFAULT',
            message=f'Delete this object\'s {self.deletion_target} data?',
            deletion_target=self.deletion_target,
        )

        return {'CANCELLED'}
