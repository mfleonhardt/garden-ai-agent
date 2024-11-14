from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import GrowthForm, LifeCycle, UseCategory
from garden_ai_agent.data.models import Plant
from .test_api import APITest

class Test_Plant(APITest):

    BASE_URL = BASE_URL + '/plants/'

    def test_create_verify_delete_plant(self):
        """Test CRUD operations for Plant API endpoint.
        
        Tests:
        - Creating a plant with valid data
        - Retrieving the created plant
        - Verifying plant appears in list endpoint
        - Modifying plant attributes
        - Deleting the plant
        """
        # First create a garden location for the plant
        garden_location_data = {
            'name': 'Test Garden',
            'longitude': -122.4194,
            'latitude': 37.7749,
            'sun_exposure': 'FULL',
            'wind_exposure': 'PROTECTED',
            'drainage': 'GOOD',
            'irrigation_zone_id': 1  # Assuming this exists
        }
        response = self.client.post('/garden_locations/', json=garden_location_data)
        self.assertEqual(response.status_code, 201)
        garden_location_id = response.json['data']['id']

        plant = Plant(
            name='Tomato',
            scientific_name='Solanum lycopersicum',
            variety='Better Boy',
            growth_form=GrowthForm.HERB,
            life_cycle=LifeCycle.ANNUAL,
            primary_use=UseCategory.VEGETABLE,
            secondary_use=UseCategory.POLLINATOR,
            expected_height_inches=48,
            expected_spread_inches=24,
            hardiness_zone_min=5,
            hardiness_zone_max=9,
            preferred_soil_ph_min=6.0,
            preferred_soil_ph_max=6.8,
            planting_depth_inches=0.25,
            spacing_inches=24,
            description='Indeterminate tomato variety',
            care_instructions='Water regularly, provide support',
            notes='Plant after last frost',
            garden_location_id=garden_location_id
        )

        # Create new plant
        response = self.client.post(self.BASE_URL, json=plant.json())
        self.assertEqual(response.status_code, 201)
        created_plant = response.json['data']
        self.assertEqual(created_plant['name'], plant.name)
        plant_id = created_plant['id']

        # Get the specific plant
        response = self.client.get(f"{self.BASE_URL}{plant_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_plant = response.json['data']
        self.assertEqual(retrieved_plant['name'], plant.name)

        # Get all plants and verify our plant is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        plants = response.json['data']
        self.assertTrue(any(p['id'] == plant_id for p in plants))

        # Modify the plant
        plant.name = 'Better Boy Tomato'
        plant.expected_height_inches = 60

        response = self.client.put(f"{self.BASE_URL}{plant_id}", json=plant.json())
        self.assertEqual(response.status_code, 200)
        modified_plant = response.json['data']
        self.assertEqual(modified_plant['name'], plant.name)
        self.assertEqual(modified_plant['expected_height_inches'], plant.expected_height_inches)

        # Delete the plant
        response = self.client.delete(f"{self.BASE_URL}{plant_id}")
        self.assertEqual(response.status_code, 204) 