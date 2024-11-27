from flask_restx import Namespace, Resource, fields, marshal
from flask import request
from datetime import datetime

from ..data.models import Measurement
from ..data.database import db
from ..data.fields import MeasurementType, MeasurementUnit

measurement_ns = Namespace('measurements', description='Operations related to measurements')

base_measurement_fields = {
    'garden_location_id': fields.Integer(required=True, description='ID of the associated garden location'),
    'measurement_type': fields.String(required=True, description='Type of measurement'),
    'unit': fields.String(required=True, description='Unit of measurement'),
    'value': fields.Float(required=True, description='Measurement value'),
    'timestamp': fields.DateTime(description='When the measurement was taken'),
    'period_minutes': fields.Integer(description='Period over which measurement was taken (in minutes)'),
    'source': fields.String(description='Source of the measurement'),
    'notes': fields.String(description='Additional notes about the measurement')
}

measurement_input_model = measurement_ns.model('MeasurementInput', base_measurement_fields)

measurement_output_model = measurement_ns.model('MeasurementOutput', {
    'id': fields.Integer(description='The ID of the measurement'),
    **base_measurement_fields
})

@measurement_ns.route('/')
class MeasurementList(Resource):
    def get(self):
        """List all measurements"""
        measurements = Measurement.query.all()
        return marshal(measurements, measurement_output_model, envelope='data')

    @measurement_ns.expect(measurement_input_model)
    def post(self):
        """Create a new measurement"""
        data = request.json
        try:
            # Validate measurement_type and unit values
            if data['measurement_type'] not in MeasurementType.__members__:
                raise ValueError("Invalid value for field: 'measurement_type'")
            if data['unit'] not in MeasurementUnit.__members__:
                raise ValueError("Invalid value for field: 'unit'")

            # Parse timestamp if it's provided as string
            timestamp = (
                datetime.fromisoformat(data['timestamp'])
                if isinstance(data.get('timestamp'), str)
                else data.get('timestamp', datetime.utcnow())
            )

            new_measurement = Measurement(
                garden_location_id=data['garden_location_id'],
                measurement_type=MeasurementType[data['measurement_type']],
                unit=MeasurementUnit[data['unit']],
                value=data['value'],
                timestamp=timestamp,
                period_minutes=data.get('period_minutes'),
                source=data.get('source'),
                notes=data.get('notes')
            )
            db.session.add(new_measurement)
            db.session.commit()
            return marshal(new_measurement, measurement_output_model, envelope='data'), 201
        except KeyError as e:
            return {"error": f"Missing required field: {str(e)}"}, 400
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400

@measurement_ns.route('/<int:id>')
class MeasurementResource(Resource):
    def get(self, id):
        """Get a single measurement by ID"""
        measurement = Measurement.query.get_or_404(id)
        return marshal(measurement, measurement_output_model, envelope='data')

    @measurement_ns.expect(measurement_input_model)
    def put(self, id):
        """Update a measurement"""
        data = request.json
        measurement = Measurement.query.get_or_404(id)

        try:
            if 'measurement_type' in data:
                measurement.measurement_type = MeasurementType[data['measurement_type']]
            if 'unit' in data:
                measurement.unit = MeasurementUnit[data['unit']]
            if 'value' in data:
                measurement.value = data['value']
            if 'timestamp' in data:
                measurement.timestamp = (
                    datetime.fromisoformat(data['timestamp'])
                    if isinstance(data['timestamp'], str)
                    else data['timestamp']
                )
            if 'period_minutes' in data:
                measurement.period_minutes = data['period_minutes']
            if 'source' in data:
                measurement.source = data['source']
            if 'notes' in data:
                measurement.notes = data['notes']

            db.session.commit()
            return marshal(measurement, measurement_output_model, envelope='data')
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400

    def delete(self, id):
        """Delete a measurement"""
        measurement = Measurement.query.get_or_404(id)
        db.session.delete(measurement)
        db.session.commit()
        return '', 204 