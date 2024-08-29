import bpy

def get_animation_actions(self, context):
    try:
        # Get the active object
        active_obj = bpy.context.active_object

        item_id = 0

        # Ensure the object has animation data
        if active_obj.animation_data:
            selectable_actions = [
                # Add option to deselect animations.
                ('csmUndefined', 'Not Set', '', 'PANEL_CLOSE', item_id),
            ]
            item_id += 1

            active_action = ''

            # Get the active action for convenience in case the user is doing simple really basic.
            if active_obj.animation_data.action:
                active_action = active_obj.animation_data.action.name
                selectable_actions.append(
                    (active_action, active_action, '', 'LAYER_ACTIVE', item_id),
                )
                item_id += 1

            # Get all remaining actions.
            actions = bpy.data.actions
            for action in actions:
                # We skip the active action because it's already in the list (we display the active action first).
                if action.name != active_action:
                    selectable_actions.append((
                        action.name,
                        action.name,
                        '',
                        '',
                        item_id,
                    ))
                    item_id += 1

        else:
            # No animation data found for the active object.
            return (
                ('csmUndefined', 'Not Set', '', 'PANEL_CLOSE', 0),
            )

        return selectable_actions
    except AttributeError:
        return (
            ('csmUndefined', 'Error while reading animation data', '', 'PANEL_CLOSE', 0),
        )
