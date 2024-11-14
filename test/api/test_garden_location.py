from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import SunExposure, WindExposure, Drainage
from garden_ai_agent.data.models import GardenLocation
from .test_api import APITest

class Test_GardenLocation(APITest):

    BASE_URL = BASE_URL + '/garden_locations/'

    def test_create_verify_delete_garden_location(self):
        garden_location = GardenLocation(
            name='Backyard Corner',
            longitude=-122.4194,
            latitude=37.7749,
            elevation=100.5,
            sun_exposure=SunExposure.FULL,
            wind_exposure=WindExposure.PARTIALLY_EXPOSED,
            drainage=Drainage.GOOD,
            irrigation_zone_id=1
        )

        # Create new garden location
        response = self.client.post(self.BASE_URL, json=garden_location.json())
        self.assertEqual(response.status_code, 201)
        created_location = response.json['data']
        self.assertEqual(created_location['name'], garden_location.name)
        location_id = created_location['id']

        # Get the specific location
        response = self.client.get(f"{self.BASE_URL}{location_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_location = response.json['data']
        self.assertEqual(retrieved_location['name'], garden_location.name)

        # Get all locations and verify our location is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        locations = response.json['data']
        self.assertTrue(any(location['id'] == location_id for location in locations))

        # Modify the location
        garden_location.name = 'Backyard Corner Modified'
        garden_location.elevation = 120.5

        response = self.client.put(f"{self.BASE_URL}{location_id}", json=garden_location.json())
        self.assertEqual(response.status_code, 200)
        modified_location = response.json['data']
        self.assertEqual(modified_location['name'], garden_location.name)
        self.assertEqual(modified_location['elevation'], garden_location.elevation)

        # Delete the location
        response = self.client.delete(f"{self.BASE_URL}{location_id}")
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        response = self.client.get(f"{self.BASE_URL}{location_id}")
        self.assertEqual(response.status_code, 404) 