from flask_restx import Namespace, Resource, fields, marshal_with
from flask import request

from ..data.models import IrrigationZone
from ..data.database import db
from flask_restx import fields as restx_fields

irrigation_zone_ns = Namespace('irrigation_zones', description='Operations related to irrigation zones')

class EnumSetField(restx_fields.Raw):
    def format(self, value):
        # Convert set of enums to sorted list of string names
        return [day.name for day in sorted(value, key=lambda x: x.value)]

base_irrigation_zone_fields = {
    'name': fields.String(required=True, description='The name of the irrigation zone'),
    'scheduled_days': EnumSetField(required=True, description='List of scheduled days'),
    'start_time': fields.String(required=True, description='Start time in HH:MM:SS format'),
    'duration_minutes': fields.Integer(required=True, description='Duration in minutes'),
    'flow_rate_gpm': fields.Float(required=True, description='Flow rate in gallons per minute')
}

irrigation_zone_input_model = irrigation_zone_ns.model('IrrigationZoneInput', base_irrigation_zone_fields)

irrigation_zone_output_model = irrigation_zone_ns.model('IrrigationZoneOutput', {
    'id': fields.Integer(description='The ID of the irrigation zone'),
    **base_irrigation_zone_fields
})

@irrigation_zone_ns.route('/')
class IrrigationZoneList(Resource):
    @marshal_with(irrigation_zone_output_model, envelope='data')
    def get(self):
        """List all irrigation zones"""
        zones = IrrigationZone.query.all()
        return zones

    @irrigation_zone_ns.expect(irrigation_zone_input_model)
    @marshal_with(irrigation_zone_output_model, envelope='data')
    def post(self):
        """Create a new irrigation zone"""
        data = request.json
        new_zone = IrrigationZone(
            name=data['name'],
            scheduled_days=data['scheduled_days'],
            start_time=data['start_time'],
            duration_minutes=data['duration_minutes'],
            flow_rate_gpm=data['flow_rate_gpm']
        )
        db.session.add(new_zone)
        db.session.commit()
        
        return new_zone, 201

@irrigation_zone_ns.route('/<int:id>')
class IrrigationZoneResource(Resource):
    @marshal_with(irrigation_zone_output_model, envelope='data')
    def get(self, id):
        """Get a single irrigation zone by ID"""
        zone = IrrigationZone.query.get_or_404(id)
        return zone

    @irrigation_zone_ns.expect(irrigation_zone_input_model)
    @marshal_with(irrigation_zone_output_model, envelope='data')
    def put(self, id):
        """Update an irrigation zone"""
        data = request.json
        zone = IrrigationZone.query.get_or_404(id)

        zone.name = data['name']
        zone.scheduled_days = data['scheduled_days']
        zone.start_time = data['start_time']
        zone.duration_minutes = data['duration_minutes']
        zone.flow_rate_gpm = data['flow_rate_gpm']

        db.session.commit()
        return zone

    def delete(self, id):
        """Delete an irrigation zone"""
        zone = IrrigationZone.query.get_or_404(id)
        db.session.delete(zone)
        db.session.commit()
        return '', 204
