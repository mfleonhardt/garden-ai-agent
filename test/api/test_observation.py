from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import ObservationType, GrowthStage
from datetime import datetime
from .test_api import APITest

class Test_Observation(APITest):

    BASE_URL = BASE_URL + '/observations/'

    def test_create_verify_delete_observation(self):
        """Test CRUD operations for Observation API endpoint.
        
        Tests:
        - Creating an observation with valid data
        - Retrieving the created observation
        - Verifying observation appears in list endpoint
        - Modifying observation attributes
        - Deleting the observation
        """
        # First create a garden location and plant for the observation
        garden_location_data = {
            'name': 'Test Garden',
            'longitude': -122.4194,
            'latitude': 37.7749,
            'sun_exposure': 'FULL',
            'wind_exposure': 'PROTECTED',
            'drainage': 'GOOD',
            'irrigation_zone_id': 1
        }
        response = self.client.post('/garden_locations/', json=garden_location_data)
        self.assertEqual(response.status_code, 201)
        garden_location_id = response.json['data']['id']

        # Create a plant
        plant_data = {
            'name': 'Test Plant',
            'scientific_name': 'Testus plantus',
            'growth_form': 'HERB',
            'life_cycle': 'ANNUAL',
            'primary_use': 'VEGETABLE',
            'garden_location_id': garden_location_id
        }
        response = self.client.post('/plants/', json=plant_data)
        self.assertEqual(response.status_code, 201)
        plant_id = response.json['data']['id']

        # Create observation data
        observation_data = {
            'plant_id': plant_id,
            'timestamp': datetime.now().isoformat(),
            'observation_type': ObservationType.HEIGHT.value,
            'numeric_value': 24.5,
            'stage_value': GrowthStage.VEGETATIVE.value,
            'notes': 'Plant is growing well',
            'recorded_by': 'Test User'
        }

        # Create new observation
        response = self.client.post(self.BASE_URL, json=observation_data)
        self.assertEqual(response.status_code, 201)
        created_observation = response.json['data']
        self.assertEqual(created_observation['numeric_value'], observation_data['numeric_value'])
        observation_id = created_observation['id']

        # Get the specific observation
        response = self.client.get(f"{self.BASE_URL}{observation_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_observation = response.json['data']
        self.assertEqual(retrieved_observation['numeric_value'], observation_data['numeric_value'])

        # Get all observations and verify our observation is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        observations = response.json['data']
        self.assertTrue(any(o['id'] == observation_id for o in observations))

        # Modify the observation
        observation_data['numeric_value'] = 30.0
        observation_data['notes'] = 'Plant has grown significantly'

        response = self.client.put(f"{self.BASE_URL}{observation_id}", json=observation_data)
        self.assertEqual(response.status_code, 200)
        modified_observation = response.json['data']
        self.assertEqual(modified_observation['numeric_value'], observation_data['numeric_value'])
        self.assertEqual(modified_observation['notes'], observation_data['notes'])

        # Delete the observation
        response = self.client.delete(f"{self.BASE_URL}{observation_id}")
        self.assertEqual(response.status_code, 204) 