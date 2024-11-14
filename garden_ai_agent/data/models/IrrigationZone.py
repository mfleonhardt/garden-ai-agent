from sqlalchemy.orm import validates
from typing import List, Set
from datetime import time

from ..database import db
from ..fields import Day

class IrrigationZone(db.Model):
    """
    Represents an irrigation zone with scheduled watering days and associated garden locations.
    
    Each zone has a specific watering schedule, duration, and flow rate, and can contain
    multiple garden locations that are watered simultaneously when the zone is active.
    """
    __tablename__ = 'irrigation_zones'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Added length constraint
    _scheduled_days = db.Column('scheduled_days', db.String(100), nullable=False)
    _start_time = db.Column('start_time', db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    flow_rate_gpm = db.Column(db.Float, nullable=False)
    garden_locations = db.relationship(
        'GardenLocation',
        backref='irrigation_zone',
        lazy='select'  # Explicit loading strategy
    )

    @validates('name')
    def validate_name(self, key, value):
        """Validates that the zone name is not empty and within length limits."""
        if not value or not value.strip():
            raise ValueError("Zone name cannot be empty")
        if len(value) > 100:
            raise ValueError("Zone name cannot exceed 100 characters")
        return value.strip()

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        """Validates that the duration is within acceptable limits."""
        if not isinstance(value, (int, float)):
            raise TypeError("Duration must be a number")
        if value <= 0:
            raise ValueError("Duration must be greater than 0 minutes")
        if value > 120:
            raise ValueError("Duration must be 120 minutes or less")
        return int(value)  # Ensure integer value

    @validates('flow_rate_gpm')
    def validate_flow_rate_gpm(self, key, value):
        """Validates that the flow rate is positive."""
        if not isinstance(value, (int, float)):
            raise TypeError("Flow rate must be a number")
        if value <= 0:
            raise ValueError("Flow rate must be greater than 0 gallons per minute")
        return float(value)  # Ensure float value

    def __repr__(self):
        return f"<IrrigationZone (name={self.name})>"

    @property
    def scheduled_days(self) -> Set[Day]:
        """
        Gets the set of scheduled irrigation days.
        
        Returns:
            Set[Day]: Set of Day enum values representing scheduled watering days
        """
        if not self._scheduled_days:
            return set()
        return {Day(int(day)) for day in self._scheduled_days.split(',')}

    @scheduled_days.setter
    def scheduled_days(self, days: List[Day | str | int] | Set[Day | str | int]) -> None:
        """
        Sets the scheduled irrigation days with flexible input formats.
        
        Args:
            days: List or Set of values representing days. Accepts:
                - Day enum values
                - Integers (0-6)
                - Strings: Full names (e.g., "MONDAY", "Monday")
                          Short names (e.g., "Mon", "M")
                          Comma-separated strings (e.g., "M,T,W")
            
        Raises:
            ValueError: If days is empty or contains invalid day representations
        """
        if isinstance(days, str):
            # Handle comma-separated string input
            days = [d.strip() for d in days.split(',')]

        days_set = set()
        
        def parse_day(day) -> Day:
            if isinstance(day, Day):
                return day
            if isinstance(day, int) and 0 <= day <= 6:
                return Day(day)
            if isinstance(day, str):
                day = day.strip().upper()
                # Handle full names
                try:
                    return Day[day]
                except KeyError:
                    # Handle short names
                    short_names = {
                        'SUN': Day.SUNDAY, 'S': Day.SUNDAY, '0': Day.SUNDAY,
                        'MON': Day.MONDAY, 'M': Day.MONDAY, '1': Day.MONDAY,
                        'TUE': Day.TUESDAY, 'T': Day.TUESDAY, '2': Day.TUESDAY,
                        'WED': Day.WEDNESDAY, 'W': Day.WEDNESDAY, '3': Day.WEDNESDAY,
                        'THU': Day.THURSDAY, 'TH': Day.THURSDAY, '4': Day.THURSDAY,
                        'FRI': Day.FRIDAY, 'F': Day.FRIDAY, '5': Day.FRIDAY,
                        'SAT': Day.SATURDAY, 'SA': Day.SATURDAY, '6': Day.SATURDAY,
                    }
                    if day in short_names:
                        return short_names[day]
                raise ValueError(f"Invalid day format: {day}")

        for day in days:
            try:
                days_set.add(parse_day(day))
            except ValueError as e:
                raise ValueError(f"Invalid day value: {day}. Use Day enum, integers (0-6), "
                               "or strings (e.g., 'MONDAY', 'Mon', 'M')")

        if not days_set:
            raise ValueError("Scheduled days cannot be empty")

        self._scheduled_days = ','.join(str(day.value) for day in sorted(days_set, key=lambda d: d.value))

    def is_scheduled_for_day(self, day: Day) -> bool:
        """
        Checks if irrigation is scheduled for a specific day.
        
        Args:
            day: Day enum value to check
            
        Returns:
            bool: True if irrigation is scheduled for the given day
        """
        if not isinstance(day, Day):
            raise TypeError("Day parameter must be a Day enum value")
        return day in self.scheduled_days

    def add_scheduled_day(self, day: Day) -> None:
        """
        Adds a day to the irrigation schedule.
        
        Args:
            day: Day enum value to add
            
        Raises:
            TypeError: If day is not a Day enum value
        """
        if not isinstance(day, Day):
            raise TypeError("Day parameter must be a Day enum value")
        current_days = self.scheduled_days
        current_days.add(day)
        self.scheduled_days = current_days

    def remove_scheduled_day(self, day: Day) -> None:
        """
        Removes a day from the irrigation schedule.
        
        Args:
            day: Day enum value to remove
            
        Raises:
            ValueError: If attempting to remove the last scheduled day
            TypeError: If day is not a Day enum value
            KeyError: If day is not in the schedule
        """
        if not isinstance(day, Day):
            raise TypeError("Day parameter must be a Day enum value")
        current_days = self.scheduled_days
        if len(current_days) <= 1:
            raise ValueError("Cannot remove the last scheduled day")
        if day not in current_days:
            raise KeyError(f"{day.value} is not in the schedule")
        current_days.remove(day)
        self.scheduled_days = current_days

    @property
    def start_time(self) -> time:
        """Gets the irrigation start time."""
        return self._start_time
    
    @start_time.setter
    def start_time(self, value: str | time) -> None:
        """Sets the irrigation start time.
        
        Args:
            value: Time string in 'HH:MM' or 'HH:MM:SS' format, or time object

        Raises:
            ValueError: If time string is invalid
        """
        if isinstance(value, str):
            try:
                parts = value.split(':')
                if len(parts) == 2:
                    value = time(int(parts[0]), int(parts[1]))
                else:
                    value = time.fromisoformat(value)
            except ValueError as e:
                raise ValueError(f"Invalid time format. Use 'HH:MM' or 'HH:MM:SS'. Error: {str(e)}")
        
        self._start_time = value

    def get_water_usage(self) -> float:
        """
        Calculates the water usage for one irrigation cycle.
        
        Returns:
            float: Water usage in gallons
        """
        return float(self.duration_minutes * self.flow_rate_gpm)

    def json(self):
        """
        Converts the irrigation zone instance to a JSON-serializable dictionary.
        
        Returns:
            dict: A dictionary representation of the irrigation zone.
        """
        return {
            'id': self.id,
            'name': self.name,
            'scheduled_days': [day.value for day in self.scheduled_days],
            'start_time': self.start_time if isinstance(self.start_time, str) else self.start_time.strftime('%H:%M:%S'),
            'duration_minutes': self.duration_minutes,
            'flow_rate_gpm': self.flow_rate_gpm
        }