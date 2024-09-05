from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Helm control and pilot items
    seat_camera,
    animated_cockpit_peripheral,
    actuator_animation,
    # Signal-based communication
    signal_switch,
    # Other
    generic,
)

enabled_menu_items = [
    signal_switch.SignalSwitch,
    'separator',
    animated_cockpit_peripheral.AnimatedCockpitPeripheral,
    actuator_animation.ActuatorAnimation,
    seat_camera.SeatCamera,
    'separator',
    area_light.AreaLight,
    fake_light.FakeLight,
    point_light.PointLight,
    spotlight.Spotlight,
    'separator',
    generic.Generic,
]
