import bpy


class ConfirmAndDelete(bpy.types.Operator):
    """
    Helper class to ensure that the confirmation dialog shows for both menu-launched and keybinding-launched windows.
    """
    bl_idname = "wm.csm_confirm_and_delete"
    bl_label = "Confirm Type Info Deletion"

    deletion_target: bpy.props.StringProperty(
        default=''
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f'Delete this object\'s {self.deletion_target} data?')

    def execute(self, context):
        """
        Clears mesh code information from the selected object.
        """
        if self.deletion_target == '':
            self.alert_deletion_error('[CosmosisDev] Warning: deletion_target not correctly defined.')
            return {'CANCELLED'}

        if not context.object:
            self.alert_deletion_error('[CosmosisDev] Warning: deletion failed: context.object is falsy.')
            return {'CANCELLED'}

        if 'csmMeshCodes' not in context.object:
            self.alert_deletion_error('[CosmosisDev] Warning: deletion failed: "csmMeshCodes" not in context.object.')
            return {'CANCELLED'}

        if self.deletion_target not in context.object['csmMeshCodes']:
            self.alert_deletion_error(
                f'[CosmosisDev] Warning: deletion failed: "{self.deletion_target}" not in csmMeshCodes object.'
            )
            return {'CANCELLED'}

        del context.object['csmMeshCodes'][self.deletion_target]
        return {'FINISHED'}
