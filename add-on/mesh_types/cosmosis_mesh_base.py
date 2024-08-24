import bpy


class CosmosisMeshBase(bpy.types.Operator):
    """
    Base class for all Cosmosis mesh code classes.
    """
    bl_idname = 'object.area_light'
    bl_label = '???'
    bl_description = (
        'Base class for all Cosmosis mesh code classes.'
    )
    bl_options = {'REGISTER', 'UNDO'}

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

    csmSubsystem: bpy.props.StringProperty(
        name='Subsystem',
        description='Optional; examples: cockpitLights | externalLights'
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

    def load_or_set_default(self, context, key, default):
        """
        Determines if the specified field should be loaded from the mesh, or if
        the field value should overwrite what's in the mesh, and then writes
        the needed data. Used during boot to set previous values, used after
        boot to save new values.

        Set self.init_complete to True after you've run this for all fields.
        :param context:
        :param key:
        :param default:
        :return:
        """

        # Possible example if this was not written dynamically:
        #  [if preexisting] self.csmSubsystem = context.object['csmSubsystem']
        #  [if new]         context.object['csmSubsystem'] = self.csmSubsystem
        #
        if key in context.object and not self.init_complete:
            setattr(self, key, context.object[key])
        else:
            context.object[key] = default

    ### --- Common menu items --- ###

    csmGfxqLight: bpy.props.EnumProperty(
        name='Lighting quality',
        description='Used to prevent the light from rendering on certain GFX quality settings',
        items=(
            ('auto', 'Engine decides', ''),
            ('low', 'Only render if low quality', ''),
            ('low,medium', 'Only render if medium or lower quality', ''),
            ('medium', 'Only render if medium quality', ''),
            ('medium,high', 'Only render if medium or higher quality', ''),
            ('high', 'Only render if high quality', ''),
        )
    )

    csmDevHelper: bpy.props.EnumProperty(
        name='Dev helpers',
        description='Optional; if enabled, the game engine will draw hints about the nature of the object, such as light ray direction and cone size.',
        items=(
            ('true', 'Enable', ''),
            ('false', 'Disable', ''),
        )
    )
