from flask_restx import Namespace, Resource, fields, marshal_with
from flask import request
from datetime import datetime

from ..data.models import Observation
from ..data.database import db
from ..data.fields import ObservationType, GrowthStage

observation_ns = Namespace('observations', description='Operations related to plant observations')

# Define the fields for the input model
base_observation_fields = {
    'plant_id': fields.Integer(required=True, description='ID of the associated plant'),
    'timestamp': fields.DateTime(required=True, description='When the observation was made'),
    'observation_type': fields.String(required=True, description='Type of observation'),
    'numeric_value': fields.Float(description='Numeric measurement value'),
    'stage_value': fields.String(description='Growth stage value'),
    'notes': fields.String(description='Additional notes about the observation'),
    'image_data': fields.String(description='Base64 encoded image data'),
    'recorded_by': fields.String(description='User who recorded the observation')
}

# Define the input and output models
observation_input_model = observation_ns.model('ObservationInput', base_observation_fields)

observation_output_model = observation_ns.model('ObservationOutput', {
    'id': fields.Integer(description='The ID of the observation'),
    **base_observation_fields
})

@observation_ns.route('/')
class ObservationList(Resource):
    @marshal_with(observation_output_model, envelope='data')
    def get(self):
        """List all observations"""
        observations = Observation.query.all()
        return observations

    @observation_ns.expect(observation_input_model)
    @marshal_with(observation_output_model, envelope='data')
    def post(self):
        """Create a new observation"""
        data = request.json
        
        # Parse timestamp if it's provided as string
        timestamp = datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp']
        
        new_observation = Observation(
            plant_id=data['plant_id'],
            timestamp=timestamp,
            observation_type=data['observation_type'],
            numeric_value=data.get('numeric_value'),
            stage_value=data.get('stage_value'),
            notes=data.get('notes'),
            image_data=data.get('image_data').encode('utf-8') if data.get('image_data') else None,
            recorded_by=data.get('recorded_by')
        )
        
        db.session.add(new_observation)
        db.session.commit()
        
        return new_observation, 201

@observation_ns.route('/<int:id>')
class ObservationResource(Resource):
    @marshal_with(observation_output_model, envelope='data')
    def get(self, id):
        """Get a single observation by ID"""
        observation = Observation.query.get_or_404(id)
        return observation

    @observation_ns.expect(observation_input_model)
    @marshal_with(observation_output_model, envelope='data')
    def put(self, id):
        """Update an observation"""
        data = request.json
        observation = Observation.query.get_or_404(id)

        # Parse timestamp if it's provided as string
        if 'timestamp' in data:
            observation.timestamp = (
                datetime.fromisoformat(data['timestamp']) 
                if isinstance(data['timestamp'], str) 
                else data['timestamp']
            )
        
        if 'observation_type' in data:
            observation.observation_type = data['observation_type']
        if 'numeric_value' in data:
            observation.numeric_value = data.get('numeric_value')
        if 'stage_value' in data:
            observation.stage_value = data.get('stage_value')
        if 'notes' in data:
            observation.notes = data.get('notes')
        if 'image_data' in data:
            observation.image_data = data.get('image_data').encode('utf-8') if data.get('image_data') else None
        if 'recorded_by' in data:
            observation.recorded_by = data.get('recorded_by')

        db.session.commit()
        return observation

    def delete(self, id):
        """Delete an observation"""
        observation = Observation.query.get_or_404(id)
        db.session.delete(observation)
        db.session.commit()
        return '', 204 