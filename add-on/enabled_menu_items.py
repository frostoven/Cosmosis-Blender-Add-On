from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Other items
    seat_camera,
)

enabled_menu_items = [
    area_light.AreaLight,
    fake_light.FakeLight,
    point_light.PointLight,
    spotlight.Spotlight,
    'separator',
    seat_camera.SeatCamera,
]
