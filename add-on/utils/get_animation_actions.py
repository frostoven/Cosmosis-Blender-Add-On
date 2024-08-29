import bpy
import uuid

# Used to disable animation.
unset_action = ('csmUndefined', 'Not Set', '"Not Set" disables animation', 'PANEL_CLOSE', 0)

# Allows the engine to guess the animation.
auto_animate_action = (
    'csmAutoAnimate',
    'Auto-Animate',
    'If selected, the game engine will rotate this mesh about its origin instead of using keyframes. For better '
    'results, prefer using keyframes',
    'OUTLINER_DATA_ARMATURE',
    1
)


def action_uuid(action):
    """
    If the user renamed an animation and we identified actions by name, we'd now have a stale name. Actions can have
    custom properties like objects can, so we generate and attach a unique UUID to the action if it does not already
    have one.
    """
    if 'csmUuid' not in action:
        object_uuid = str(uuid.uuid4())
        print('[CosmosisDev] First time encountering action ' + action.name + '; assigning UUID ' + object_uuid)
        action['csmUuid'] = object_uuid
        return object_uuid
    else:
        return action['csmUuid']


def get_animation_actions(self, context):
    try:
        # Get the active object.
        active_obj = bpy.context.active_object

        # Ensure the object has animation data
        if active_obj.animation_data:

            selectable_actions = [
                unset_action,
                auto_animate_action,
            ]
            item_id = 2

            active_action = ''

            # Get the active action for convenience in case the user is doing simple really basic.
            if active_obj.animation_data.action:
                action = active_obj.animation_data.action
                active_action = action.name
                selectable_actions.append(
                    (
                        action_uuid(action),
                        active_action,
                        'Keyframed action (currently visible in viewport)',
                        'LAYER_ACTIVE',
                        item_id
                    ),
                )
                item_id += 1

            # Get all remaining actions.
            actions = bpy.data.actions
            for action in actions:
                # We skip the active action because it's already in the list (we display the active action first).
                if action.name != active_action:
                    selectable_actions.append((
                        action_uuid(action),
                        action.name,
                        'Keyframed action',
                        '',
                        item_id,
                    ))
                    item_id += 1

        else:
            # No animation data found for the active object.
            return (
                unset_action,
                auto_animate_action,
            )

        return selectable_actions
    except AttributeError:
        return (
            ('csmUndefined', 'Error while reading animation data', '', 'PANEL_CLOSE', 0),
        )
