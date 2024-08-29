from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Helm control and pilot items
    seat_camera,
    animated_cockpit_peripheral,
)

enabled_menu_items = [
    area_light.AreaLight,
    fake_light.FakeLight,
    point_light.PointLight,
    spotlight.Spotlight,
    'separator',
    animated_cockpit_peripheral.AnimatedCockpitPeripheral,
    seat_camera.SeatCamera,
]
