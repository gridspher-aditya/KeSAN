# tools/farm_sensor_tool.py
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

@tool
def fetch_farm_sensor_data(device_id: str, limit: int = 5) -> str:
    """
    Fetches real-time and historical sensor data from apple orchard IoT devices.
    
    This tool retrieves comprehensive environmental data including:
    - Air temperature and humidity
    - Soil temperature and humidity at surface and depth
    - Light intensity (important for photosynthesis)
    - Atmospheric pressure
    - Rainfall measurements
    - Wind speed and direction
    - Leaf wetness (critical for disease prediction)
    
    Args:
        device_id: The unique identifier for the farm's sensor device
        limit: Number of recent readings to analyze (default: 5)
        
    Returns:
        A formatted string with sensor readings and analysis
    """
    try:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        url = f"https://gridsphere.in/dapi/?d_id={device_id}"
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        readings = data.get("readings", [])
        
        if not readings:
            return f"No sensor data available for device {device_id}"
        
        # Get the most recent readings
        recent_readings = readings[:limit]
        latest = recent_readings[0]
        
        # Calculate averages from recent readings
        avg_temp = sum(float(r["temp"]) for r in recent_readings) / len(recent_readings)
        avg_humidity = sum(float(r["humidity"]) for r in recent_readings) / len(recent_readings)
        avg_surface_temp = sum(float(r["surface_temp"]) for r in recent_readings) / len(recent_readings)
        avg_depth_temp = sum(float(r["depth_temp"]) for r in recent_readings) / len(recent_readings)
        total_rainfall = sum(float(r["rainfall"]) for r in recent_readings)
        
        # Format data for LLM
        formatted_data = f"""
╔══════════════════════════════════════════════════════════════╗
║          APPLE ORCHARD SENSOR DATA (Device: {device_id})     ║
╚══════════════════════════════════════════════════════════════╝

📅 LATEST READING: {latest['timestamp']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌡️  ATMOSPHERIC CONDITIONS:
   • Air Temperature: {latest['temp']}°C (Avg: {avg_temp:.2f}°C)
   • Humidity: {latest['humidity']}% (Avg: {avg_humidity:.2f}%)
   • Atmospheric Pressure: {latest['pressure']} hPa
   • Light Intensity: {latest['light_intensity']} lux

🌧️  WEATHER PARAMETERS:
   • Rainfall: {latest['rainfall']} mm (Total: {total_rainfall:.2f} mm)
   • Wind Speed: {latest['wind_speed']} m/s
   • Wind Direction: {latest['wind_direction']}°

🌱 SOIL CONDITIONS:
   • Surface Temperature: {latest['surface_temp']}°C (Avg: {avg_surface_temp:.2f}°C)
   • Surface Humidity: {latest['surface_humidity']}%
   • Depth Temperature: {latest['depth_temp']}°C (Avg: {avg_depth_temp:.2f}°C)
   • Depth Humidity: {latest['depth_humidity']}%

🍃 DISEASE INDICATORS:
   • Leaf Wetness: {latest['leafwetness'] if latest['leafwetness'] else 'Not Available'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ANALYSIS PERIOD: Last {len(recent_readings)} readings
📈 Data Quality: {len(recent_readings)}/{limit} readings available

OPTIMAL RANGES FOR APPLE ORCHARDS:
- Air Temperature: 15-25°C (growth), 10-18°C (fruiting)
- Soil Moisture: 60-80% field capacity
- Leaf Wetness Duration: <6 hours (to prevent diseases)
"""
        
        return formatted_data
        
    except requests.exceptions.Timeout:
        return f"⚠️ Error: Request timed out while fetching data for device {device_id}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error: Failed to fetch sensor data: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in fetch_farm_sensor_data: {e}")
        return f"⚠️ Error: Unexpected error occurred: {str(e)}"


def parse_sensor_readings(readings: List[Dict]) -> Dict[str, Any]:
    """
    Helper function to parse and analyze sensor readings
    Returns structured data for programmatic use
    """
    if not readings:
        return {}
    
    latest = readings[0]
    
    return {
        "latest_reading": {
            "timestamp": latest["timestamp"],
            "air_temp": float(latest["temp"]),
            "humidity": float(latest["humidity"]),
            "light_intensity": float(latest["light_intensity"]),
            "pressure": float(latest["pressure"]),
            "rainfall": float(latest["rainfall"]),
            "wind_speed": float(latest["wind_speed"]),
            "surface_temp": float(latest["surface_temp"]),
            "surface_humidity": float(latest["surface_humidity"]),
            "depth_temp": float(latest["depth_temp"]),
            "depth_humidity": float(latest["depth_humidity"]),
            "leaf_wetness": latest["leafwetness"]
        },
        "averages": {
            "air_temp": sum(float(r["temp"]) for r in readings) / len(readings),
            "humidity": sum(float(r["humidity"]) for r in readings) / len(readings),
            "surface_temp": sum(float(r["surface_temp"]) for r in readings) / len(readings),
            "depth_temp": sum(float(r["depth_temp"]) for r in readings) / len(readings),
        },
        "totals": {
            "rainfall": sum(float(r["rainfall"]) for r in readings)
        },
        "reading_count": len(readings)
    }