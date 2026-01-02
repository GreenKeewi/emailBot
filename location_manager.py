"""
Location management for province-wide coverage.
Handles city/town data and grid-based search coordination.
"""

from typing import List, Dict, Tuple
import math


class LocationManager:
    """Manages location data and search grid generation."""
    
    # Province data with major cities and their coordinates
    PROVINCE_DATA = {
        'Ontario': [
            {'city': 'Toronto', 'lat': 43.6532, 'lon': -79.3832},
            {'city': 'Ottawa', 'lat': 45.4215, 'lon': -75.6972},
            {'city': 'Mississauga', 'lat': 43.5890, 'lon': -79.6441},
            {'city': 'Brampton', 'lat': 43.7315, 'lon': -79.7624},
            {'city': 'Hamilton', 'lat': 43.2557, 'lon': -79.8711},
            {'city': 'London', 'lat': 42.9849, 'lon': -81.2453},
            {'city': 'Markham', 'lat': 43.8561, 'lon': -79.3370},
            {'city': 'Vaughan', 'lat': 43.8361, 'lon': -79.4983},
            {'city': 'Kitchener', 'lat': 43.4516, 'lon': -80.4925},
            {'city': 'Windsor', 'lat': 42.3149, 'lon': -83.0364},
            {'city': 'Richmond Hill', 'lat': 43.8828, 'lon': -79.4403},
            {'city': 'Oakville', 'lat': 43.4675, 'lon': -79.6877},
            {'city': 'Burlington', 'lat': 43.3255, 'lon': -79.7990},
            {'city': 'Oshawa', 'lat': 43.8971, 'lon': -78.8658},
            {'city': 'Barrie', 'lat': 44.3894, 'lon': -79.6903},
            {'city': 'Sudbury', 'lat': 46.4917, 'lon': -80.9930},
            {'city': 'Kingston', 'lat': 44.2312, 'lon': -76.4860},
            {'city': 'Waterloo', 'lat': 43.4643, 'lon': -80.5204},
            {'city': 'Guelph', 'lat': 43.5448, 'lon': -80.2482},
            {'city': 'Cambridge', 'lat': 43.3616, 'lon': -80.3144},
            {'city': 'Whitby', 'lat': 43.8975, 'lon': -78.9429},
            {'city': 'Ajax', 'lat': 43.8509, 'lon': -79.0204},
            {'city': 'Pickering', 'lat': 43.8384, 'lon': -79.0868},
            {'city': 'Newmarket', 'lat': 44.0592, 'lon': -79.4613},
            {'city': 'Niagara Falls', 'lat': 43.0896, 'lon': -79.0849},
            {'city': 'St Catharines', 'lat': 43.1594, 'lon': -79.2469},
            {'city': 'Brantford', 'lat': 43.1394, 'lon': -80.2644},
            {'city': 'Peterborough', 'lat': 44.3091, 'lon': -78.3197},
            {'city': 'Thunder Bay', 'lat': 48.3809, 'lon': -89.2477},
            {'city': 'Sault Ste Marie', 'lat': 46.5136, 'lon': -84.3468},
            {'city': 'Sarnia', 'lat': 42.9745, 'lon': -82.4066},
            {'city': 'Welland', 'lat': 42.9834, 'lon': -79.2482},
            {'city': 'North Bay', 'lat': 46.3091, 'lon': -79.4608},
            {'city': 'Belleville', 'lat': 44.1628, 'lon': -77.3832},
            {'city': 'Cornwall', 'lat': 45.0275, 'lon': -74.7400},
            {'city': 'Chatham', 'lat': 42.4048, 'lon': -82.1910},
            {'city': 'Georgetown', 'lat': 43.6483, 'lon': -79.9328},
            {'city': 'Milton', 'lat': 43.5183, 'lon': -79.8774},
            {'city': 'Orangeville', 'lat': 43.9197, 'lon': -80.0942},
            {'city': 'Orillia', 'lat': 44.6082, 'lon': -79.4196},
            {'city': 'Stratford', 'lat': 43.3701, 'lon': -80.9819},
            {'city': 'Woodstock', 'lat': 43.1315, 'lon': -80.7467},
            {'city': 'Bowmanville', 'lat': 43.9128, 'lon': -78.6878},
            {'city': 'Leamington', 'lat': 42.0534, 'lon': -82.5998},
            {'city': 'Stouffville', 'lat': 43.9706, 'lon': -79.2450},
        ],
        'Quebec': [
            {'city': 'Montreal', 'lat': 45.5017, 'lon': -73.5673},
            {'city': 'Quebec City', 'lat': 46.8139, 'lon': -71.2080},
            {'city': 'Laval', 'lat': 45.6066, 'lon': -73.7124},
            {'city': 'Gatineau', 'lat': 45.4765, 'lon': -75.7013},
            {'city': 'Longueuil', 'lat': 45.5312, 'lon': -73.5185},
        ],
        'British Columbia': [
            {'city': 'Vancouver', 'lat': 49.2827, 'lon': -123.1207},
            {'city': 'Surrey', 'lat': 49.1913, 'lon': -122.8490},
            {'city': 'Burnaby', 'lat': 49.2488, 'lon': -122.9805},
            {'city': 'Richmond', 'lat': 49.1666, 'lon': -123.1336},
            {'city': 'Victoria', 'lat': 48.4284, 'lon': -123.3656},
        ],
        'Alberta': [
            {'city': 'Calgary', 'lat': 51.0447, 'lon': -114.0719},
            {'city': 'Edmonton', 'lat': 53.5461, 'lon': -113.4938},
            {'city': 'Red Deer', 'lat': 52.2681, 'lon': -113.8111},
            {'city': 'Lethbridge', 'lat': 49.6942, 'lon': -112.8328},
        ]
    }
    
    def __init__(self, default_radius: int = 5000):
        """
        Initialize location manager.
        
        Args:
            default_radius: Default search radius in meters
        """
        self.default_radius = default_radius
    
    def get_province_cities(self, province: str) -> List[Dict]:
        """
        Get all cities for a province.
        
        Args:
            province: Province name
            
        Returns:
            List of city dictionaries with name, lat, lon
        """
        return self.PROVINCE_DATA.get(province, [])
    
    def generate_search_grids(self, city: Dict, radius: int = None) -> List[Tuple[float, float, int]]:
        """
        Generate search grid points for a city.
        For smaller cities, use a single center point.
        For larger cities, generate multiple overlapping search areas.
        
        Args:
            city: Dictionary with city, lat, lon
            radius: Search radius in meters (uses default if None)
            
        Returns:
            List of tuples (latitude, longitude, radius)
        """
        if radius is None:
            radius = self.default_radius
        
        city_name = city['city']
        base_lat = city['lat']
        base_lon = city['lon']
        
        # Major cities need multiple grid points
        major_cities = ['Toronto', 'Ottawa', 'Mississauga', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton']
        
        if city_name in major_cities:
            # Generate a 3x3 grid for major cities
            grids = []
            # Approximate degrees per km at typical Canadian latitudes
            lat_offset = 0.045  # ~5km
            lon_offset = 0.065  # ~5km (adjusted for latitude)
            
            for lat_mult in [-1, 0, 1]:
                for lon_mult in [-1, 0, 1]:
                    lat = base_lat + (lat_mult * lat_offset)
                    lon = base_lon + (lon_mult * lon_offset)
                    grids.append((lat, lon, radius))
            
            return grids
        else:
            # Single center point for smaller cities
            return [(base_lat, base_lon, radius)]
    
    def get_all_search_locations(self, province: str, category: str, radius: int = None) -> List[Dict]:
        """
        Generate all search locations for a province.
        
        Args:
            province: Province name
            category: Business category
            radius: Search radius in meters
            
        Returns:
            List of search location dictionaries
        """
        cities = self.get_province_cities(province)
        all_locations = []
        
        for city in cities:
            grids = self.generate_search_grids(city, radius)
            
            for lat, lon, r in grids:
                all_locations.append({
                    'province': province,
                    'city': city['city'],
                    'category': category,
                    'latitude': lat,
                    'longitude': lon,
                    'radius': r
                })
        
        return all_locations
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in meters
        """
        R = 6371000  # Earth's radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def is_duplicate_location(self, lat: float, lon: float, existing_locations: List[Tuple[float, float]], 
                             threshold: float = 100) -> bool:
        """
        Check if a location is a duplicate of existing locations.
        
        Args:
            lat, lon: Coordinates to check
            existing_locations: List of (lat, lon) tuples
            threshold: Distance threshold in meters
            
        Returns:
            True if location is within threshold of any existing location
        """
        for existing_lat, existing_lon in existing_locations:
            distance = self.calculate_distance(lat, lon, existing_lat, existing_lon)
            if distance < threshold:
                return True
        return False
