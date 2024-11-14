from ..database import db
from ..fields import ObservationType, GrowthStage

class Observation(db.Model):
    """
    Temporal model for tracking plant growth and health observations over time.
    Each record represents a single observation at a specific point in time.
    """
    __tablename__ = 'observations'

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(
        db.Integer, 
        db.ForeignKey('plants.id', name='fk_observations_plant'),
        nullable=False
    )
    timestamp = db.Column(db.DateTime, nullable=False)
    
    # Type of observation being recorded
    observation_type = db.Column(db.Enum(ObservationType), nullable=False)
    
    # The actual measurement/observation value
    numeric_value = db.Column(db.Float, nullable=True)  # For quantitative measurements
    stage_value = db.Column(db.Enum(GrowthStage), nullable=True)  # For growth stage observations
    
    # Optional fields for additional context
    notes = db.Column(db.Text, nullable=True)
    image_data = db.Column(db.BLOB, nullable=True)  # Base64 encoded image data
    recorded_by = db.Column(db.String(100), nullable=True)  # User who made the observation

    def __repr__(self):
        return f"<Observation(plant_id={self.plant_id}, type={self.observation_type}, timestamp={self.timestamp})>"

    def json(self):
        """Returns a dictionary representation suitable for JSON serialization"""
        return {
            'id': self.id,
            'plant_id': self.plant_id,
            'timestamp': self.timestamp.isoformat(),
            'observation_type': self.observation_type.name,
            'numeric_value': self.numeric_value,
            'stage_value': self.stage_value.name if self.stage_value else None,
            'notes': self.notes,
            'image_data': self.image_data.decode('utf-8') if self.image_data else None,
            'recorded_by': self.recorded_by
        }
