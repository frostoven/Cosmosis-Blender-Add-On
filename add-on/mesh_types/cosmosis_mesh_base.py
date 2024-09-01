import bpy


class CosmosisMeshBase(bpy.types.Operator):
    """
    Base class for all Cosmosis mesh code classes.
    """
    bl_idname = 'object.csm_mesh_base'
    bl_label = '???'
    bl_description = (
        'Base class for all Cosmosis mesh code classes.'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'NONE'
    mesh_code = 'csmUndefined'

    ### --- Attributes altered by derived classes --- ###

    init_complete = False

    ### --- Static helpers --- ###

    @staticmethod
    def alert_info(message):
        bpy.context.window_manager.popup_menu(
            CosmosisMeshBase.draw_modal,
            title=message, icon="INFO"
        )

    @staticmethod
    def alert_error(message):
        bpy.context.window_manager.popup_menu(
            CosmosisMeshBase.draw_modal,
            title=message, icon="ERROR"
        )

    @staticmethod
    def draw_modal(self, context):
        pass

    ### --- Common menu items --- ###

    csmDriver: bpy.props.StringProperty(
        name='Driver String',
        description='Exposes this object to relevant ship modules. Examples: cockpitLights | externalLights | yourSwitchName'
    )

    ### --- Required overrides --- ###

    def execute(self, context):
        CosmosisMeshBase.alert_error(
            'The CosmosisMeshBase `execute` function should be overridden.'
        )
        return {'FINISHED'}

    def draw(self, context):
        CosmosisMeshBase.alert_error(
            'The CosmosisMeshBase `draw` function should be overridden.'
        )

    ### --- Common methods --- ###

    def create_structure_if_needed(self, context):
        """Call this each time your operator executes. It ensures your object has the needed user data structures."""

        if 'csmMeshCodes' not in context.object:
            context.object['csmMeshCodes'] = {}

        if self.mesh_code not in context.object['csmMeshCodes']:
            context.object['csmMeshCodes'][self.mesh_code] = {'csmType': self.mesh_code}

    def load_or_set_default(self, context, key, default):
        """
        Please run self.create_structure_if_needed() for running this method.

        This method determines if the specified field should be loaded from the mesh, or if the field value should
        overwrite what's in the mesh, and then writes the needed data. Used during boot to set previous values, used
        after boot to save new values.

        Please set self.init_complete to True after you've run this for all fields, otherwise it'll re-init each time.
        """
        target = context.object['csmMeshCodes'][self.mesh_code]

        if key in target and not self.init_complete:
            setattr(self, key, target[key])
        else:
            target[key] = default

    def apply_user_preset(self, context, presets):
        """Please run self.create_structure_if_needed() for running this method."""
        target = context.object['csmMeshCodes'][self.mesh_code]
        preset = presets.get(self.csmPresetMenu, None)
        if preset:
            keys = preset.keys()
            for key in keys:
                target[key] = preset.get(key, '')
                setattr(self, key, target[key])

            # Prevent the preset menu from blocking user customization.
            setattr(self, 'csmPresetMenu', 'Presets')

    ### --- Common menu items --- ###

    csmGfxqLight: bpy.props.EnumProperty(
        name='Lighting Quality',
        description='Used to prevent the light from rendering on certain GFX quality settings',
        items=(
            ('auto', 'Engine decides', ''),
            ('low', 'Only render if low quality', ''),
            ('low,medium', 'Only render if medium or lower quality', ''),
            ('medium', 'Only render if medium quality', ''),
            ('medium,high', 'Only render if medium or higher quality', ''),
            ('high', 'Only render if high quality', ''),
        ),
    )

    csmDevHelper: bpy.props.EnumProperty(
        name='Dev Helpers',
        description='Optional; if enabled, the game engine will draw hints about the nature of the object, such as light ray direction and cone size',
        items=(
            ('true', 'Enable', ''),
            ('false', 'Disable', ''),
        ),
        default='false',
    )

    ### --- Common UI Items --- ###

    def draw_optional_items_heading(self):
        self.layout.separator()
        self.layout.label(text='Optional properties', icon='SNAP_EDGE')

    def draw_required_items_heading(self):
        self.layout.separator()
        self.layout.label(text='Required properties', icon='SNAP_VERTEX')
