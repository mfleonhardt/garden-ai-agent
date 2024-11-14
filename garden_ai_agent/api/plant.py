from flask_restx import Namespace, Resource, fields, marshal_with
from flask import request

from ..data.models import Plant
from ..data.database import db

plant_ns = Namespace('plants', description='Operations related to plants')

# Define the fields for the input model
base_plant_fields = {
    'garden_location_id': fields.Integer(required=True, description='ID of the associated garden location'),
    'name': fields.String(required=True, description='Common name of the plant'),
    'scientific_name': fields.String(description='Scientific name of the plant'),
    'variety': fields.String(description='Specific cultivar or variety'),
    'growth_form': fields.String(required=True, description='Growth form of the plant'),
    'life_cycle': fields.String(required=True, description='Life cycle of the plant'),
    'primary_use': fields.String(required=True, description='Primary use category'),
    'secondary_use': fields.String(description='Secondary use category'),
    'expected_height_inches': fields.Integer(description='Expected height in inches'),
    'expected_spread_inches': fields.Integer(description='Expected spread in inches'),
    'hardiness_zone_min': fields.Integer(description='Minimum hardiness zone'),
    'hardiness_zone_max': fields.Integer(description='Maximum hardiness zone'),
    'preferred_soil_ph_min': fields.Float(description='Minimum preferred soil pH'),
    'preferred_soil_ph_max': fields.Float(description='Maximum preferred soil pH'),
    'planting_depth_inches': fields.Float(description='Planting depth in inches'),
    'spacing_inches': fields.Integer(description='Recommended spacing between plants'),
    'description': fields.String(description='General description of the plant'),
    'care_instructions': fields.String(description='Basic care guidelines'),
    'notes': fields.String(description='Additional notes')
}

# Define the input and output models
plant_input_model = plant_ns.model('PlantInput', base_plant_fields)

plant_output_model = plant_ns.model('PlantOutput', {
    'id': fields.Integer(description='The ID of the plant'),
    **base_plant_fields
})

@plant_ns.route('/')
class PlantList(Resource):
    @marshal_with(plant_output_model, envelope='data')
    def get(self):
        """List all plants"""
        plants = Plant.query.all()
        return plants

    @plant_ns.expect(plant_input_model)
    @marshal_with(plant_output_model, envelope='data')
    def post(self):
        """Create a new plant"""
        data = request.json
        new_plant = Plant(
            garden_location_id=data['garden_location_id'],
            name=data['name'],
            scientific_name=data.get('scientific_name'),
            variety=data.get('variety'),
            growth_form=data['growth_form'],
            life_cycle=data['life_cycle'],
            primary_use=data['primary_use'],
            secondary_use=data.get('secondary_use'),
            expected_height_inches=data.get('expected_height_inches'),
            expected_spread_inches=data.get('expected_spread_inches'),
            hardiness_zone_min=data.get('hardiness_zone_min'),
            hardiness_zone_max=data.get('hardiness_zone_max'),
            preferred_soil_ph_min=data.get('preferred_soil_ph_min'),
            preferred_soil_ph_max=data.get('preferred_soil_ph_max'),
            planting_depth_inches=data.get('planting_depth_inches'),
            spacing_inches=data.get('spacing_inches'),
            description=data.get('description'),
            care_instructions=data.get('care_instructions'),
            notes=data.get('notes')
        )
        db.session.add(new_plant)
        db.session.commit()
        
        return new_plant, 201

@plant_ns.route('/<int:id>')
class PlantResource(Resource):
    @marshal_with(plant_output_model, envelope='data')
    def get(self, id):
        """Get a single plant by ID"""
        plant = Plant.query.get_or_404(id)
        return plant

    @plant_ns.expect(plant_input_model)
    @marshal_with(plant_output_model, envelope='data')
    def put(self, id):
        """Update a plant"""
        data = request.json
        plant = Plant.query.get_or_404(id)

        plant.name = data['name']
        plant.scientific_name = data.get('scientific_name')
        plant.variety = data.get('variety')
        plant.growth_form = data['growth_form']
        plant.life_cycle = data['life_cycle']
        plant.primary_use = data['primary_use']
        plant.secondary_use = data.get('secondary_use')
        plant.expected_height_inches = data.get('expected_height_inches')
        plant.expected_spread_inches = data.get('expected_spread_inches')
        plant.hardiness_zone_min = data.get('hardiness_zone_min')
        plant.hardiness_zone_max = data.get('hardiness_zone_max')
        plant.preferred_soil_ph_min = data.get('preferred_soil_ph_min')
        plant.preferred_soil_ph_max = data.get('preferred_soil_ph_max')
        plant.planting_depth_inches = data.get('planting_depth_inches')
        plant.spacing_inches = data.get('spacing_inches')
        plant.description = data.get('description')
        plant.care_instructions = data.get('care_instructions')
        plant.notes = data.get('notes')

        db.session.commit()
        return plant

    def delete(self, id):
        """Delete a plant"""
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204

