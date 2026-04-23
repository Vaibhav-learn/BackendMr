"""
Utility Helper Functions
"""
from typing import Dict, Any, Optional
import math


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance


def is_within_geofence(
    user_lat: float, 
    user_lon: float, 
    assigned_lat: float, 
    assigned_lon: float, 
    radius_km: float = 5.0
) -> bool:
    """
    Check if user is within geofence radius
    """
    distance = calculate_distance(user_lat, user_lon, assigned_lat, assigned_lon)
    return distance <= radius_km


def paginate_query(query, page: int = 1, page_size: int = 10):
    """
    Paginate database query
    """
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()


def get_pagination_meta(total_count: int, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    Generate pagination metadata
    """
    total_pages = (total_count + page_size - 1) // page_size
    return {
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
    }


def format_error_response(detail: str, error_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Format error response
    """
    return {
        "detail": detail,
        "error_code": error_code or "ERROR",
    }
