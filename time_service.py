"""Time service for getting current date and time information."""
from datetime import datetime
import pytz
from typing import Dict, Any


class TimeService:
    """Service for getting current date and time information."""
    
    def __init__(self):
        """Initialize the time service."""
        # Default timezone (Cairo, Egypt)
        self.default_timezone = pytz.timezone('Africa/Cairo')
    
    def get_current_time(self, timezone: str = None) -> Dict[str, Any]:
        """Get current date and time information."""
        try:
            # Use provided timezone or default
            tz = pytz.timezone(timezone) if timezone else self.default_timezone
            
            # Get current time in the specified timezone
            now = datetime.now(tz)
            
            # Format different time representations
            time_data = {
                "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "day_of_week": now.strftime("%A"),
                "month": now.strftime("%B"),
                "year": now.year,
                "hour_12": now.strftime("%I:%M %p"),
                "timezone": str(tz),
                "timestamp": now.timestamp(),
                "formatted_long": now.strftime("%A, %B %d, %Y at %I:%M %p"),
                "formatted_short": now.strftime("%m/%d/%Y %H:%M")
            }
            
            print(f"SUCCESS: Current time retrieved for {tz}")
            return time_data
            
        except Exception as e:
            print(f"ERROR: Failed to get time data: {str(e)}")
            return {
                "error": f"Failed to get time data: {str(e)}",
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_time_summary(self, timezone: str = None) -> str:
        """Get a human-readable time summary."""
        time_data = self.get_current_time(timezone)
        
        if "error" in time_data:
            return f"Time data unavailable: {time_data['error']}"
        
        return f"""Current Date and Time:
Date: {time_data['date']}
Time: {time_data['time']} ({time_data['hour_12']})
Day: {time_data['day_of_week']}
Month: {time_data['month']} {time_data['year']}
Timezone: {time_data['timezone']}
Formatted: {time_data['formatted_long']}"""


def get_time_service() -> TimeService:
    """Get a time service instance."""
    return TimeService()
