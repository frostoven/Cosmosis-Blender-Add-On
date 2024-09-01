from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Helm control and pilot items
    seat_camera,
    animated_cockpit_peripheral,
    actuator_animation,
)

enabled_menu_items = [
    # Temporarily disabling some items as part of the mult-mesh-code migration.
    # area_light.AreaLight,
    fake_light.FakeLight,
    # point_light.PointLight,
    # spotlight.Spotlight,
    # 'separator',
    # animated_cockpit_peripheral.AnimatedCockpitPeripheral,
    # actuator_animation.ActuatorAnimation,
    seat_camera.SeatCamera,
]
