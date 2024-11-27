from garden_ai_agent.config import BASE_URL
from garden_ai_agent.data.fields import MeasurementType, MeasurementUnit, SunExposure, WindExposure, Drainage
from garden_ai_agent.data.models import Measurement, GardenLocation
from datetime import datetime
from .test_api import APITest

class Test_Measurement(APITest):

    BASE_URL = BASE_URL + '/measurements/'

    def test_create_verify_delete_measurement(self):
        """Test CRUD operations for Measurement API endpoint.
        
        Tests:
        - Creating a measurement with valid data
        - Retrieving the created measurement
        - Verifying measurement appears in list endpoint
        - Modifying measurement attributes
        - Deleting the measurement
        """
        # First create a garden location for the measurement
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

        # Create measurement using the model class
        measurement = Measurement(
            garden_location_id=garden_location_id,
            measurement_type=MeasurementType.TEMPERATURE,
            unit=MeasurementUnit.CELSIUS,
            value=22.5,
            timestamp=datetime.now(),
            period_minutes=15,
            source='Test Sensor',
            notes='Initial test measurement'
        )

        # Create new measurement
        response = self.client.post(self.BASE_URL, json=measurement.json())
        self.assertEqual(response.status_code, 201, response.text)
        created_measurement = response.json['data']
        self.assertEqual(created_measurement['value'], measurement.value)
        measurement_id = created_measurement['id']

        # Get the specific measurement
        response = self.client.get(f"{self.BASE_URL}{measurement_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_measurement = response.json['data']
        self.assertEqual(retrieved_measurement['value'], measurement.value)

        # Get all measurements and verify our measurement is in the list
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        measurements = response.json['data']
        self.assertTrue(any(m['id'] == measurement_id for m in measurements))

        # Modify the measurement
        measurement.value = 23.5
        measurement.notes = 'Modified test measurement'

        response = self.client.put(f"{self.BASE_URL}{measurement_id}", json=measurement.json())
        self.assertEqual(response.status_code, 200)
        modified_measurement = response.json['data']
        self.assertEqual(modified_measurement['value'], measurement.value)
        self.assertEqual(modified_measurement['notes'], measurement.notes)

        # Delete the measurement
        response = self.client.delete(f"{self.BASE_URL}{measurement_id}")
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        response = self.client.get(f"{self.BASE_URL}{measurement_id}")
        self.assertEqual(response.status_code, 404) 