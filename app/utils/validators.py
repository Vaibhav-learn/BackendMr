import re
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    pattern = r'^[0-9\-\+\s\(\)]{10,20}$'
    return bool(re.match(pattern, phone))


def validate_employee_id(employee_id: str) -> bool:
    pattern = r'^[A-Za-z0-9\-_]{3,50}$'
    return bool(re.match(pattern, employee_id))


def validate_latitude(lat: str) -> bool:
    try:
        lat_float = float(lat)
        return -90 <= lat_float <= 90
    except (ValueError, TypeError):
        return False


def validate_longitude(lon: str) -> bool:
    try:
        lon_float = float(lon)
        return -180 <= lon_float <= 180
    except (ValueError, TypeError):
        return False


def validate_coordinates(latitude: str, longitude: str) -> bool:
    return validate_latitude(latitude) and validate_longitude(longitude)


def validate_gst_number(gst: str) -> bool:
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst))
