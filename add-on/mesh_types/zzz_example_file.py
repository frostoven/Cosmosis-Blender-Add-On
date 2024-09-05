import bpy

from .cosmosis_mesh_base import CosmosisMeshBase


class TemplateFile(CosmosisMeshBase):
    """
    Please ensure that you very precisely replace TemplateFile, template_file, and Template File with your name using
    the original case. This is needed to ensure proper interop between Blender, Cosmosis, and the generic systems that
    interop between them.
    """
    bl_idname = 'object.csm_template_file'
    bl_label = 'Template File'
    bl_description = (
        'Your description here. Note that Blender automatically adds a period at the end'
    )
    bl_options = {'REGISTER', 'UNDO'}
    icon = 'PLUS'
    mesh_code = 'templateFile'

    csmMyCustomField: bpy.props.StringProperty(
        name='Your Field Name Here',
        description='Describe what it does',
        default='Optional default value',
    )

    def execute(self, context):
        self.prepare_class(context)

        # Prevents edits from being lost.
        self.init_complete = True

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.draw_required_items_heading()
        self.draw_defaults(layout)
