from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import ObservationType, GrowthStage
from datetime import datetime
from .test_api import APITest
from garden_ai_agent.data.models import GardenLocation, Plant, Observation
from garden_ai_agent.data.fields import SunExposure, WindExposure, Drainage, GrowthForm, LifeCycle, UseCategory

class Test_Observation(APITest):

    BASE_URL = BASE_URL + '/observations/'

    def test_create_verify_delete_observation(self):
        """Test CRUD operations for Observation API endpoint."""
        # First create a garden location for the plant
        garden_location = GardenLocation(
            name='Test Garden',
            longitude=-122.4194,
            latitude=37.7749,
            sun_exposure=SunExposure.FULL,
            wind_exposure=WindExposure.PROTECTED,
            drainage=Drainage.GOOD,
            irrigation_zone_id=1
        )
        response = self.client.post('/garden_locations/', json=garden_location.json())
        self.assertEqual(response.status_code, 201)
        garden_location_id = response.json['data']['id']

        # Create a plant for the observation
        plant = Plant(
            name='Test Plant',
            scientific_name='Testus plantus',
            growth_form=GrowthForm.HERB,
            life_cycle=LifeCycle.ANNUAL,
            primary_use=UseCategory.VEGETABLE,
            garden_location_id=garden_location_id
        )
        response = self.client.post('/plants/', json=plant.json())
        self.assertEqual(response.status_code, 201)
        plant_id = response.json['data']['id']

        # Create observation using model class
        observation = Observation(
            plant_id=plant_id,
            timestamp=datetime.now(),
            observation_type=ObservationType.HEIGHT,
            numeric_value=24.5,
            stage_value=GrowthStage.VEGETATIVE,
            notes='Initial test observation',
            recorded_by='Test User'
        )

        # Create new observation
        response = self.client.post(self.BASE_URL, json=observation.json())
        self.assertEqual(response.status_code, 201)
        created_observation = response.json['data']
        self.assertEqual(created_observation['numeric_value'], observation.numeric_value)
        observation_id = created_observation['id']

        # Get the specific observation
        response = self.client.get(f"{self.BASE_URL}{observation_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_observation = response.json['data']
        self.assertEqual(retrieved_observation['numeric_value'], observation.numeric_value)

        # Get all observations and verify our observation is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        observations = response.json['data']
        self.assertTrue(any(o['id'] == observation_id for o in observations))

        # Modify the observation
        observation.numeric_value = 26.0
        observation.notes = 'Updated measurement'

        response = self.client.put(f"{self.BASE_URL}{observation_id}", json=observation.json())
        self.assertEqual(response.status_code, 200)
        modified_observation = response.json['data']
        self.assertEqual(modified_observation['numeric_value'], observation.numeric_value)
        self.assertEqual(modified_observation['notes'], observation.notes)

        # Delete the observation
        response = self.client.delete(f"{self.BASE_URL}{observation_id}")
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        response = self.client.get(f"{self.BASE_URL}{observation_id}")
        self.assertEqual(response.status_code, 404) 