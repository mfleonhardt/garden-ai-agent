from flask_restx import Namespace, Resource, fields, marshal
from flask import request

from ..data.models import GardenLocation
from ..data.database import db
from ..data.fields import SunExposure, WindExposure, Drainage

garden_location_ns = Namespace('garden_locations', description='Operations related to garden locations')

base_garden_location_fields = {
    'name': fields.String(required=True, description='The name of the garden location'),
    'longitude': fields.Float(required=True, description='The longitude of the garden location'),
    'latitude': fields.Float(required=True, description='The latitude of the garden location'),
    'elevation': fields.Float(description='The elevation of the garden location'),
    'sun_exposure': fields.String(required=True, description='The sun exposure of the garden location. Possible values: FULL, PARTIAL_SUN, PARTIAL_SHADE, DAPPLED, FULL_SHADE'),
    'wind_exposure': fields.String(required=True, description='The wind exposure of the garden location. Possible values: EXPOSED, PARTIALLY_EXPOSED, PROTECTED, INDOOR'),
    'drainage': fields.String(required=True, description='The drainage of the garden location. Possible values: EXCELLENT, GOOD, POOR')
}

garden_location_input_model = garden_location_ns.model('GardenLocationInput', base_garden_location_fields)

garden_location_output_model = garden_location_ns.model('GardenLocationOutput', {
    'id': fields.Integer(description='The ID of the garden location'),
    **base_garden_location_fields
})

@garden_location_ns.route('/')
class GardenLocationList(Resource):
    def get(self):
        """List all garden locations"""
        locations = GardenLocation.query.all()
        return marshal(locations, garden_location_output_model, envelope='data')

    @garden_location_ns.expect(garden_location_input_model)
    def post(self):
        """Create a new garden location"""
        data = request.json
        try:
            # Validate sun_exposure, wind_exposure, and drainage values
            if data['sun_exposure'] not in SunExposure.__members__:
                raise ValueError("Invalid value for field: 'sun_exposure'")
            if data['wind_exposure'] not in WindExposure.__members__:
                raise ValueError("Invalid value for field: 'wind_exposure'")
            if data['drainage'] not in Drainage.__members__:
                raise ValueError("Invalid value for field: 'drainage'")

            new_location = GardenLocation(
                name=data['name'],
                longitude=data['longitude'],
                latitude=data['latitude'],
                elevation=data.get('elevation'),
                sun_exposure=SunExposure[data['sun_exposure']],
                wind_exposure=WindExposure[data['wind_exposure']],
                drainage=Drainage[data['drainage']],
                irrigation_zone_id=data['irrigation_zone_id']
            )
            db.session.add(new_location)
            db.session.commit()
            return marshal(new_location, garden_location_output_model, envelope='data'), 201
        except KeyError as e:
            return {"error": f"Missing field: {str(e)}"}, 400
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400

@garden_location_ns.route('/<int:id>')
class GardenLocationResource(Resource):
    def get(self, id):
        """Get a single garden location by ID"""
        location = GardenLocation.query.get_or_404(id)
        return marshal(location, garden_location_output_model, envelope='data')

    @garden_location_ns.expect(garden_location_input_model)
    def put(self, id):
        """Update a garden location"""
        data = request.json
        location = GardenLocation.query.get_or_404(id)

        location.name = data['name']
        location.longitude = data['longitude']
        location.latitude = data['latitude']
        location.elevation = data.get('elevation')
        location.sun_exposure = data['sun_exposure']
        location.wind_exposure = data['wind_exposure']
        location.drainage = data['drainage']

        db.session.commit()
        return marshal(location, garden_location_output_model, envelope='data')

    def delete(self, id):
        """Delete a garden location"""
        location = GardenLocation.query.get_or_404(id)
        db.session.delete(location)
        db.session.commit()
        return '', 204
