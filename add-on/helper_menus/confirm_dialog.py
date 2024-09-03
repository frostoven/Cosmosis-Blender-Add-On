import bpy


class ConfirmDialogOperator(bpy.types.Operator):
    bl_idname = "wm.confirm_dialog"
    bl_label = "Confirm Dialog"

    deletion_target: bpy.props.StringProperty(
        default=''
    )

    message: bpy.props.StringProperty(name='Message', default='Are you sure?')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message)

    def execute(self, context):
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
