from .mesh_types import (
    # Lighting
    area_light, fake_light, point_light, spotlight,
    # Helm control and pilot items
    seat_camera,
    helm_flight_stick,
)

enabled_menu_items = [
    area_light.AreaLight,
    fake_light.FakeLight,
    point_light.PointLight,
    spotlight.Spotlight,
    'separator',
    seat_camera.SeatCamera,
    helm_flight_stick.HelmFlightStick,
]
