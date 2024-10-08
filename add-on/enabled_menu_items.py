from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Helm control and pilot items
    seat_camera,
    animated_cockpit_peripheral,
    actuator_animation,
    # Signal-based communication
    signal_switch,
    signal_receiver,
    # Other
    mesh_lod_management,
    generic,
)

# Menu items shown regardless of context.
header_items = [
    mesh_lod_management.MeshLodManagement,
    'separator',
]

# Menu items shown contextually.
enabled_menu_items = [
    signal_switch.SignalSwitch,
    signal_receiver.SignalReceiver,
    actuator_animation.ActuatorAnimation,
    'separator',
    animated_cockpit_peripheral.AnimatedCockpitPeripheral,
    seat_camera.SeatCamera,
    'separator',
    area_light.AreaLight,
    fake_light.FakeLight,
    point_light.PointLight,
    spotlight.Spotlight,
    'separator',
    generic.Generic,
]
