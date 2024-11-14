from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import Day
from garden_ai_agent.data.models import IrrigationZone
from .test_api import APITest

class Test_IrrigationZone(APITest):

    BASE_URL = BASE_URL + '/irrigation_zones/'

    def test_create_verify_delete_irrigation_zone(self):
        irrigation_zone = IrrigationZone(
            name='Front Yard',
            scheduled_days=[Day.MONDAY, Day.WEDNESDAY, Day.FRIDAY],
            start_time='06:00:00',
            duration_minutes=30,
            flow_rate_gpm=2.5
        )

        # Create new irrigation zone
        response = self.client.post(self.BASE_URL, json=irrigation_zone.json())
        self.assertEqual(response.status_code, 201)
        created_zone = response.json['data']
        self.assertEqual(created_zone['name'], irrigation_zone.name)
        zone_id = created_zone['id']

        # Get the specific zone
        response = self.client.get(f"{self.BASE_URL}{zone_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_zone = response.json['data']
        self.assertEqual(retrieved_zone['name'], irrigation_zone.name)

        # Get all zones and verify our zone is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        zones = response.json['data']
        self.assertTrue(any(zone['id'] == zone_id for zone in zones))

        # Modify the zone
        irrigation_zone.name = 'Front Yard Modified'
        irrigation_zone.duration_minutes = 45

        response = self.client.put(f"{self.BASE_URL}{zone_id}", json=irrigation_zone.json())
        self.assertEqual(response.status_code, 200)
        modified_zone = response.json['data']
        self.assertEqual(modified_zone['name'], irrigation_zone.name)
        self.assertEqual(modified_zone['duration_minutes'], irrigation_zone.duration_minutes)

        # Delete the zone
        response = self.client.delete(f"{self.BASE_URL}{zone_id}")
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        response = self.client.get(f"{self.BASE_URL}{zone_id}")
        self.assertEqual(response.status_code, 404)
