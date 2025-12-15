import pygame
import random
import sys
import math
import json
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Get display info for fullscreen
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
FPS = 60
FULLSCREEN = True  # Set to False for windowed mode

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
DARKER_GRAY = (45, 45, 45)
ASPHALT = (52, 52, 52)
LIGHT_ASPHALT = (68, 68, 68)
GREEN = (34, 139, 34)
DARK_GREEN = (20, 100, 20)
YELLOW = (255, 223, 0)
RED = (220, 20, 20)
DARK_RED = (150, 10, 10)
BRIGHT_RED = (255, 50, 50)
BLUE = (30, 144, 255)
LIGHT_BLUE = (100, 180, 255)
DARK_BLUE = (20, 80, 150)
SILVER = (192, 192, 192)
DARK_SILVER = (140, 140, 140)
ORANGE = (255, 140, 0)
SHADOW = (0, 0, 0, 80)

# Biome definitions
BIOMES = {
    'normal': {
        'grass': (34, 139, 34),
        'grass_dark': (20, 100, 20),
        'grass_stripe': (30, 130, 30),
        'road': (52, 52, 52),
        'road_dark': (40, 40, 40),
        'lane_line': (255, 223, 0),
        'edge_line': (255, 255, 255),
        'tree_trunk': (101, 67, 33),
        'tree_leaves': (34, 139, 34),
        'tree_dark': (25, 100, 25),
        'sky_top': (18, 20, 28),
        'sky_bottom': (30, 35, 46)
    },
    'lava': {
        'grass': (60, 20, 10),             # Dark volcanic rock
        'grass_dark': (40, 15, 8),         # Darker rock
        'grass_stripe': (80, 30, 15),      # Reddish rock stripe
        'road': (35, 25, 25),              # Dark ashy road
        'road_dark': (25, 18, 18),
        'lane_line': (255, 120, 40),       # Orange-red lines
        'edge_line': (255, 80, 30),        # Bright orange edges
        'tree_trunk': (50, 30, 20),        # Charred trunk
        'tree_leaves': (180, 60, 20),      # Ember orange
        'tree_dark': (140, 40, 15),        # Dark ember
        'sky_top': (30, 10, 5),            # Dark volcanic sky
        'sky_bottom': (80, 25, 10)         # Reddish glow
    },
    'cherry_blossom': {
        'grass': (255, 200, 210),          # Light pink background
        'grass_dark': (240, 180, 195),     # Darker pink
        'grass_stripe': (255, 210, 220),   # Lighter pink stripe
        'road': (55, 55, 60),              # Slightly blue-gray road
        'road_dark': (42, 42, 48),
        'lane_line': (255, 200, 220),      # Soft pink lines
        'edge_line': (255, 230, 240),      # Light pink edges
        'tree_trunk': (90, 60, 50),        # Brown trunk
        'tree_leaves': (255, 182, 193),    # Light pink blossoms
        'tree_dark': (255, 150, 170),      # Darker pink
        'sky_top': (40, 45, 60),           # Soft evening sky
        'sky_bottom': (70, 80, 100)        # Lighter blue-purple
    },
    'autumn': {
        'grass': (139, 119, 42),           # Golden brown grass
        'grass_dark': (120, 100, 35),      # Darker brown
        'grass_stripe': (150, 130, 50),    # Light golden
        'road': (60, 55, 50),              # Brownish road
        'road_dark': (45, 40, 35),
        'lane_line': (255, 200, 80),       # Warm yellow lines
        'edge_line': (255, 240, 200),      # Cream edges
        'tree_trunk': (90, 60, 30),        # Rich brown trunk
        'tree_leaves': (210, 105, 30),     # Orange leaves
        'tree_dark': (180, 80, 20),        # Dark orange
        'sky_top': (50, 40, 35),           # Warm dark sky
        'sky_bottom': (90, 60, 45)         # Warm brown sky
    },
    'underwater': {
        'grass': (20, 80, 120),            # Deep blue seabed
        'grass_dark': (15, 60, 100),       # Darker blue
        'grass_stripe': (25, 90, 130),     # Light blue stripe
        'road': (30, 70, 100),             # Deep blue road
        'road_dark': (25, 55, 80),
        'lane_line': (100, 180, 200),      # Light cyan lines
        'edge_line': (80, 150, 180),       # Teal edges
        'tree_trunk': (60, 90, 70),        # Seaweed stem
        'tree_leaves': (30, 140, 100),     # Seaweed green
        'tree_dark': (25, 110, 80),
        'sky_top': (10, 40, 80),           # Deep ocean
        'sky_bottom': (20, 70, 110)        # Lighter ocean
    },
    'winter': {
        'grass': (230, 240, 250),
        'grass_dark': (200, 215, 230),
        'grass_stripe': (210, 225, 240),
        'road': (65, 75, 90),
        'road_dark': (50, 60, 75),
        'lane_line': (180, 200, 230),
        'edge_line': (255, 255, 255),
        'tree_trunk': (80, 60, 45),
        'tree_leaves': (220, 235, 245),
        'tree_dark': (190, 210, 225),
        'sky_top': (40, 50, 70),
        'sky_bottom': (70, 85, 110)
    },
}

# Pre-created fonts (optimization - create once, use everywhere)
FONTS = {
    16: pygame.font.Font(None, 16),
    18: pygame.font.Font(None, 18),
    20: pygame.font.Font(None, 20),
    21: pygame.font.Font(None, 21),
    22: pygame.font.Font(None, 22),
    24: pygame.font.Font(None, 24),
    25: pygame.font.Font(None, 25),
    28: pygame.font.Font(None, 28),
    32: pygame.font.Font(None, 32),
    36: pygame.font.Font(None, 36),
    40: pygame.font.Font(None, 40),
    42: pygame.font.Font(None, 42),
    48: pygame.font.Font(None, 48),
    72: pygame.font.Font(None, 72),
    80: pygame.font.Font(None, 80),
}

# Road dimensions
ROAD_WIDTH = 400
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2
LANE_WIDTH = 10
LANE_HEIGHT = 40
LANE_GAP = 40

# Incident types
INCIDENT_TYPES = {
    'roadwork': {'name': 'Road Work', 'color': ORANGE},
    'accident': {'name': 'Accident', 'color': RED},
    'closure': {'name': 'Road Closure', 'color': RED},
    'congestion': {'name': 'Congestion', 'color': YELLOW}
}

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
NAME_INPUT = 3
LEADERBOARD_VIEW = 4
HOW_TO_PLAY = 5
SETTINGS = 6

# Leaderboard file
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Load leaderboard from file"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(leaderboard):
    """Save leaderboard to file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f)
    except:
        pass

def is_high_score(score, leaderboard):
    """Check if score qualifies for top 5"""
    # Minimum score of 10 to qualify
    if score < 10:
        return False
    if len(leaderboard) < 5:
        return True
    return score > leaderboard[-1]['score']

def add_to_leaderboard(name, score, leaderboard):
    """Add score to leaderboard and keep top 5, updating duplicates with highest score"""
    # Check if name already exists
    existing_entry = None
    for entry in leaderboard:
        if entry['name'] == name:
            existing_entry = entry
            break
    
    if existing_entry:
        # Update only if new score is higher
        if score > existing_entry['score']:
            existing_entry['score'] = score
    else:
        # Add new entry
        leaderboard.append({'name': name, 'score': score})
    
    # Sort by score and keep top 5
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard[:5]  # Keep only top 5

class Car:
    def __init__(self, x, y):
        self.width = 50
        self.height = 85
        self.x = x
        self.y = y
        self.speed = 5
        
    def draw(self, screen, biome='normal'):
        # Shadow
        shadow_surface = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, SHADOW, (0, 0, self.width + 6, self.height + 6))
        screen.blit(shadow_surface, (self.x - 3, self.y + 3))
        
        # Wheels
        pygame.draw.ellipse(screen, BLACK, (self.x - 3, self.y + 20, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 7, self.y + 20, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x - 3, self.y + 50, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 7, self.y + 50, 10, 18))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 1, self.y + 23, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + self.width - 5, self.y + 23, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 1, self.y + 53, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + self.width - 5, self.y + 53, 6, 12))
        
        # Car body - main
        pygame.draw.rect(screen, RED, (self.x + 2, self.y + 15, self.width - 4, self.height - 20), border_radius=8)
        pygame.draw.rect(screen, DARK_RED, (self.x + 3, self.y + 16, self.width - 6, self.height - 22), border_radius=7)
        
        # Hood section (front)
        pygame.draw.rect(screen, BRIGHT_RED, (self.x + 4, self.y + 15, self.width - 8, 20), border_top_left_radius=8, border_top_right_radius=8)
        
        # Windshield
        pygame.draw.polygon(screen, LIGHT_BLUE, [
            (self.x + 8, self.y + 30),
            (self.x + self.width - 8, self.y + 30),
            (self.x + self.width - 10, self.y + 48),
            (self.x + 10, self.y + 48)
        ])
        pygame.draw.polygon(screen, DARK_BLUE, [
            (self.x + 10, self.y + 32),
            (self.x + self.width - 10, self.y + 32),
            (self.x + self.width - 11, self.y + 46),
            (self.x + 11, self.y + 46)
        ])
        
        # Headlights
        pygame.draw.ellipse(screen, YELLOW, (self.x + 6, self.y + 18, 10, 8))
        pygame.draw.ellipse(screen, YELLOW, (self.x + self.width - 16, self.y + 18, 10, 8))
        pygame.draw.ellipse(screen, WHITE, (self.x + 8, self.y + 20, 6, 4))
        pygame.draw.ellipse(screen, WHITE, (self.x + self.width - 14, self.y + 20, 6, 4))
        
        # Side mirrors
        pygame.draw.ellipse(screen, DARK_RED, (self.x - 2, self.y + 38, 6, 8))
        pygame.draw.ellipse(screen, DARK_RED, (self.x + self.width - 4, self.y + 38, 6, 8))
        
        # Rear window
        pygame.draw.polygon(screen, LIGHT_BLUE, [
            (self.x + 12, self.y + 55),
            (self.x + self.width - 12, self.y + 55),
            (self.x + self.width - 10, self.y + 70),
            (self.x + 10, self.y + 70)
        ])
        
        # Back details
        pygame.draw.rect(screen, DARK_RED, (self.x + 8, self.y + self.height - 18, self.width - 16, 12), border_radius=3)
        
        # Taillights
        pygame.draw.ellipse(screen, RED, (self.x + 10, self.y + self.height - 15, 8, 6))
        pygame.draw.ellipse(screen, RED, (self.x + self.width - 18, self.y + self.height - 15, 8, 6))
        pygame.draw.ellipse(screen, BRIGHT_RED, (self.x + 11, self.y + self.height - 14, 6, 4))
        pygame.draw.ellipse(screen, BRIGHT_RED, (self.x + self.width - 17, self.y + self.height - 14, 6, 4))
        
    def move(self, dx):
        self.x += dx
        # Keep car on the road
        if self.x < ROAD_X + 10:
            self.x = ROAD_X + 10
        elif self.x > ROAD_X + ROAD_WIDTH - self.width - 10:
            self.x = ROAD_X + ROAD_WIDTH - self.width - 10
            
    def get_rect(self):
        return pygame.Rect(self.x + 2, self.y + 15, self.width - 4, self.height - 20)

class ObstacleCar:
    def __init__(self, x, y, speed, vehicle_type='car'):
        self.vehicle_type = vehicle_type
        self.y = y
        self.speed = speed
        
        # Set dimensions based on vehicle type
        if vehicle_type == 'truck':
            self.width = 60
            self.height = 130
            self.x = x - 5  # Slightly adjust for width difference
        elif vehicle_type == 'bike':
            self.width = 25
            self.height = 60
            self.x = x + 12  # Center bikes in lane
        else:  # car
            self.width = 50
            self.height = 85
            self.x = x
        
        colors = [
            (BLUE, DARK_BLUE, LIGHT_BLUE),
            (SILVER, DARK_SILVER, WHITE),
            (ORANGE, (200, 100, 0), (255, 180, 50)),
            ((100, 50, 150), (60, 30, 100), (140, 90, 180)),
            ((50, 150, 50), (30, 100, 30), (80, 180, 80))
        ]
        self.color, self.dark_color, self.light_color = random.choice(colors)
        
        # Bike-specific colors (rider gear)
        if vehicle_type == 'bike':
            bike_colors = [
                {'body': (220, 20, 20), 'body_dark': (150, 10, 10), 'accent': (255, 200, 0)},      # Red sport bike
                {'body': (30, 30, 30), 'body_dark': (15, 15, 15), 'accent': (255, 140, 0)},        # Black bike
                {'body': (0, 100, 200), 'body_dark': (0, 60, 140), 'accent': (255, 255, 255)},     # Blue bike
                {'body': (50, 180, 50), 'body_dark': (30, 120, 30), 'accent': (0, 0, 0)},          # Green Kawasaki style
                {'body': (255, 255, 255), 'body_dark': (200, 200, 200), 'accent': (220, 20, 20)},  # White bike
            ]
            bike_scheme = random.choice(bike_colors)
            self.bike_color = bike_scheme['body']
            self.bike_dark = bike_scheme['body_dark']
            self.bike_accent = bike_scheme['accent']
            # Rider colors
            helmet_colors = [(220, 20, 20), (30, 30, 30), (255, 255, 255), (0, 100, 200), (255, 200, 0)]
            jacket_colors = [(30, 30, 30), (50, 50, 50), (20, 20, 60), (60, 20, 20)]
            self.helmet_color = random.choice(helmet_colors)
            self.jacket_color = random.choice(jacket_colors)
        
    def draw(self, screen, biome='normal'):
        if self.vehicle_type == 'truck':
            self.draw_truck(screen, biome)
        elif self.vehicle_type == 'bike':
            self.draw_bike(screen, biome)
        else:
            self.draw_car(screen, biome)
    
    def draw_car(self, screen, biome='normal'):
        # Shadow
        shadow_surface = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, SHADOW, (0, 0, self.width + 6, self.height + 6))
        screen.blit(shadow_surface, (self.x - 3, self.y + 3))
        
        # Wheels
        pygame.draw.ellipse(screen, BLACK, (self.x - 3, self.y + 20, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 7, self.y + 20, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x - 3, self.y + 50, 10, 18))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 7, self.y + 50, 10, 18))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 1, self.y + 23, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + self.width - 5, self.y + 23, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 1, self.y + 53, 6, 12))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + self.width - 5, self.y + 53, 6, 12))
        
        # Car body
        pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 15, self.width - 4, self.height - 20), border_radius=8)
        pygame.draw.rect(screen, self.dark_color, (self.x + 3, self.y + 16, self.width - 6, self.height - 22), border_radius=7)
        
        # Rear section (this car faces away from player)
        pygame.draw.rect(screen, self.light_color, (self.x + 4, self.y + self.height - 23, self.width - 8, 15), border_bottom_left_radius=6, border_bottom_right_radius=6)
        
        # Rear window
        pygame.draw.polygon(screen, LIGHT_BLUE, [
            (self.x + 10, self.y + self.height - 40),
            (self.x + self.width - 10, self.y + self.height - 40),
            (self.x + self.width - 8, self.y + self.height - 25),
            (self.x + 8, self.y + self.height - 25)
        ])
        pygame.draw.polygon(screen, DARK_BLUE, [
            (self.x + 11, self.y + self.height - 38),
            (self.x + self.width - 11, self.y + self.height - 38),
            (self.x + self.width - 9, self.y + self.height - 27),
            (self.x + 9, self.y + self.height - 27)
        ])
        
        # Front windshield
        pygame.draw.polygon(screen, LIGHT_BLUE, [
            (self.x + 12, self.y + 20),
            (self.x + self.width - 12, self.y + 20),
            (self.x + self.width - 10, self.y + 35),
            (self.x + 10, self.y + 35)
        ])
        
        # Side mirrors
        pygame.draw.ellipse(screen, self.dark_color, (self.x - 2, self.y + 38, 6, 8))
        pygame.draw.ellipse(screen, self.dark_color, (self.x + self.width - 4, self.y + 38, 6, 8))
        
        # Taillights (brake lights)
        pygame.draw.ellipse(screen, RED, (self.x + 8, self.y + self.height - 18, 10, 7))
        pygame.draw.ellipse(screen, RED, (self.x + self.width - 18, self.y + self.height - 18, 10, 7))
        pygame.draw.ellipse(screen, BRIGHT_RED, (self.x + 9, self.y + self.height - 17, 8, 5))
        pygame.draw.ellipse(screen, BRIGHT_RED, (self.x + self.width - 17, self.y + self.height - 17, 8, 5))
    
    def draw_truck(self, screen, biome='normal'):
        # Shadow
        shadow_surface = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, SHADOW, (0, 0, self.width + 8, self.height + 8))
        screen.blit(shadow_surface, (self.x - 4, self.y + 4))
        
        # Wheels (trucks have more wheels)
        wheel_positions = [(self.y + 25, 10, 20), (self.y + 55, 10, 20), 
                          (self.y + 85, 10, 20), (self.y + 105, 10, 20)]
        for wheel_y, wheel_w, wheel_h in wheel_positions:
            pygame.draw.ellipse(screen, BLACK, (self.x - 4, wheel_y, wheel_w, wheel_h))
            pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 6, wheel_y, wheel_w, wheel_h))
            pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 2, wheel_y + 3, 6, 14))
            pygame.draw.ellipse(screen, DARK_GRAY, (self.x + self.width - 4, wheel_y + 3, 6, 14))
        
        # Cargo section (long back)
        pygame.draw.rect(screen, self.color, (self.x, self.y + 40, self.width, 70), border_radius=5)
        pygame.draw.rect(screen, self.dark_color, (self.x + 2, self.y + 42, self.width - 4, 66), border_radius=4)
        
        # Cargo door lines
        for i in range(3):
            pygame.draw.line(screen, self.light_color, 
                           (self.x + 5, self.y + 55 + i * 15),
                           (self.x + self.width - 5, self.y + 55 + i * 15), 2)
        
        # Cab section (front driver area)
        pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 15, self.width - 4, 30), border_radius=6)
        pygame.draw.rect(screen, self.dark_color, (self.x + 3, self.y + 16, self.width - 6, 28), border_radius=5)
        
        # Cab windshield
        pygame.draw.polygon(screen, LIGHT_BLUE, [
            (self.x + 10, self.y + 20),
            (self.x + self.width - 10, self.y + 20),
            (self.x + self.width - 8, self.y + 35),
            (self.x + 8, self.y + 35)
        ])
        
        # Truck grill/front
        pygame.draw.rect(screen, self.dark_color, (self.x + 8, self.y + 110, self.width - 16, 12), border_radius=2)
        
        # Taillights
        pygame.draw.rect(screen, RED, (self.x + 8, self.y + self.height - 10, 12, 6), border_radius=2)
        pygame.draw.rect(screen, RED, (self.x + self.width - 20, self.y + self.height - 10, 12, 6), border_radius=2)
    
    def draw_bike(self, screen, biome='normal'):
        cx = self.x + self.width // 2  # Center x
        
        # Shadow
        shadow_surface = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (0, 0, self.width + 8, self.height + 8))
        screen.blit(shadow_surface, (self.x - 4, self.y + 4))
        
        # === REAR WHEEL ===
        wheel_rear_y = self.y + self.height - 12
        # Tire
        pygame.draw.circle(screen, (20, 20, 20), (cx, wheel_rear_y), 9)
        # Rim
        pygame.draw.circle(screen, (80, 80, 80), (cx, wheel_rear_y), 6)
        # Hub
        pygame.draw.circle(screen, (50, 50, 50), (cx, wheel_rear_y), 3)
        # Spokes effect
        pygame.draw.circle(screen, (100, 100, 100), (cx, wheel_rear_y), 5, 1)
        
        # === FRONT WHEEL ===
        wheel_front_y = self.y + 10
        # Tire
        pygame.draw.circle(screen, (20, 20, 20), (cx, wheel_front_y), 9)
        # Rim
        pygame.draw.circle(screen, (80, 80, 80), (cx, wheel_front_y), 6)
        # Hub
        pygame.draw.circle(screen, (50, 50, 50), (cx, wheel_front_y), 3)
        # Spokes effect
        pygame.draw.circle(screen, (100, 100, 100), (cx, wheel_front_y), 5, 1)
        
        # === MOTORCYCLE FRAME/BODY ===
        # Main fuel tank and body (sporty shape)
        body_top = self.y + 22
        # Tank - main body piece
        tank_points = [
            (cx - 8, body_top),
            (cx + 8, body_top),
            (cx + 10, body_top + 8),
            (cx + 6, body_top + 16),
            (cx - 6, body_top + 16),
            (cx - 10, body_top + 8),
        ]
        pygame.draw.polygon(screen, self.bike_color, tank_points)
        pygame.draw.polygon(screen, self.bike_dark, tank_points, 1)
        
        # Tank highlight
        pygame.draw.ellipse(screen, self.bike_accent, (cx - 4, body_top + 2, 8, 4))
        
        # Rear fairing / seat area
        seat_points = [
            (cx - 6, body_top + 14),
            (cx + 6, body_top + 14),
            (cx + 5, body_top + 28),
            (cx - 5, body_top + 28),
        ]
        pygame.draw.polygon(screen, self.bike_dark, seat_points)
        
        # Exhaust pipe (right side)
        pygame.draw.line(screen, (120, 120, 120), (cx + 6, body_top + 20), (cx + 8, body_top + 32), 3)
        pygame.draw.circle(screen, (80, 80, 80), (cx + 8, body_top + 32), 3)
        
        # Front fork (connects to front wheel)
        pygame.draw.line(screen, (60, 60, 60), (cx - 2, self.y + 18), (cx - 2, body_top), 3)
        pygame.draw.line(screen, (60, 60, 60), (cx + 2, self.y + 18), (cx + 2, body_top), 3)
        
        # === HEADLIGHT ===
        pygame.draw.ellipse(screen, (255, 255, 200), (cx - 4, self.y + 2, 8, 5))
        pygame.draw.ellipse(screen, (255, 255, 255), (cx - 3, self.y + 3, 6, 3))
        
        # === HANDLEBARS ===
        pygame.draw.line(screen, (40, 40, 40), (cx - 10, self.y + 20), (cx + 10, self.y + 20), 3)
        # Mirrors
        pygame.draw.circle(screen, (60, 60, 60), (cx - 11, self.y + 19), 2)
        pygame.draw.circle(screen, (60, 60, 60), (cx + 11, self.y + 19), 2)
        # Grips
        pygame.draw.rect(screen, (30, 30, 30), (cx - 12, self.y + 18, 3, 5))
        pygame.draw.rect(screen, (30, 30, 30), (cx + 9, self.y + 18, 3, 5))
        
        # === RIDER ===
        rider_y = body_top - 2
        
        # Rider's arms (holding handlebars) - draw first so body overlaps
        pygame.draw.line(screen, self.jacket_color, (cx - 6, rider_y + 8), (cx - 10, self.y + 21), 3)
        pygame.draw.line(screen, self.jacket_color, (cx + 6, rider_y + 8), (cx + 10, self.y + 21), 3)
        # Gloves
        pygame.draw.circle(screen, (20, 20, 20), (cx - 10, self.y + 21), 2)
        pygame.draw.circle(screen, (20, 20, 20), (cx + 10, self.y + 21), 2)
        
        # Rider's body/jacket (leaning forward sporty pose)
        body_points = [
            (cx - 6, rider_y + 4),
            (cx + 6, rider_y + 4),
            (cx + 7, rider_y + 16),
            (cx - 7, rider_y + 16),
        ]
        pygame.draw.polygon(screen, self.jacket_color, body_points)
        # Jacket stripe
        pygame.draw.line(screen, self.bike_accent, (cx, rider_y + 5), (cx, rider_y + 14), 2)
        
        # Helmet (aerodynamic shape)
        helmet_points = [
            (cx, rider_y - 6),       # Top
            (cx + 7, rider_y),       # Right
            (cx + 6, rider_y + 6),   # Bottom right
            (cx - 6, rider_y + 6),   # Bottom left
            (cx - 7, rider_y),       # Left
        ]
        pygame.draw.polygon(screen, self.helmet_color, helmet_points)
        # Visor
        pygame.draw.arc(screen, (40, 40, 40), (cx - 5, rider_y - 2, 10, 6), 3.14, 0, 2)
        # Helmet shine
        pygame.draw.arc(screen, (255, 255, 255), (cx - 4, rider_y - 4, 6, 4), 0.5, 2.5, 1)
        
        # === TAILLIGHT ===
        pygame.draw.rect(screen, (150, 0, 0), (cx - 4, self.y + self.height - 6, 8, 4), border_radius=1)
        pygame.draw.rect(screen, (255, 50, 50), (cx - 3, self.y + self.height - 5, 6, 2), border_radius=1)
        
    def move(self):
        self.y += self.speed
        
    def get_rect(self):
        # Adjust collision box based on vehicle type
        if self.vehicle_type == 'truck':
            return pygame.Rect(self.x + 2, self.y + 15, self.width - 4, self.height - 20)
        elif self.vehicle_type == 'bike':
            return pygame.Rect(self.x + 4, self.y + 15, self.width - 8, self.height - 20)
        else:  # car
            return pygame.Rect(self.x + 2, self.y + 15, self.width - 4, self.height - 20)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class LaneLine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = LANE_WIDTH
        self.height = LANE_HEIGHT
        
    def draw(self, screen, color=None):
        if color is None:
            color = YELLOW
        # Main line
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=2)
        # Add highlight for 3D effect
        highlight = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
        pygame.draw.rect(screen, highlight, (self.x + 1, self.y + 1, self.width - 2, self.height // 2), border_radius=1)
        # Shadow at bottom
        shadow = (max(color[0] - 40, 0), max(color[1] - 40, 0), max(color[2] - 40, 0))
        pygame.draw.rect(screen, shadow, (self.x + 1, self.y + self.height - 4, self.width - 2, 3))
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, SCREEN_HEIGHT)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.drift = random.uniform(-0.5, 0.5)
        self.alpha = random.randint(150, 255)
        
    def update(self):
        self.y += self.speed
        self.x += self.drift
        
        # Reset if off screen
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
            
    def draw(self, screen):
        snow_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(snow_surface, (255, 255, 255, self.alpha), (self.size, self.size), self.size)
        screen.blit(snow_surface, (int(self.x - self.size), int(self.y - self.size)))

class FallingLeaf:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, SCREEN_HEIGHT)
        self.size = random.randint(4, 8)
        self.speed = random.uniform(1.5, 3.5)
        self.drift_speed = random.uniform(0.02, 0.05)
        self.drift_amount = random.uniform(20, 40)
        self.drift_offset = random.random() * 3.14 * 2
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-3, 3)
        self.alpha = random.randint(180, 255)
        # Autumn leaf colors: orange, red, yellow, brown
        self.color = random.choice([
            (255, 140, 0),    # Orange
            (255, 69, 0),     # Red-orange
            (220, 60, 20),    # Dark red
            (255, 200, 0),    # Yellow
            (200, 120, 50),   # Brown
            (180, 80, 20),    # Dark brown
        ])
        
    def update(self, road_offset_delta=0):
        self.y += self.speed + road_offset_delta * 0.3
        # Swaying motion
        self.x += math.sin(self.y * self.drift_speed + self.drift_offset) * 0.8
        self.rotation += self.rotation_speed
        
        # Reset if off screen
        if self.y > SCREEN_HEIGHT + 20:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)
            self.color = random.choice([
                (255, 140, 0), (255, 69, 0), (220, 60, 20),
                (255, 200, 0), (200, 120, 50), (180, 80, 20),
            ])
        if self.x < -20:
            self.x = SCREEN_WIDTH + 10
        elif self.x > SCREEN_WIDTH + 20:
            self.x = -10
            
    def draw(self, screen):
        # Draw a simple leaf shape
        leaf_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        center = self.size * 1.5
        
        # Draw leaf as an ellipse/oval
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.ellipse(leaf_surface, color_with_alpha, 
                           (center - self.size, center - self.size // 2, 
                            self.size * 2, self.size))
        # Leaf vein/stem
        darker_color = (max(0, self.color[0] - 40), max(0, self.color[1] - 30), max(0, self.color[2] - 20), self.alpha)
        pygame.draw.line(leaf_surface, darker_color, 
                        (center - self.size + 2, center), 
                        (center + self.size - 2, center), 1)
        
        # Rotate the leaf
        rotated = pygame.transform.rotate(leaf_surface, self.rotation)
        new_rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, new_rect)

class FallingPetal:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, SCREEN_HEIGHT)
        self.size = random.randint(3, 6)
        self.speed = random.uniform(1.0, 2.5)
        self.drift_speed = random.uniform(0.015, 0.04)
        self.drift_amount = random.uniform(25, 50)
        self.drift_offset = random.random() * 3.14 * 2
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        self.alpha = random.randint(180, 255)
        # Cherry blossom petal colors: various pinks and white
        self.color = random.choice([
            (255, 183, 197),   # Light pink
            (255, 192, 203),   # Pink
            (255, 160, 180),   # Deeper pink
            (255, 209, 220),   # Pale pink
            (255, 240, 245),   # Almost white pink
            (255, 170, 190),   # Medium pink
        ])
        
    def update(self, road_offset_delta=0):
        self.y += self.speed + road_offset_delta * 0.2
        # Gentle floating motion
        self.x += math.sin(self.y * self.drift_speed + self.drift_offset) * 1.2
        self.rotation += self.rotation_speed
        
        # Reset if off screen
        if self.y > SCREEN_HEIGHT + 20:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)
            self.color = random.choice([
                (255, 183, 197), (255, 192, 203), (255, 160, 180),
                (255, 209, 220), (255, 240, 245), (255, 170, 190),
            ])
        if self.x < -20:
            self.x = SCREEN_WIDTH + 10
        elif self.x > SCREEN_WIDTH + 20:
            self.x = -10
            
    def draw(self, screen):
        # Draw a small petal shape (oval)
        petal_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        center = self.size * 1.5
        
        # Draw petal as a small oval
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.ellipse(petal_surface, color_with_alpha, 
                           (center - self.size, center - self.size // 2, 
                            self.size * 2, self.size))
        # Subtle center detail
        lighter_color = (min(255, self.color[0] + 20), min(255, self.color[1] + 20), min(255, self.color[2] + 20), self.alpha // 2)
        pygame.draw.ellipse(petal_surface, lighter_color, 
                           (center - self.size // 2, center - self.size // 4, 
                            self.size, self.size // 2))
        
        # Rotate the petal
        rotated = pygame.transform.rotate(petal_surface, self.rotation)
        new_rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, new_rect)

class Bubble:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 300)
        self.size = random.randint(8, 20)  # Larger bubbles
        self.speed = random.uniform(1.0, 2.5)  # Slower rise
        self.drift_speed = random.uniform(0.015, 0.035)
        self.drift_offset = random.random() * 3.14 * 2
        self.alpha = random.randint(120, 200)
        self.wobble_phase = random.random() * 3.14 * 2
        self.pulse_speed = random.uniform(0.02, 0.04)  # For size pulsing
        
    def update(self, road_offset_delta=0):
        self.y -= self.speed  # Bubbles rise up
        # Wobble motion - more gentle
        self.x += math.sin(self.y * self.drift_speed + self.drift_offset) * 1.2
        self.wobble_phase += 0.05  # For pulsing effect
        
        # Reset if off screen (top)
        if self.y < -30:
            self.y = random.randint(SCREEN_HEIGHT + 50, SCREEN_HEIGHT + 200)
            self.x = random.randint(0, SCREEN_WIDTH)
            self.size = random.randint(8, 20)
        if self.x < -30:
            self.x = SCREEN_WIDTH + 20
        elif self.x > SCREEN_WIDTH + 30:
            self.x = -20
            
    def draw(self, screen):
        # Pulsing size effect
        pulse = math.sin(self.wobble_phase) * 0.1
        current_size = int(self.size * (1 + pulse))
        
        bubble_surface = pygame.Surface((current_size * 4, current_size * 4), pygame.SRCALPHA)
        center = current_size * 2
        
        # Outer glow
        glow_alpha = int(self.alpha * 0.3)
        pygame.draw.circle(bubble_surface, (100, 200, 255, glow_alpha), 
                          (int(center), int(center)), int(current_size * 1.3))
        
        # Main bubble body (gradient effect with multiple circles)
        pygame.draw.circle(bubble_surface, (140, 210, 250, self.alpha), 
                          (int(center), int(center)), current_size)
        pygame.draw.circle(bubble_surface, (160, 220, 255, int(self.alpha * 0.9)), 
                          (int(center), int(center)), int(current_size * 0.85))
        
        # Inner lighter area
        pygame.draw.circle(bubble_surface, (180, 230, 255, int(self.alpha * 0.7)), 
                          (int(center + current_size * 0.1), int(center + current_size * 0.1)), 
                          int(current_size * 0.6))
        
        # Main highlight (top-left shine)
        pygame.draw.circle(bubble_surface, (220, 245, 255, int(self.alpha * 0.9)), 
                          (int(center - current_size * 0.35), int(center - current_size * 0.35)), 
                          int(current_size * 0.35))
        # Smaller bright highlight
        pygame.draw.circle(bubble_surface, (255, 255, 255, int(self.alpha * 0.95)), 
                          (int(center - current_size * 0.4), int(center - current_size * 0.4)), 
                          int(current_size * 0.15))
        
        # Secondary small highlight (bottom right)
        pygame.draw.circle(bubble_surface, (200, 240, 255, int(self.alpha * 0.5)), 
                          (int(center + current_size * 0.3), int(center + current_size * 0.4)), 
                          int(current_size * 0.12))
        
        # Outer ring/edge
        pygame.draw.circle(bubble_surface, (80, 160, 200, int(self.alpha * 0.6)), 
                          (int(center), int(center)), current_size, 2)
        
        screen.blit(bubble_surface, (int(self.x - center), int(self.y - center)))

class FallingEmber:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-100, SCREEN_HEIGHT)
        self.size = random.randint(2, 6)
        self.speed = random.uniform(2.0, 4.5)
        self.drift_speed = random.uniform(0.03, 0.06)
        self.drift_offset = random.random() * 3.14 * 2
        self.alpha = random.randint(180, 255)
        self.flicker_phase = random.random() * 3.14 * 2
        self.flicker_speed = random.uniform(0.1, 0.2)
        # Ember colors: orange, red, yellow
        self.base_color = random.choice([
            (255, 100, 20),    # Orange
            (255, 60, 10),     # Red-orange
            (255, 150, 30),    # Yellow-orange
            (255, 80, 15),     # Deep orange
            (255, 200, 50),    # Bright yellow
        ])
        
    def update(self, road_offset_delta=0):
        self.y += self.speed + road_offset_delta * 0.5  # Embers fall down
        # Drift motion
        self.x += math.sin(self.y * self.drift_speed + self.drift_offset) * 1.5
        self.flicker_phase += self.flicker_speed
        
        # Reset if off screen
        if self.y > SCREEN_HEIGHT + 30:
            self.y = random.randint(-80, -20)
            self.x = random.randint(0, SCREEN_WIDTH)
            self.size = random.randint(2, 6)
            self.base_color = random.choice([
                (255, 100, 20), (255, 60, 10), (255, 150, 30),
                (255, 80, 15), (255, 200, 50),
            ])
        if self.x < -20:
            self.x = SCREEN_WIDTH + 10
        elif self.x > SCREEN_WIDTH + 20:
            self.x = -10
            
    def draw(self, screen):
        # Flickering brightness
        flicker = 0.7 + math.sin(self.flicker_phase) * 0.3
        current_alpha = int(self.alpha * flicker)
        
        ember_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        center = self.size * 2
        
        # Outer glow
        glow_color = (255, 80, 20, int(current_alpha * 0.3))
        pygame.draw.circle(ember_surface, glow_color, 
                          (int(center), int(center)), int(self.size * 1.8))
        
        # Middle glow
        mid_glow = (255, 120, 40, int(current_alpha * 0.5))
        pygame.draw.circle(ember_surface, mid_glow, 
                          (int(center), int(center)), int(self.size * 1.3))
        
        # Core ember
        core_color = (*self.base_color, current_alpha)
        pygame.draw.circle(ember_surface, core_color, 
                          (int(center), int(center)), self.size)
        
        # Bright center
        bright_center = (255, 220, 150, int(current_alpha * 0.9))
        pygame.draw.circle(ember_surface, bright_center, 
                          (int(center), int(center)), int(self.size * 0.5))
        
        # White hot core (small)
        if self.size > 3:
            hot_core = (255, 255, 200, int(current_alpha * 0.8))
            pygame.draw.circle(ember_surface, hot_core, 
                              (int(center), int(center)), int(self.size * 0.25))
        
        screen.blit(ember_surface, (int(self.x - center), int(self.y - center)))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.collected = False
        self.animation_frame = 0
        self.bob_offset = random.random() * 3.14 * 2  # Random start phase for bobbing
        
    def draw(self, screen):
        if self.collected:
            return
            
        # Bobbing animation
        bob = math.sin(pygame.time.get_ticks() / 200 + self.bob_offset) * 3
        draw_y = self.y + bob
        
        # Shine/sparkle effect
        sparkle = abs(math.sin(pygame.time.get_ticks() / 150 + self.bob_offset))
        
        # Coin shadow
        shadow_surface = pygame.Surface((self.radius * 2 + 4, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (0, 0, self.radius * 2 + 4, 8))
        screen.blit(shadow_surface, (self.x - self.radius - 2, draw_y + self.radius + 2))
        
        # Outer gold ring
        pygame.draw.circle(screen, (218, 165, 32), (self.x, int(draw_y)), self.radius)
        
        # Inner gold (brighter)
        pygame.draw.circle(screen, (255, 215, 0), (self.x, int(draw_y)), self.radius - 2)
        
        # Highlight/shine
        highlight_color = (255, 255, int(150 + sparkle * 105))
        pygame.draw.circle(screen, highlight_color, (self.x - 3, int(draw_y) - 3), 4)
        
        # Dollar sign or star
        coin_font = FONTS[18]
        symbol = coin_font.render("$", True, (180, 130, 0))
        symbol_rect = symbol.get_rect(center=(self.x, int(draw_y)))
        screen.blit(symbol, symbol_rect)
        
    def move(self, speed):
        self.y += speed
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 20

class Incident:
    def __init__(self, incident_type, y_position, scene_image=None):
        self.type = incident_type
        self.y = y_position
        self.x = ROAD_X + ROAD_WIDTH // 2
        self.active = True
        self.scene_image = scene_image  # Store the randomly selected scene image
        
    def draw(self, screen):
        if self.type == 'roadwork':
            self.draw_roadwork(screen)
        elif self.type == 'accident':
            self.draw_accident(screen)
        elif self.type == 'closure':
            self.draw_closure(screen)
        elif self.type == 'congestion':
            self.draw_congestion(screen)
    
    def draw_accident(self, screen):
        # Two cars crashing into each other at angle
        
        # Car 1 (Red car - angled from left)
        car1_x = self.x - 50
        car1_y = self.y + 20
        # Body
        pygame.draw.rect(screen, RED, (car1_x, car1_y, 45, 70), border_radius=6)
        pygame.draw.rect(screen, DARK_RED, (car1_x + 2, car1_y + 2, 41, 66), border_radius=5)
        # Window
        pygame.draw.rect(screen, LIGHT_BLUE, (car1_x + 8, car1_y + 15, 30, 20), border_radius=3)
        # Wheels
        pygame.draw.ellipse(screen, BLACK, (car1_x - 4, car1_y + 15, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car1_x + 39, car1_y + 15, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car1_x - 4, car1_y + 45, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car1_x + 39, car1_y + 45, 10, 16))
        # Damage/crumple on right side
        pygame.draw.polygon(screen, BLACK, [
            (car1_x + 45, car1_y + 25),
            (car1_x + 50, car1_y + 30),
            (car1_x + 48, car1_y + 40),
            (car1_x + 45, car1_y + 45)
        ])
        
        # Car 2 (Blue car - angled from right)
        car2_x = self.x + 5
        car2_y = self.y + 20
        # Body
        pygame.draw.rect(screen, BLUE, (car2_x, car2_y, 45, 70), border_radius=6)
        pygame.draw.rect(screen, DARK_BLUE, (car2_x + 2, car2_y + 2, 41, 66), border_radius=5)
        # Window
        pygame.draw.rect(screen, LIGHT_BLUE, (car2_x + 8, car2_y + 15, 30, 20), border_radius=3)
        # Wheels
        pygame.draw.ellipse(screen, BLACK, (car2_x - 4, car2_y + 15, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car2_x + 39, car2_y + 15, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car2_x - 4, car2_y + 45, 10, 16))
        pygame.draw.ellipse(screen, BLACK, (car2_x + 39, car2_y + 45, 10, 16))
        # Damage/crumple on left side
        pygame.draw.polygon(screen, BLACK, [
            (car2_x, car2_y + 25),
            (car2_x - 5, car2_y + 30),
            (car2_x - 3, car2_y + 40),
            (car2_x, car2_y + 45)
        ])
        
        # Impact/crash effect between cars
        impact_x = self.x - 3
        impact_y = self.y + 50
        # Yellow impact starburst
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            end_x = impact_x + math.cos(rad) * 15
            end_y = impact_y + math.sin(rad) * 15
            pygame.draw.line(screen, YELLOW, (impact_x, impact_y), (end_x, end_y), 3)
        # Orange inner burst
        for angle in range(22, 360, 45):
            rad = math.radians(angle)
            end_x = impact_x + math.cos(rad) * 10
            end_y = impact_y + math.sin(rad) * 10
            pygame.draw.line(screen, ORANGE, (impact_x, impact_y), (end_x, end_y), 2)
        
        # Debris scattered around
        debris_positions = [
            (self.x - 30, self.y + 70), (self.x - 15, self.y + 75),
            (self.x + 10, self.y + 72), (self.x + 25, self.y + 78),
            (self.x - 5, self.y + 80), (self.x + 15, self.y + 68)
        ]
        for debris_x, debris_y in debris_positions:
            pygame.draw.circle(screen, DARK_GRAY, (debris_x, debris_y), 3)
            pygame.draw.circle(screen, GRAY, (debris_x - 1, debris_y - 1), 2)
        
        # Tire marks/skid marks
        pygame.draw.line(screen, BLACK, (car1_x + 5, car1_y - 20), (car1_x + 10, car1_y), 3)
        pygame.draw.line(screen, BLACK, (car2_x + 35, car2_y - 20), (car2_x + 30, car2_y), 3)
        
        # Warning sign
        self.draw_warning_sign(screen, self.y - 40)
    
    def draw_closure(self, screen):
        # Draw barrier/cones
        for i in range(5):
            x_pos = self.x - 100 + i * 50
            # Cone base
            pygame.draw.polygon(screen, ORANGE, [
                (x_pos, self.y + 50),
                (x_pos - 15, self.y + 70),
                (x_pos + 15, self.y + 70)
            ])
            # Cone stripes
            pygame.draw.polygon(screen, WHITE, [
                (x_pos - 8, self.y + 55),
                (x_pos + 8, self.y + 55),
                (x_pos + 6, self.y + 60),
                (x_pos - 6, self.y + 60)
            ])
        
        # Barrier
        pygame.draw.rect(screen, RED, (self.x - 120, self.y, 240, 15), border_radius=3)
        pygame.draw.rect(screen, WHITE, (self.x - 120, self.y + 5, 40, 5))
        pygame.draw.rect(screen, WHITE, (self.x - 40, self.y + 5, 40, 5))
        pygame.draw.rect(screen, WHITE, (self.x + 40, self.y + 5, 40, 5))
        
        # Warning sign
        self.draw_warning_sign(screen, self.y - 40)
    
    def draw_roadwork(self, screen):
        # Draw road work scene with workers and equipment
        # Construction cones
        for i in range(4):
            x_pos = self.x - 80 + i * 50
            # Cone
            pygame.draw.polygon(screen, ORANGE, [
                (x_pos, self.y + 40),
                (x_pos - 12, self.y + 60),
                (x_pos + 12, self.y + 60)
            ])
            # White stripe on cone
            pygame.draw.polygon(screen, WHITE, [
                (x_pos - 8, self.y + 48),
                (x_pos + 8, self.y + 48),
                (x_pos + 6, self.y + 53),
                (x_pos - 6, self.y + 53)
            ])
        
        # Worker figure (simplified)
        pygame.draw.circle(screen, YELLOW, (self.x - 30, self.y + 15), 8)  # Head with hard hat
        pygame.draw.rect(screen, ORANGE, (self.x - 38, self.y + 23, 16, 20))  # Body (vest)
        
        # Construction sign
        sign_x = self.x + 40
        pygame.draw.rect(screen, ORANGE, (sign_x - 25, self.y + 10, 50, 40), border_radius=5)
        pygame.draw.polygon(screen, BLACK, [
            (sign_x, self.y + 20),
            (sign_x - 10, self.y + 35),
            (sign_x + 10, self.y + 35)
        ])
        
        # Warning sign
        self.draw_warning_sign(screen, self.y - 40)
    
    def draw_congestion(self, screen):
        # Draw multiple stopped/slow cars in traffic
        # Car 1
        pygame.draw.rect(screen, BLUE, (self.x - 80, self.y + 10, 35, 55), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x - 78, self.y + 15, 31, 15))
        
        # Car 2
        pygame.draw.rect(screen, RED, (self.x - 30, self.y + 20, 35, 55), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x - 28, self.y + 25, 31, 15))
        
        # Car 3
        pygame.draw.rect(screen, SILVER, (self.x + 20, self.y + 15, 35, 55), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x + 22, self.y + 20, 31, 15))
        
        # Car 4 (behind)
        pygame.draw.rect(screen, ORANGE, (self.x + 65, self.y + 25, 35, 55), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x + 67, self.y + 30, 31, 15))
        
        # Exhaust/frustration lines
        for i in range(3):
            y_pos = self.y + 70 + i * 8
            pygame.draw.line(screen, GRAY, (self.x - 70, y_pos), (self.x - 50, y_pos), 2)
            pygame.draw.line(screen, GRAY, (self.x + 30, y_pos), (self.x + 50, y_pos), 2)
        
        # Warning sign
        self.draw_warning_sign(screen, self.y - 40)
    
    def draw_warning_sign(self, screen, y_pos):
        # Triangle warning sign
        sign_x = self.x
        pygame.draw.polygon(screen, YELLOW, [
            (sign_x, y_pos),
            (sign_x - 25, y_pos + 40),
            (sign_x + 25, y_pos + 40)
        ])
        pygame.draw.polygon(screen, BLACK, [
            (sign_x, y_pos + 5),
            (sign_x - 22, y_pos + 37),
            (sign_x + 22, y_pos + 37)
        ], 3)
        # Exclamation mark
        pygame.draw.rect(screen, BLACK, (sign_x - 3, y_pos + 12, 6, 15))
        pygame.draw.circle(screen, BLACK, (sign_x, y_pos + 32), 3)
    
    def move(self, speed):
        self.y += speed
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100

class MenuButton:
    def __init__(self, x, y, width, height, text, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.hovered = False
        
    def draw(self, screen):
        # Clean, modern button styling
        if self.hovered:
            bg_color = (255, 210, 80)
            border_color = (255, 180, 50)
            text_color = (30, 30, 35)
        else:
            bg_color = (45, 47, 55)
            border_color = (70, 72, 80)
            text_color = (255, 220, 80)  # Yellow text
        
        # Subtle shadow
        shadow_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 40), (2, 2, self.width, self.height), border_radius=10)
        screen.blit(shadow_surface, (self.x - 2, self.y))
        
        # Button background
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height), border_radius=10)
        
        # Border
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2, border_radius=10)
        
        # Highlight at top (subtle 3D effect)
        if not self.hovered:
            pygame.draw.line(screen, (60, 62, 70), 
                           (self.x + 10, self.y + 1), 
                           (self.x + self.width - 10, self.y + 1), 1)
        
        # Draw text
        button_font = FONTS[28]
        text_surface = button_font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.hovered = (self.x <= pos[0] <= self.x + self.width and 
                       self.y <= pos[1] <= self.y + self.height)
        return self.hovered
    
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)

class IconButton:
    def __init__(self, x, y, incident_type, label, number, icon_image=None):
        self.x = x
        self.y = y
        self.width = 110
        self.height = 120
        self.incident_type = incident_type
        self.label = label
        self.number = number
        self.icon_image = icon_image
        self.hovered = False
        
    def draw(self, screen, font):
        # Button background with cleaner style
        if self.hovered:
            bg_color = (70, 70, 75)
            border_color = YELLOW
            border_width = 3
        else:
            bg_color = (50, 50, 55)
            border_color = (100, 100, 105)
            border_width = 2
        
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), border_width, border_radius=10)
        
        # Number badge in top-left corner
        badge_radius = 12
        badge_x = self.x + 18
        badge_y = self.y + 18
        pygame.draw.circle(screen, YELLOW, (badge_x, badge_y), badge_radius)
        number_font = FONTS[22]
        number_text = number_font.render(str(self.number), True, BLACK)
        number_rect = number_text.get_rect(center=(badge_x, badge_y))
        screen.blit(number_text, number_rect)
        
        # Draw icon - use image if available, otherwise draw shapes
        icon_center_y = self.y + 55
        if self.icon_image:
            # Display the custom icon image
            icon_rect = self.icon_image.get_rect(center=(self.x + self.width // 2, icon_center_y))
            screen.blit(self.icon_image, icon_rect)
        else:
            # Fallback to drawn icons
            icon_y = self.y + 30
            cx = self.x + self.width // 2
            if self.incident_type == 'roadwork':
                # Construction cone
                pygame.draw.polygon(screen, ORANGE, [
                    (cx, icon_y), (cx - 12, icon_y + 25), (cx + 12, icon_y + 25)
                ])
                pygame.draw.rect(screen, WHITE, (cx - 8, icon_y + 10, 16, 4))
            elif self.incident_type == 'accident':
                # Mini crashed cars
                pygame.draw.rect(screen, RED, (cx - 18, icon_y, 15, 22), border_radius=2)
                pygame.draw.rect(screen, BLUE, (cx + 3, icon_y, 15, 22), border_radius=2)
            elif self.incident_type == 'closure':
                # Barrier
                pygame.draw.rect(screen, RED, (cx - 25, icon_y + 8, 50, 10), border_radius=2)
                pygame.draw.rect(screen, WHITE, (cx - 20, icon_y + 10, 10, 6))
                pygame.draw.rect(screen, WHITE, (cx + 10, icon_y + 10, 10, 6))
            elif self.incident_type == 'congestion':
                # Multiple cars
                pygame.draw.rect(screen, BLUE, (cx - 22, icon_y, 12, 20), border_radius=2)
                pygame.draw.rect(screen, RED, (cx - 6, icon_y, 12, 20), border_radius=2)
                pygame.draw.rect(screen, SILVER, (cx + 10, icon_y, 12, 20), border_radius=2)
        
        # Label
        label_font = FONTS[18]
        text = label_font.render(self.label, True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height - 18))
        screen.blit(text, text_rect)
    
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)
    
    def check_hover(self, pos):
        self.hovered = (self.x <= pos[0] <= self.x + self.width and 
                       self.y <= pos[1] <= self.y + self.height)

def draw_menu(screen, menu_buttons, font, title_font, title_logo=None, leaderboard=None):
    # Dark gradient background
    for y in range(SCREEN_HEIGHT):
        # Create a subtle blue-gray gradient
        ratio = y / SCREEN_HEIGHT
        r = int(18 + ratio * 12)
        g = int(20 + ratio * 15)
        b = int(28 + ratio * 18)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Animated road in background (subtle)
    road_y_offset = (pygame.time.get_ticks() // 25) % 80
    
    # Road with subtle glow
    road_glow = pygame.Surface((ROAD_WIDTH + 20, SCREEN_HEIGHT), pygame.SRCALPHA)
    road_glow.fill((40, 40, 45, 100))
    screen.blit(road_glow, (ROAD_X - 10, 0))
    
    pygame.draw.rect(screen, (35, 35, 40), (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Road edge lines (subtle white)
    pygame.draw.rect(screen, (80, 80, 85), (ROAD_X, 0, 4, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (80, 80, 85), (ROAD_X + ROAD_WIDTH - 4, 0, 4, SCREEN_HEIGHT))
    
    # Animated lane lines
    for i in range(-1, SCREEN_HEIGHT // 80 + 2):
        lane_y = i * 80 + road_y_offset
        lane_x = ROAD_X + ROAD_WIDTH // 2 - 4
        pygame.draw.rect(screen, (180, 160, 60), (lane_x, lane_y, 8, 35), border_radius=2)
    
    # Side areas
    pygame.draw.rect(screen, (25, 35, 25), (0, 0, ROAD_X, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (25, 35, 25), (ROAD_X + ROAD_WIDTH, 0, SCREEN_WIDTH - ROAD_X - ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Main panel - clean and modern
    panel_width = 380
    panel_height = 450
    panel_x = SCREEN_WIDTH // 2 - panel_width // 2
    panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
    
    # Panel shadow (soft)
    for i in range(3):
        shadow_alpha = 40 - i * 12
        shadow_offset = 4 + i * 2
        shadow_surface = pygame.Surface((panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 0, panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), border_radius=18)
        screen.blit(shadow_surface, (panel_x - shadow_offset, panel_y + shadow_offset // 2))
    
    # Panel background with gradient
    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    for py in range(panel_height):
        ratio = py / panel_height
        r = int(30 + ratio * 8)
        g = int(32 + ratio * 8)
        b = int(38 + ratio * 10)
        pygame.draw.line(panel_surface, (r, g, b, 245), (0, py), (panel_width, py))
    screen.blit(panel_surface, (panel_x, panel_y))
    
    # Panel border (subtle golden)
    pygame.draw.rect(screen, (200, 170, 80), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=15)
    
    # Inner highlight line at top
    pygame.draw.line(screen, (60, 62, 70), (panel_x + 15, panel_y + 1), (panel_x + panel_width - 15, panel_y + 1), 1)
    
    # Title - use logo image if available
    if title_logo:
        logo_rect = title_logo.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 75))
        
        # Subtle glow behind logo
        glow_surface = pygame.Surface((logo_rect.width + 40, logo_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (255, 200, 50, 15), (0, 0, logo_rect.width + 40, logo_rect.height + 20))
        screen.blit(glow_surface, (logo_rect.x - 20, logo_rect.y - 10))
        
        screen.blit(title_logo, logo_rect)
        content_start_y = logo_rect.bottom + 8
    else:
        # Fallback text title
        title_lines = ["REPORT", "RACER"]
        y_offset = panel_y + 50
        for line in title_lines:
            title_shadow = title_font.render(line, True, (20, 20, 25))
            title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, y_offset + 2))
            screen.blit(title_shadow, title_shadow_rect)
            
            title_text = title_font.render(line, True, (255, 210, 80))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(title_text, title_rect)
            y_offset += 48
        content_start_y = y_offset
    
    # Subtitle with decorative elements
    subtitle_y = content_start_y + 5
    
    # Decorative dots
    dot_spacing = 8
    for i in range(5):
        dot_x = SCREEN_WIDTH // 2 - 20 + i * dot_spacing
        pygame.draw.circle(screen, (180, 160, 60), (dot_x, subtitle_y), 2)
    
    subtitle_font = FONTS[20]
    subtitle = subtitle_font.render("Report Incidents & Avoid Traffic", True, YELLOW)
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, subtitle_y + 18))
    screen.blit(subtitle, subtitle_rect)
    
    # Draw menu buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in menu_buttons:
        button.check_hover(mouse_pos)
        button.draw(screen)
    
    # Version at bottom (very subtle)
    credit_font = FONTS[16]
    credit = credit_font.render("v1.0", True, (60, 60, 65))
    credit_rect = credit.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 12))
    screen.blit(credit, credit_rect)

def blend_color(color1, color2, progress):
    """Smoothly blend between two colors based on progress (0.0 to 1.0)"""
    return (
        int(color1[0] + (color2[0] - color1[0]) * progress),
        int(color1[1] + (color2[1] - color1[1]) * progress),
        int(color1[2] + (color2[2] - color1[2]) * progress)
    )

def get_blended_biome_colors(from_biome, to_biome, progress):
    """Get all biome colors blended based on transition progress between any two biomes"""
    from_b = BIOMES[from_biome]
    to_b = BIOMES[to_biome]
    
    return {
        'grass': blend_color(from_b['grass'], to_b['grass'], progress),
        'grass_dark': blend_color(from_b['grass_dark'], to_b['grass_dark'], progress),
        'grass_stripe': blend_color(from_b['grass_stripe'], to_b['grass_stripe'], progress),
        'road': blend_color(from_b['road'], to_b['road'], progress),
        'road_dark': blend_color(from_b['road_dark'], to_b['road_dark'], progress),
        'lane_line': blend_color(from_b['lane_line'], to_b['lane_line'], progress),
        'edge_line': blend_color(from_b['edge_line'], to_b['edge_line'], progress),
        'tree_trunk': blend_color(from_b['tree_trunk'], to_b['tree_trunk'], progress),
        'tree_leaves': blend_color(from_b['tree_leaves'], to_b['tree_leaves'], progress),
        'tree_dark': blend_color(from_b['tree_dark'], to_b['tree_dark'], progress),
        'sky_top': blend_color(from_b['sky_top'], to_b['sky_top'], progress),
        'sky_bottom': blend_color(from_b['sky_bottom'], to_b['sky_bottom'], progress)
    }

def draw_road(screen, lane_lines, road_speed, road_offset, biome='normal', transition_progress=0.0, from_biome='normal', to_biome='normal'):
    # Get blended biome colors based on transition progress
    if transition_progress > 0 and transition_progress < 1:
        b = get_blended_biome_colors(from_biome, to_biome, transition_progress)
    else:
        b = BIOMES[biome]
    
    # Draw grass on sides with better texture and details
    for side in [0, ROAD_X + ROAD_WIDTH]:
        side_width = ROAD_X if side == 0 else SCREEN_WIDTH - side
        
        # Base grass/snow layer
        pygame.draw.rect(screen, b['grass'], (side, 0, side_width, SCREEN_HEIGHT))
    
    # Add small snow mounds - only when fully in winter biome (not during transition)
    if biome == 'winter' and transition_progress >= 1.0:
        for side in [0, ROAD_X + ROAD_WIDTH]:
            side_width = ROAD_X if side == 0 else SCREEN_WIDTH - side
            # Use fixed positions based on index, not random
            for i in range(0, SCREEN_HEIGHT, 60):
                bush_y = (i + int(road_offset * 1.2)) % SCREEN_HEIGHT
                bush_x = side + 50 + (i * 7) % (max(1, side_width - 80))
                
                mound_colors = [(240, 248, 255), (220, 235, 250), (230, 242, 255)]
                pygame.draw.circle(screen, mound_colors[0], (bush_x, bush_y), 10)
                pygame.draw.circle(screen, mound_colors[1], (bush_x - 6, bush_y + 3), 8)
                pygame.draw.circle(screen, mound_colors[2], (bush_x + 6, bush_y + 3), 8)
    
    # Draw road base
    pygame.draw.rect(screen, b['road'], (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Draw road edge lines
    pygame.draw.rect(screen, b['edge_line'], (ROAD_X, 0, 8, SCREEN_HEIGHT))
    pygame.draw.rect(screen, b['edge_line'], (ROAD_X + ROAD_WIDTH - 8, 0, 8, SCREEN_HEIGHT))
    
    # Draw edge line shadows for depth
    pygame.draw.rect(screen, b['road_dark'], (ROAD_X + 8, 0, 3, SCREEN_HEIGHT))
    pygame.draw.rect(screen, b['road_dark'], (ROAD_X + ROAD_WIDTH - 11, 0, 3, SCREEN_HEIGHT))
    
    # Draw lane lines with biome color
    for lane in lane_lines:
        lane.draw(screen, b['lane_line'])
        lane.move(road_speed)
        
    # Remove off-screen lanes and add new ones
    lane_lines[:] = [lane for lane in lane_lines if not lane.is_off_screen()]
    
    # Add new lane lines
    while len(lane_lines) < 20:
        last_y = lane_lines[-1].y if lane_lines else -LANE_GAP
        new_y = last_y - LANE_HEIGHT - LANE_GAP
        # Create lanes for the road divisions
        lane_x = ROAD_X + ROAD_WIDTH // 2 - LANE_WIDTH // 2
        lane_lines.append(LaneLine(lane_x, new_y))

def draw_leaderboard(screen, leaderboard, font, title_font, y_start=200):
    """Draw the leaderboard on screen"""
    # Title
    title = title_font.render("TOP 5", True, YELLOW)
    title_shadow = title_font.render("TOP 5", True, BLACK)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, y_start))
    screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title, title_rect)
    
    # Leaderboard entries
    y_offset = y_start + 70
    for i, entry in enumerate(leaderboard):
        rank_color = [YELLOW, SILVER, (205, 127, 50), (100, 149, 237), (147, 112, 219)][i]  # Gold, Silver, Bronze, 4th, 5th
        
        # Rank - left aligned (size 21)
        rank_font = FONTS[21]
        rank_text = rank_font.render(f"{i + 1}.", True, rank_color)
        screen.blit(rank_text, (SCREEN_WIDTH // 2 - 150, y_offset))
        
        # Name - left aligned, truncate to 20 characters (size 20)
        name_font = FONTS[20]
        display_name = entry['name'][:20]
        name_text = name_font.render(display_name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 100, y_offset))
        
        # Score - right aligned, centered with name (size 25)
        score_font = FONTS[25]
        score_text = score_font.render(str(entry['score']), True, YELLOW)
        name_center_y = y_offset + name_text.get_height() // 2
        score_rect = score_text.get_rect(right=SCREEN_WIDTH // 2 + 150, centery=name_center_y)
        screen.blit(score_text, score_rect)
        
        y_offset += 50

def main():
    if FULLSCREEN:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Report Race")
    clock = pygame.time.Clock()
    
    # Load leaderboard
    leaderboard = load_leaderboard()
    
    # Load sound effects
    try:
        crash_sound = pygame.mixer.Sound('sounds/crash.mp3')
    except:
        crash_sound = None
        print("Warning: Could not load sounds/crash.mp3")
    
    try:
        car_sound = pygame.mixer.Sound('sounds/car_sound.mp3')
    except:
        car_sound = None
        print("Warning: Could not load sounds/car_sound.mp3")
    
    try:
        coin_sound = pygame.mixer.Sound('sounds/coin.mp3')
    except:
        coin_sound = None
        print("Warning: Could not load sounds/coin.mp3")
    
    try:
        menu_sound = pygame.mixer.Sound('sounds/menu.mp3')
    except:
        menu_sound = None
        print("Warning: Could not load sounds/menu.mp3")
    
    try:
        car_engine_sound = pygame.mixer.Sound('sounds/car_engine.mp3')
    except:
        car_engine_sound = None
        print("Warning: Could not load sounds/car_engine.mp3")
    
    try:
        incident_sound = pygame.mixer.Sound('sounds/incident.mp3')
    except:
        incident_sound = None
        print("Warning: Could not load sounds/incident.mp3")
    
    # Create a dedicated channel for car engine (so we can pause/unpause it)
    engine_channel = pygame.mixer.Channel(0)
    
    # Create a dedicated channel for radio music (so we can pause/unpause it)
    radio_channel = pygame.mixer.Channel(1)
    
    # Load radio music options
    radio_tracks = [
        {"name": "OFF", "sound": None},
        {"name": "Tokyo Drift", "sound": None}
    ]
    
    # Load Tokyo Drift
    try:
        tokyo_drift = pygame.mixer.Sound('sounds/tokyo_drift.mp3')
        tokyo_drift.set_volume(0.3)  # Lower volume so it's not too loud
        radio_tracks[1]["sound"] = tokyo_drift
    except:
        print("Warning: Could not load sounds/tokyo_drift.mp3")
    
    # Radio settings
    selected_radio = 0  # 0 = OFF, 1 = Tokyo Drift
    
    # Sound settings
    sound_enabled = True
    
    # Start menu music (game starts in MENU state)
    if menu_sound and sound_enabled:
        menu_sound.play(loops=-1)
    
    # Load title logo
    try:
        title_logo = pygame.image.load('images/title.png').convert_alpha()
        # Scale the logo if needed (you can adjust these dimensions)
        logo_width = 250
        logo_height = int(title_logo.get_height() * (logo_width / title_logo.get_width()))
        title_logo = pygame.transform.scale(title_logo, (logo_width, logo_height))
    except:
        title_logo = None
        print("Warning: Could not load images/title.png")
    
    # Load incident icons
    incident_icons = {}
    icon_size = (80, 80)  # Size for the icons in buttons
    for incident_type in ['roadwork', 'accident', 'closure', 'congestion']:
        try:
            icon = pygame.image.load(f'images/{incident_type}.png').convert_alpha()
            # Scale to fit button
            icon = pygame.transform.scale(icon, icon_size)
            incident_icons[incident_type] = icon
        except:
            incident_icons[incident_type] = None
            print(f"Warning: Could not load images/{incident_type}.png")
    
    # Load incident scene images for display (supports multiple images per type)
    incident_scenes = {}
    max_width = 700
    max_height = 220
    
    for incident_type in ['roadwork', 'accident', 'closure', 'congestion']:
        scenes_list = []
        
        # First try loading the base image (e.g., accident_scene.png)
        for ext in ['.png', '.jpeg', '.jpg']:
            try:
                scene = pygame.image.load(f'images/{incident_type}_scene{ext}').convert()
                orig_width, orig_height = scene.get_size()
                width_ratio = max_width / orig_width
                height_ratio = max_height / orig_height
                scale_factor = min(width_ratio, height_ratio)
                new_width = int(orig_width * scale_factor)
                new_height = int(orig_height * scale_factor)
                scene = pygame.transform.scale(scene, (new_width, new_height))
                scenes_list.append(scene)
                break
            except:
                continue
        
        # Then try loading numbered images (e.g., accident_scene1.png, accident_scene2.png, etc.)
        for i in range(1, 10):  # Support up to 9 additional images per type
            for ext in ['.png', '.jpeg', '.jpg']:
                try:
                    scene = pygame.image.load(f'images/{incident_type}_scene{i}{ext}').convert()
                    orig_width, orig_height = scene.get_size()
                    width_ratio = max_width / orig_width
                    height_ratio = max_height / orig_height
                    scale_factor = min(width_ratio, height_ratio)
                    new_width = int(orig_width * scale_factor)
                    new_height = int(orig_height * scale_factor)
                    scene = pygame.transform.scale(scene, (new_width, new_height))
                    scenes_list.append(scene)
                    break
                except:
                    continue
        
        if len(scenes_list) == 0:
            print(f"Warning: Could not load any {incident_type}_scene images")
        else:
            print(f"Loaded {len(scenes_list)} image(s) for {incident_type}")
        
        incident_scenes[incident_type] = scenes_list
    
    # Font
    font = FONTS[36]
    small_font = FONTS[28]
    large_font = FONTS[72]
    title_font = FONTS[80]
    
    # Game state
    game_state = MENU
    
    # Menu buttons - properly centered in the panel
    button_width = 220
    button_height = 45
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    start_button_y = SCREEN_HEIGHT // 2 - 85  # Adjusted for 5 buttons
    button_spacing = 50  # Space between buttons
    
    menu_buttons = [
        MenuButton(button_x, start_button_y, button_width, button_height, "START GAME", font),
        MenuButton(button_x, start_button_y + button_spacing, button_width, button_height, "HOW TO PLAY", font),
        MenuButton(button_x, start_button_y + button_spacing * 2, button_width, button_height, "LEADERBOARD", font),
        MenuButton(button_x, start_button_y + button_spacing * 3, button_width, button_height, "SETTINGS", font),
        MenuButton(button_x, start_button_y + button_spacing * 4, button_width, button_height, "QUIT", font)
    ]
    
    # Create player car
    player_car = Car(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 130)
    
    # Lane lines
    lane_lines = []
    for i in range(15):
        lane_x = ROAD_X + ROAD_WIDTH // 2 - LANE_WIDTH // 2
        lane_y = i * (LANE_HEIGHT + LANE_GAP)
        lane_lines.append(LaneLine(lane_x, lane_y))
    
    # Obstacle cars
    obstacle_cars = []
    
    # Coins
    coins = []
    coin_spawn_timer = 0
    coin_spawn_delay = 60  # Spawn coin every ~1 second
    coins_collected = 0
    
    # Game variables
    road_speed = 5
    base_speed = 5
    score = 0
    spawn_timer = 0
    spawn_delay = 60  # Frames between spawns
    road_offset = 0
    distance_traveled = 0  # Track distance for progressive difficulty
    
    # Biome system
    current_biome = 'normal'
    target_biome = 'normal'
    snowflakes = [Snowflake() for _ in range(100)]  # Pre-create snowflakes
    falling_leaves = [FallingLeaf() for _ in range(80)]  # Pre-create falling leaves
    falling_petals = [FallingPetal() for _ in range(100)]  # Pre-create cherry blossom petals
    bubbles = [Bubble() for _ in range(25)]  # Pre-create underwater bubbles
    falling_embers = [FallingEmber() for _ in range(50)]  # Pre-create lava embers
    biome_transition_timer = 0  # For showing biome notification
    biome_notification_text = ""  # Text to show for biome change
    biome_transition_progress = 0.0  # 0.0 = start biome, 1.0 = target biome
    biome_transition_speed = 0.012  # How fast the transition happens (faster for smoother feel)
    previous_biome = 'normal'  # Track previous biome for transitions
    biome_changed = False
    
    # Name input for high scores
    player_name = ""
    name_input_active = False
    
    # Screen shake effect
    shake_amount = 0
    shake_duration = 0
    
    # Incident system
    current_incident = None
    incident_timer = 0
    incident_delay = random.randint(300, 600)  # Random time between incidents
    showing_incident = False
    incident_buttons = []
    correct_reports = 0
    wrong_reports = 0
    report_timer = 0  # Timer for reporting (in frames, 60 fps = 1 second)
    report_time_limit = 300  # 5 seconds at 60 FPS
    
    # Popup feedback system
    show_popup = False
    popup_timer = 0
    popup_duration = 60  # 1 second at 60 FPS
    popup_type = None  # 'wrong' or 'correct'
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Menu state events
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == MENU:
                mouse_pos = pygame.mouse.get_pos()
                if menu_buttons[0].is_clicked(mouse_pos):  # Start button
                    game_state = PLAYING
                    # Stop menu music and play car driving sound on loop
                    if menu_sound:
                        menu_sound.stop()
                    if car_sound and sound_enabled:
                        car_sound.play(loops=-1)
                    # Play car engine sound on loop
                    if car_engine_sound and sound_enabled:
                        engine_channel.play(car_engine_sound, loops=-1)
                    # Play radio music if selected
                    if selected_radio > 0 and radio_tracks[selected_radio]["sound"] and sound_enabled:
                        radio_channel.play(radio_tracks[selected_radio]["sound"], loops=-1)
                elif menu_buttons[1].is_clicked(mouse_pos):  # How to Play button
                    game_state = HOW_TO_PLAY
                elif menu_buttons[2].is_clicked(mouse_pos):  # Leaderboard button
                    game_state = LEADERBOARD_VIEW
                elif menu_buttons[3].is_clicked(mouse_pos):  # Settings button
                    game_state = SETTINGS
                elif menu_buttons[4].is_clicked(mouse_pos):  # Quit button
                    running = False
            
            # How to Play view state events
            elif event.type == pygame.KEYDOWN and game_state == HOW_TO_PLAY:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    game_state = MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == HOW_TO_PLAY:
                game_state = MENU
            
            # Leaderboard view state events
            elif event.type == pygame.KEYDOWN and game_state == LEADERBOARD_VIEW:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    game_state = MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == LEADERBOARD_VIEW:
                # Any click returns to menu
                game_state = MENU
            
            # Settings state events
            elif event.type == pygame.KEYDOWN and game_state == SETTINGS:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == SETTINGS:
                mouse_pos = pygame.mouse.get_pos()
                # Calculate panel position (same as drawing)
                settings_panel_width = 350
                settings_panel_height = 320
                settings_panel_x = SCREEN_WIDTH // 2 - settings_panel_width // 2
                settings_panel_y = SCREEN_HEIGHT // 2 - settings_panel_height // 2
                
                # Check if sound toggle button was clicked
                toggle_x = settings_panel_x + settings_panel_width // 2 - 100
                toggle_y = settings_panel_y + 90
                toggle_width = 200
                toggle_height = 45
                if toggle_x <= mouse_pos[0] <= toggle_x + toggle_width and toggle_y <= mouse_pos[1] <= toggle_y + toggle_height:
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        # Resume menu music
                        if menu_sound:
                            menu_sound.play(loops=-1)
                    else:
                        # Stop all sounds
                        if menu_sound:
                            menu_sound.stop()
                        if car_sound:
                            car_sound.stop()
                        if crash_sound:
                            crash_sound.stop()
                        if coin_sound:
                            coin_sound.stop()
                        engine_channel.stop()
                        radio_channel.stop()
                
                # Check if radio button was clicked
                radio_x = settings_panel_x + settings_panel_width // 2 - 100
                radio_y = settings_panel_y + 150
                radio_width = 200
                radio_height = 45
                if radio_x <= mouse_pos[0] <= radio_x + radio_width and radio_y <= mouse_pos[1] <= radio_y + radio_height:
                    # Cycle through radio options
                    selected_radio = (selected_radio + 1) % len(radio_tracks)
                
                # Check if back button was clicked
                back_x = settings_panel_x + settings_panel_width // 2 - 75
                back_y = settings_panel_y + 210
                back_width = 150
                back_height = 45
                if back_x <= mouse_pos[0] <= back_x + back_width and back_y <= mouse_pos[1] <= back_y + back_height:
                    game_state = MENU
            
            # Name input state events
            elif event.type == pygame.KEYDOWN and game_state == NAME_INPUT:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    # Save to leaderboard
                    leaderboard = add_to_leaderboard(player_name, score, leaderboard)
                    save_leaderboard(leaderboard)
                    game_state = GAME_OVER
                    name_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 20 and event.unicode.isprintable():
                    # Add character to name
                    player_name += event.unicode.upper()
            
            # Game over state events
            elif event.type == pygame.KEYDOWN and game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    # Reset game variables and go to menu
                    player_car.x = SCREEN_WIDTH // 2 - 25
                    player_car.y = SCREEN_HEIGHT - 130
                    obstacle_cars.clear()
                    road_speed = base_speed
                    score = 0
                    game_state = MENU  # Go to menu instead of directly to playing
                    # Resume menu music
                    if menu_sound and sound_enabled:
                        menu_sound.play(loops=-1)
                    spawn_timer = 0
                    road_offset = 0
                    shake_amount = 0
                    shake_duration = 0
                    current_incident = None
                    incident_timer = 0
                    incident_delay = random.randint(300, 600)
                    showing_incident = False
                    incident_buttons.clear()
                    correct_reports = 0
                    show_popup = False
                    popup_timer = 0
                    wrong_reports = 0
                    report_timer = 0
                    coins.clear()
                    coins_collected = 0
                    coin_spawn_timer = 0
                    distance_traveled = 0
                    current_biome = 'normal'  # Reset biome
                    target_biome = 'normal'
                    previous_biome = 'normal'
                    biome_transition_timer = 0
                    biome_transition_progress = 0.0
                    biome_notification_text = ""
                    biome_changed = False
            
            # Incident button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == PLAYING and showing_incident:
                # Check if any incident button was clicked
                mouse_pos = pygame.mouse.get_pos()
                for button in incident_buttons:
                    if button.is_clicked(mouse_pos):
                        # Check if correct button
                        if button.incident_type == current_incident.type:
                            correct_reports += 1
                            score += 50  # Bonus points for correct report
                            popup_type = 'correct'
                        else:
                            wrong_reports += 1
                            score = max(0, score - 25)  # Penalty for wrong report
                            popup_type = 'wrong'
                        
                        # Show popup and resume game
                        show_popup = True
                        popup_timer = popup_duration
                        showing_incident = False
                        current_incident = None
                        incident_buttons.clear()
                        incident_delay = random.randint(300, 600)
                        incident_timer = 0
                        # Resume car engine sound and radio
                        engine_channel.unpause()
                        radio_channel.unpause()
                        break
            
            # Keyboard incident selection
            elif event.type == pygame.KEYDOWN and game_state == PLAYING and showing_incident:
                # Check if number key 1-4 was pressed
                selected_button = None
                if event.key == pygame.K_1:
                    selected_button = incident_buttons[0] if len(incident_buttons) > 0 else None
                elif event.key == pygame.K_2:
                    selected_button = incident_buttons[1] if len(incident_buttons) > 1 else None
                elif event.key == pygame.K_3:
                    selected_button = incident_buttons[2] if len(incident_buttons) > 2 else None
                elif event.key == pygame.K_4:
                    selected_button = incident_buttons[3] if len(incident_buttons) > 3 else None
                
                if selected_button:
                    # Check if correct button
                    if selected_button.incident_type == current_incident.type:
                        correct_reports += 1
                        score += 50  # Bonus points for correct report
                        popup_type = 'correct'
                    else:
                        wrong_reports += 1
                        score = max(0, score - 25)  # Penalty for wrong report
                        popup_type = 'wrong'
                    
                    # Show popup and resume game
                    show_popup = True
                    popup_timer = popup_duration
                    showing_incident = False
                    current_incident = None
                    incident_buttons.clear()
                    incident_delay = random.randint(300, 600)
                    incident_timer = 0
                    # Resume car engine sound and radio
                    engine_channel.unpause()
                    radio_channel.unpause()
        
        # Update screen shake
        if shake_duration > 0:
            shake_duration -= 1
            if shake_duration == 0:
                shake_amount = 0
        
        # Update report timer if incident is being shown
        if showing_incident:
            report_timer -= 1
            if report_timer <= 0:
                # Time ran out - count as wrong report
                wrong_reports += 1
                score = max(0, score - 25)
                popup_type = 'wrong'
                show_popup = True
                popup_timer = popup_duration
                showing_incident = False
                current_incident = None
                incident_buttons.clear()
                incident_delay = random.randint(300, 600)
                incident_timer = 0
                # Resume car engine sound and radio
                engine_channel.unpause()
                radio_channel.unpause()
        
        # Update popup timer
        if show_popup:
            popup_timer -= 1
            if popup_timer <= 0:
                show_popup = False
        
        if game_state == PLAYING and not showing_incident:
            # Update road offset for scrolling texture
            road_offset += road_speed
            
            # Track distance traveled
            distance_traveled += road_speed
            
            # Progressive difficulty - speed increases gradually
            # Every 500 units of distance, increase speed slightly
            speed_increase = (distance_traveled // 500) * 0.5
            road_speed = min(base_speed + speed_increase, 15)  # Cap at speed 15
            
            # Adjust spawn delay based on speed
            spawn_delay = max(25, int(60 - (road_speed - base_speed) * 3))
            
            # Handle input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_car.move(-player_car.speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_car.move(player_car.speed)
            
            # Spawn obstacle vehicles (cars, trucks, bikes)
            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                spawn_timer = 0
                
                # Don't spawn if there's an incident in the upper part of the screen
                can_spawn_car = True
                if current_incident and current_incident.y < SCREEN_HEIGHT // 2:
                    can_spawn_car = False
                
                if can_spawn_car:
                    # Random vehicle type with weighted probabilities
                    vehicle_choice = random.random()
                    if vehicle_choice < 0.55:      # 55% cars
                        vehicle_type = 'car'
                    elif vehicle_choice < 0.80:    # 25% trucks
                        vehicle_type = 'truck'
                    else:                          # 20% bikes (small and fast!)
                        vehicle_type = 'bike'
                    
                    # Random lane position (bikes only spawn in side lanes)
                    if vehicle_type == 'bike':
                        lane_positions = [
                            ROAD_X + 50,               # Left lane only
                            ROAD_X + ROAD_WIDTH - 100  # Right lane only
                        ]
                    else:
                        lane_positions = [
                            ROAD_X + 50,
                            ROAD_X + ROAD_WIDTH // 2 - 25,
                            ROAD_X + ROAD_WIDTH - 100
                        ]
                    x_pos = random.choice(lane_positions)
                    
                    obstacle_cars.append(ObstacleCar(x_pos, -140, road_speed, vehicle_type))
            
            # Spawn coins
            coin_spawn_timer += 1
            if coin_spawn_timer >= coin_spawn_delay:
                coin_spawn_timer = 0
                # Random position on road
                coin_x = random.randint(ROAD_X + 40, ROAD_X + ROAD_WIDTH - 40)
                # Only spawn if not too close to obstacles
                can_spawn = True
                for car in obstacle_cars:
                    if car.y < 50 and abs(car.x + car.width // 2 - coin_x) < 60:
                        can_spawn = False
                        break
                if can_spawn:
                    coins.append(Coin(coin_x, -20))
            
            # Move coins and check collection
            for coin in coins[:]:
                coin.move(road_speed)
                
                # Check collision with player
                if not coin.collected and player_car.get_rect().colliderect(coin.get_rect()):
                    coin.collected = True
                    coins_collected += 1
                    score += 10  # Bonus points for collecting coin
                    # Play coin sound
                    if coin_sound and sound_enabled:
                        coin_sound.play()
                
                # Remove if off screen or collected
                if coin.is_off_screen() or coin.collected:
                    coins.remove(coin)
            
            # Incident system
            incident_timer += 1
            if incident_timer >= incident_delay and current_incident is None:
                # Spawn an incident
                incident_type = random.choice(list(INCIDENT_TYPES.keys()))
                
                # Randomly select a scene image for this incident
                scene_images = incident_scenes.get(incident_type, [])
                selected_scene = random.choice(scene_images) if scene_images else None
                
                current_incident = Incident(incident_type, -100, selected_scene)
                incident_timer = 0
                
                # Clear any cars that are too close to the top (would overlap with incident)
                obstacle_cars[:] = [car for car in obstacle_cars if car.y > 100]
            
            # Move incident
            if current_incident:
                current_incident.move(road_speed)
                
                # Remove any cars that overlap with the incident area
                incident_top = current_incident.y - 80
                incident_bottom = current_incident.y + 80
                obstacle_cars[:] = [car for car in obstacle_cars 
                                   if car.y + car.height < incident_top or car.y > incident_bottom]
                
                # Check if incident reached middle of screen - time to report!
                if current_incident.y >= SCREEN_HEIGHT // 2 - 50 and current_incident.y <= SCREEN_HEIGHT // 2 + 50:
                    if not showing_incident:
                        # Pause and show reporting options
                        showing_incident = True
                        report_timer = report_time_limit  # Start the countdown timer
                        # Pause car engine sound and radio
                        engine_channel.pause()
                        radio_channel.pause()
                        # Play incident sound
                        if incident_sound and sound_enabled:
                            incident_sound.play()
                        
                        # Create icon buttons - centered in panel
                        incident_buttons.clear()
                        incident_list = list(INCIDENT_TYPES.keys())
                        random.shuffle(incident_list)  # Randomize button order
                        
                        # Calculate button positions - properly centered
                        panel_center_y = SCREEN_HEIGHT // 2
                        button_y = panel_center_y + 95  # Below the larger display box
                        button_width = 110
                        button_gap = 15  # Gap between buttons
                        num_buttons = 4
                        total_width = (num_buttons * button_width) + ((num_buttons - 1) * button_gap)
                        start_x = SCREEN_WIDTH // 2 - total_width // 2
                        
                        for i, inc_type in enumerate(incident_list):
                            button_x = start_x + i * (button_width + button_gap)
                            # Get the icon image for this incident type
                            icon_img = incident_icons.get(inc_type, None)
                            incident_buttons.append(
                                IconButton(button_x, button_y, inc_type, INCIDENT_TYPES[inc_type]['name'], i + 1, icon_img)
                            )
                
                # Remove if off screen
                if current_incident and current_incident.is_off_screen():
                    current_incident = None
            
            # Move and check obstacle cars
            collision_detected = False
            for car in obstacle_cars:
                car.move()
                
                # Check collision
                if player_car.get_rect().colliderect(car.get_rect()) and not collision_detected:
                    collision_detected = True
                    # Stop car sound, car engine, radio, and play crash sound
                    if car_sound:
                        car_sound.stop()
                    engine_channel.stop()
                    radio_channel.stop()
                    if crash_sound and sound_enabled:
                        crash_sound.play()
                    # Check if it's a high score
                    if is_high_score(score, leaderboard):
                        game_state = NAME_INPUT
                        name_input_active = True
                        player_name = ""
                    else:
                        game_state = GAME_OVER
                    # Trigger screen shake
                    shake_amount = 20
                    shake_duration = 30
                    break  # Exit loop after collision
            
            # Remove off-screen obstacles and increase score
            for car in obstacle_cars[:]:
                if car.is_off_screen():
                    obstacle_cars.remove(car)
                    score += 10
        
        # Calculate shake offset
        shake_offset_x = 0
        shake_offset_y = 0
        if shake_duration > 0:
            shake_offset_x = random.randint(-shake_amount, shake_amount)
            shake_offset_y = random.randint(-shake_amount, shake_amount)
            # Reduce shake amount over time for smooth decay
            shake_amount = int(shake_amount * 0.9)
        
        # Create a surface for game content (to apply shake effect)
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw based on game state
        if game_state == MENU:
            draw_menu(screen, menu_buttons, font, title_font, title_logo, leaderboard)
        
        elif game_state == HOW_TO_PLAY:
            # Dark gradient background (matching menu)
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(18 + ratio * 12)
                g = int(20 + ratio * 15)
                b = int(28 + ratio * 18)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
            # Animated road in background (subtle)
            road_y_offset = (pygame.time.get_ticks() // 25) % 80
            road_glow = pygame.Surface((ROAD_WIDTH + 20, SCREEN_HEIGHT), pygame.SRCALPHA)
            road_glow.fill((40, 40, 45, 100))
            screen.blit(road_glow, (ROAD_X - 10, 0))
            pygame.draw.rect(screen, (35, 35, 40), (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X, 0, 4, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X + ROAD_WIDTH - 4, 0, 4, SCREEN_HEIGHT))
            for i in range(-1, SCREEN_HEIGHT // 80 + 2):
                lane_y = i * 80 + road_y_offset
                lane_x = ROAD_X + ROAD_WIDTH // 2 - 4
                pygame.draw.rect(screen, (180, 160, 60), (lane_x, lane_y, 8, 35), border_radius=2)
            pygame.draw.rect(screen, (25, 35, 25), (0, 0, ROAD_X, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (25, 35, 25), (ROAD_X + ROAD_WIDTH, 0, SCREEN_WIDTH - ROAD_X - ROAD_WIDTH, SCREEN_HEIGHT))
            
            # Main panel - sized to fit content
            panel_width = 650
            panel_height = 500
            panel_x = SCREEN_WIDTH // 2 - panel_width // 2
            panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
            
            # Panel shadow
            for i in range(3):
                shadow_alpha = 40 - i * 12
                shadow_offset = 4 + i * 2
                shadow_surface = pygame.Surface((panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), pygame.SRCALPHA)
                pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 0, panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), border_radius=18)
                screen.blit(shadow_surface, (panel_x - shadow_offset, panel_y + shadow_offset // 2))
            
            # Panel background with gradient
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            for py in range(panel_height):
                ratio = py / panel_height
                r = int(30 + ratio * 8)
                g = int(32 + ratio * 8)
                b = int(38 + ratio * 10)
                pygame.draw.line(panel_surface, (r, g, b, 245), (0, py), (panel_width, py))
            screen.blit(panel_surface, (panel_x, panel_y))
            
            # Panel border
            pygame.draw.rect(screen, (200, 170, 80), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=15)
            
            # Title
            htp_title_font = FONTS[40]
            title_text = htp_title_font.render("HOW TO PLAY", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
            screen.blit(title_text, title_rect)
            
            # Decorative line under title
            line_width = 200
            line_x = SCREEN_WIDTH // 2 - line_width // 2
            pygame.draw.line(screen, (80, 80, 85), (line_x, panel_y + 50), (line_x + line_width, panel_y + 50), 1)
            
            # Fonts
            section_font = FONTS[22]
            content_font = FONTS[18]
            
            # Game objective section
            objective_y = panel_y + 65
            objective_title = section_font.render("OBJECTIVE", True, YELLOW)
            objective_rect = objective_title.get_rect(center=(SCREEN_WIDTH // 2, objective_y))
            screen.blit(objective_title, objective_rect)
            
            objectives = [
                "Drive and avoid crashing into vehicles. Report incidents for bonus points.",
                "Collect coins on the road for extra points!"
            ]
            
            obj_y = objective_y + 18
            for obj in objectives:
                obj_text = content_font.render(obj, True, (200, 200, 205))
                obj_rect = obj_text.get_rect(center=(SCREEN_WIDTH // 2, obj_y))
                screen.blit(obj_text, obj_rect)
                obj_y += 16
            
            # Controls section
            controls_y = obj_y + 12
            controls_title = section_font.render("CONTROLS", True, YELLOW)
            controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, controls_y))
            screen.blit(controls_title, controls_rect)
            
            ctrl_y = controls_y + 22
            
            # First control - Arrow keys with visual representation
            key_size = 22
            key_gap = 4
            arrow_keys_width = key_size * 2 + key_gap + 30 + key_size * 2 + key_gap  # left/right + " / " + A/D
            desc_text1 = content_font.render(" - Move left and right", True, (200, 200, 205))
            total_width1 = arrow_keys_width + desc_text1.get_width()
            start_x1 = SCREEN_WIDTH // 2 - total_width1 // 2
            
            # Draw left arrow key
            pygame.draw.rect(screen, (60, 62, 70), (start_x1, ctrl_y - 2, key_size, key_size), border_radius=4)
            pygame.draw.rect(screen, (100, 100, 105), (start_x1, ctrl_y - 2, key_size, key_size), 1, border_radius=4)
            # Draw left arrow
            arrow_points_left = [(start_x1 + 14, ctrl_y + 7), (start_x1 + 8, ctrl_y + 9), (start_x1 + 14, ctrl_y + 11)]
            pygame.draw.polygon(screen, (255, 220, 80), arrow_points_left)
            
            # Draw right arrow key
            right_key_x = start_x1 + key_size + key_gap
            pygame.draw.rect(screen, (60, 62, 70), (right_key_x, ctrl_y - 2, key_size, key_size), border_radius=4)
            pygame.draw.rect(screen, (100, 100, 105), (right_key_x, ctrl_y - 2, key_size, key_size), 1, border_radius=4)
            # Draw right arrow
            arrow_points_right = [(right_key_x + 8, ctrl_y + 7), (right_key_x + 14, ctrl_y + 9), (right_key_x + 8, ctrl_y + 11)]
            pygame.draw.polygon(screen, (255, 220, 80), arrow_points_right)
            
            # Draw " / " separator
            slash_x = right_key_x + key_size + 8
            slash_text = content_font.render("/", True, (150, 150, 155))
            screen.blit(slash_text, (slash_x, ctrl_y))
            
            # Draw A key
            a_key_x = slash_x + 18
            pygame.draw.rect(screen, (60, 62, 70), (a_key_x, ctrl_y - 2, key_size, key_size), border_radius=4)
            pygame.draw.rect(screen, (100, 100, 105), (a_key_x, ctrl_y - 2, key_size, key_size), 1, border_radius=4)
            a_text = content_font.render("A", True, (255, 220, 80))
            a_rect = a_text.get_rect(center=(a_key_x + key_size // 2, ctrl_y + key_size // 2 - 2))
            screen.blit(a_text, a_rect)
            
            # Draw D key
            d_key_x = a_key_x + key_size + key_gap
            pygame.draw.rect(screen, (60, 62, 70), (d_key_x, ctrl_y - 2, key_size, key_size), border_radius=4)
            pygame.draw.rect(screen, (100, 100, 105), (d_key_x, ctrl_y - 2, key_size, key_size), 1, border_radius=4)
            d_text = content_font.render("D", True, (255, 220, 80))
            d_rect = d_text.get_rect(center=(d_key_x + key_size // 2, ctrl_y + key_size // 2 - 2))
            screen.blit(d_text, d_rect)
            
            # Draw description
            screen.blit(desc_text1, (d_key_x + key_size + 5, ctrl_y))
            
            ctrl_y += 32
            
            # Second control - Number keys
            key_text2 = content_font.render("1  2  3  4", True, (255, 220, 80))
            desc_text2 = content_font.render(" - Select incident type", True, (200, 200, 205))
            total_width2 = key_text2.get_width() + desc_text2.get_width()
            start_x2 = SCREEN_WIDTH // 2 - total_width2 // 2
            screen.blit(key_text2, (start_x2, ctrl_y))
            screen.blit(desc_text2, (start_x2 + key_text2.get_width(), ctrl_y))
            
            # Incident icons section
            icons_y = ctrl_y + 22
            icons_title = section_font.render("INCIDENT TYPES", True, YELLOW)
            icons_rect = icons_title.get_rect(center=(SCREEN_WIDTH // 2, icons_y))
            screen.blit(icons_title, icons_rect)
            
            # Draw incident icons with descriptions - compact layout
            icon_start_y = icons_y + 20
            icon_spacing = 130
            icons_data = [
                ('roadwork', 'Road Work'),
                ('accident', 'Accident'),
                ('closure', 'Road Closure'),
                ('congestion', 'Congestion')
            ]
            
            total_icons_width = len(icons_data) * icon_spacing
            icon_start_x = SCREEN_WIDTH // 2 - total_icons_width // 2 + icon_spacing // 2
            
            for i, (inc_type, name) in enumerate(icons_data):
                icon_x = icon_start_x + i * icon_spacing
                
                # Icon background - smaller
                icon_bg_surface = pygame.Surface((90, 100), pygame.SRCALPHA)
                pygame.draw.rect(icon_bg_surface, (45, 47, 55, 200), (0, 0, 90, 100), border_radius=8)
                pygame.draw.rect(icon_bg_surface, (70, 72, 80), (0, 0, 90, 100), 2, border_radius=8)
                screen.blit(icon_bg_surface, (icon_x - 45, icon_start_y))
                
                # Draw icon image if available
                icon_img = incident_icons.get(inc_type, None)
                if icon_img:
                    icon_rect = icon_img.get_rect(center=(icon_x, icon_start_y + 40))
                    screen.blit(icon_img, icon_rect)
                
                # Icon name
                name_font = FONTS[16]
                name_text = name_font.render(name, True, (255, 220, 80))
                name_rect = name_text.get_rect(center=(icon_x, icon_start_y + 90))
                screen.blit(name_text, name_rect)
            
            # Tip text
            tip_y = icon_start_y + 115
            tip_font = FONTS[16]
            tip_text = tip_font.render("Quickly identify and select the correct incident type when it appears!", True, (150, 150, 155))
            tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH // 2, tip_y))
            screen.blit(tip_text, tip_rect)
            
            # Scoring section
            score_y = tip_y + 20
            score_title = section_font.render("SCORING", True, YELLOW)
            score_rect = score_title.get_rect(center=(SCREEN_WIDTH // 2, score_y))
            screen.blit(score_title, score_rect)
            
            scores = [
                ("Correct Report: +50", (100, 200, 100)),
                ("Wrong Report: -25", (200, 100, 100)),
                ("Coin: +10", (255, 215, 0))
            ]
            
            # Draw scores in a row
            score_info_y = score_y + 20
            score_texts = []
            for label, color in scores:
                score_texts.append((content_font.render(label, True, color), label))
            
            total_score_width = sum(t[0].get_width() for t in score_texts) + 40  # 40 for spacing
            score_x = SCREEN_WIDTH // 2 - total_score_width // 2
            
            for text_surf, _ in score_texts:
                screen.blit(text_surf, (score_x, score_info_y))
                score_x += text_surf.get_width() + 20
            
            # Back instruction
            back_font = FONTS[18]
            back_text = back_font.render("Press ESC or Click to return", True, (120, 120, 125))
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + panel_height - 20))
            screen.blit(back_text, back_rect)
        
        elif game_state == LEADERBOARD_VIEW:
            # Dark gradient background (matching menu)
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(18 + ratio * 12)
                g = int(20 + ratio * 15)
                b = int(28 + ratio * 18)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
            # Animated road in background (subtle)
            road_y_offset = (pygame.time.get_ticks() // 25) % 80
            road_glow = pygame.Surface((ROAD_WIDTH + 20, SCREEN_HEIGHT), pygame.SRCALPHA)
            road_glow.fill((40, 40, 45, 100))
            screen.blit(road_glow, (ROAD_X - 10, 0))
            pygame.draw.rect(screen, (35, 35, 40), (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X, 0, 4, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X + ROAD_WIDTH - 4, 0, 4, SCREEN_HEIGHT))
            for i in range(-1, SCREEN_HEIGHT // 80 + 2):
                lane_y = i * 80 + road_y_offset
                lane_x = ROAD_X + ROAD_WIDTH // 2 - 4
                pygame.draw.rect(screen, (180, 160, 60), (lane_x, lane_y, 8, 35), border_radius=2)
            pygame.draw.rect(screen, (25, 35, 25), (0, 0, ROAD_X, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (25, 35, 25), (ROAD_X + ROAD_WIDTH, 0, SCREEN_WIDTH - ROAD_X - ROAD_WIDTH, SCREEN_HEIGHT))
            
            # Main panel - clean and modern
            panel_width = 400
            panel_height = 570
            panel_x = SCREEN_WIDTH // 2 - panel_width // 2
            panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
            
            # Panel shadow
            for i in range(3):
                shadow_alpha = 40 - i * 12
                shadow_offset = 4 + i * 2
                shadow_surface = pygame.Surface((panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), pygame.SRCALPHA)
                pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 0, panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), border_radius=18)
                screen.blit(shadow_surface, (panel_x - shadow_offset, panel_y + shadow_offset // 2))
            
            # Panel background with gradient
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            for py in range(panel_height):
                ratio = py / panel_height
                r = int(30 + ratio * 8)
                g = int(32 + ratio * 8)
                b = int(38 + ratio * 10)
                pygame.draw.line(panel_surface, (r, g, b, 245), (0, py), (panel_width, py))
            screen.blit(panel_surface, (panel_x, panel_y))
            
            # Panel border
            pygame.draw.rect(screen, (200, 170, 80), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=15)
            
            # Title
            lb_title_font = FONTS[42]
            title_text = lb_title_font.render("LEADERBOARD", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 40))
            screen.blit(title_text, title_rect)
            
            # Decorative line under title
            line_width = 200
            line_x = SCREEN_WIDTH // 2 - line_width // 2
            pygame.draw.line(screen, (80, 80, 85), (line_x, panel_y + 65), (line_x + line_width, panel_y + 65), 1)
            
            # Draw leaderboard entries
            if len(leaderboard) > 0:
                entry_start_y = panel_y + 90
                entry_height = 75
                rank_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (100, 149, 237), (147, 112, 219)]  # Gold, Silver, Bronze, 4th, 5th
                
                for i, entry in enumerate(leaderboard[:5]):
                    entry_y = entry_start_y + i * entry_height
                    
                    # Entry row background
                    row_surface = pygame.Surface((panel_width - 40, 60), pygame.SRCALPHA)
                    row_color = (45, 47, 55, 180) if i % 2 == 0 else (40, 42, 50, 180)
                    pygame.draw.rect(row_surface, row_color, (0, 0, panel_width - 40, 60), border_radius=8)
                    screen.blit(row_surface, (panel_x + 20, entry_y))
                    
                    # Rank circle with number
                    circle_x = panel_x + 50
                    circle_y = entry_y + 30
                    pygame.draw.circle(screen, rank_colors[i], (circle_x, circle_y), 18)
                    pygame.draw.circle(screen, (255, 255, 255, 50), (circle_x, circle_y), 18, 2)
                    
                    rank_font = FONTS[21]
                    rank_num = rank_font.render(str(i + 1), True, (30, 30, 35))
                    rank_rect = rank_num.get_rect(center=(circle_x, circle_y))
                    screen.blit(rank_num, rank_rect)
                    
                    # Name - left aligned, truncate to 20 characters, centered with rank
                    name_font = FONTS[20]
                    display_name = entry['name'][:20]
                    name_text = name_font.render(display_name, True, (255, 220, 80))
                    name_rect = name_text.get_rect(left=panel_x + 85, centery=circle_y)
                    screen.blit(name_text, name_rect)
                    
                    # Score - right aligned
                    score_font = FONTS[25]
                    score_text = score_font.render(str(entry['score']), True, WHITE)
                    score_rect = score_text.get_rect(right=panel_x + panel_width - 65, centery=entry_y + 30)
                    screen.blit(score_text, score_rect)
                    
                    # "pts" label
                    pts_font = FONTS[18]
                    pts_text = pts_font.render("pts", True, (120, 120, 125))
                    screen.blit(pts_text, (score_rect.right + 5, entry_y + 25))
            else:
                # No scores yet
                no_scores_font = FONTS[28]
                no_scores = no_scores_font.render("No scores yet!", True, (255, 220, 80))
                no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 180))
                screen.blit(no_scores, no_scores_rect)
                
                hint_font = FONTS[20]
                hint = hint_font.render("Play to get on the leaderboard!", True, (140, 140, 145))
                hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 210))
                screen.blit(hint, hint_rect)
            
            # Back instruction
            back_font = FONTS[20]
            back_text = back_font.render("Press ESC or Click to return", True, (120, 120, 125))
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + panel_height - 25))
            screen.blit(back_text, back_rect)
        
        elif game_state == SETTINGS:
            # Dark gradient background (matching menu)
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(18 + ratio * 12)
                g = int(20 + ratio * 15)
                b = int(28 + ratio * 18)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
            # Animated road in background
            road_y_offset = (pygame.time.get_ticks() // 25) % 80
            road_glow = pygame.Surface((ROAD_WIDTH + 20, SCREEN_HEIGHT), pygame.SRCALPHA)
            road_glow.fill((40, 40, 45, 100))
            screen.blit(road_glow, (ROAD_X - 10, 0))
            pygame.draw.rect(screen, (35, 35, 40), (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X, 0, 4, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (80, 80, 85), (ROAD_X + ROAD_WIDTH - 4, 0, 4, SCREEN_HEIGHT))
            for i in range(-1, SCREEN_HEIGHT // 80 + 2):
                lane_y = i * 80 + road_y_offset
                lane_x = ROAD_X + ROAD_WIDTH // 2 - 4
                pygame.draw.rect(screen, (180, 160, 60), (lane_x, lane_y, 8, 35), border_radius=2)
            pygame.draw.rect(screen, (25, 35, 25), (0, 0, ROAD_X, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (25, 35, 25), (ROAD_X + ROAD_WIDTH, 0, SCREEN_WIDTH - ROAD_X - ROAD_WIDTH, SCREEN_HEIGHT))
            
            # Settings panel
            panel_width = 350
            panel_height = 320
            panel_x = SCREEN_WIDTH // 2 - panel_width // 2
            panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
            
            # Panel shadow
            for i in range(3):
                shadow_alpha = 40 - i * 12
                shadow_offset = 4 + i * 2
                shadow_surface = pygame.Surface((panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), pygame.SRCALPHA)
                pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 0, panel_width + shadow_offset * 2, panel_height + shadow_offset * 2), border_radius=18)
                screen.blit(shadow_surface, (panel_x - shadow_offset, panel_y + shadow_offset // 2))
            
            # Panel background
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            for py in range(panel_height):
                ratio = py / panel_height
                r = int(30 + ratio * 8)
                g = int(32 + ratio * 8)
                b = int(38 + ratio * 10)
                pygame.draw.line(panel_surface, (r, g, b, 245), (0, py), (panel_width, py))
            screen.blit(panel_surface, (panel_x, panel_y))
            
            # Panel border
            pygame.draw.rect(screen, (200, 170, 80), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=15)
            
            # Title
            settings_title_font = FONTS[42]
            title_text = settings_title_font.render("SETTINGS", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 40))
            screen.blit(title_text, title_rect)
            
            # Decorative line under title
            line_width = 150
            line_x = SCREEN_WIDTH // 2 - line_width // 2
            pygame.draw.line(screen, (80, 80, 85), (line_x, panel_y + 65), (line_x + line_width, panel_y + 65), 1)
            
            # Sound toggle button - positioned relative to panel
            toggle_x = panel_x + panel_width // 2 - 100
            toggle_y = panel_y + 90
            toggle_width = 200
            toggle_height = 45
            
            # Check hover state
            mouse_pos = pygame.mouse.get_pos()
            toggle_hovered = toggle_x <= mouse_pos[0] <= toggle_x + toggle_width and toggle_y <= mouse_pos[1] <= toggle_y + toggle_height
            
            if toggle_hovered:
                toggle_bg = (255, 210, 80)
                toggle_text_color = (30, 30, 35)
            else:
                toggle_bg = (45, 47, 55)
                toggle_text_color = (255, 220, 80)
            
            pygame.draw.rect(screen, toggle_bg, (toggle_x, toggle_y, toggle_width, toggle_height), border_radius=10)
            pygame.draw.rect(screen, (70, 72, 80), (toggle_x, toggle_y, toggle_width, toggle_height), 2, border_radius=10)
            
            toggle_font = FONTS[28]
            sound_status = "SOUND: ON" if sound_enabled else "SOUND: OFF"
            toggle_text = toggle_font.render(sound_status, True, toggle_text_color)
            toggle_text_rect = toggle_text.get_rect(center=(toggle_x + toggle_width // 2, toggle_y + toggle_height // 2))
            screen.blit(toggle_text, toggle_text_rect)
            
            # Radio button - positioned relative to panel
            radio_x = panel_x + panel_width // 2 - 100
            radio_y = panel_y + 150
            radio_width = 200
            radio_height = 45
            
            radio_hovered = radio_x <= mouse_pos[0] <= radio_x + radio_width and radio_y <= mouse_pos[1] <= radio_y + radio_height
            
            if radio_hovered:
                radio_bg = (255, 210, 80)
                radio_text_color = (30, 30, 35)
            else:
                radio_bg = (45, 47, 55)
                radio_text_color = (255, 220, 80)
            
            pygame.draw.rect(screen, radio_bg, (radio_x, radio_y, radio_width, radio_height), border_radius=10)
            pygame.draw.rect(screen, (70, 72, 80), (radio_x, radio_y, radio_width, radio_height), 2, border_radius=10)
            
            radio_font = FONTS[24]
            radio_status = f"RADIO: {radio_tracks[selected_radio]['name']}"
            radio_text = radio_font.render(radio_status, True, radio_text_color)
            radio_text_rect = radio_text.get_rect(center=(radio_x + radio_width // 2, radio_y + radio_height // 2))
            screen.blit(radio_text, radio_text_rect)
            
            # Back button - positioned relative to panel
            back_x = panel_x + panel_width // 2 - 75
            back_y = panel_y + 210
            back_width = 150
            back_height = 45
            
            back_hovered = back_x <= mouse_pos[0] <= back_x + back_width and back_y <= mouse_pos[1] <= back_y + back_height
            
            if back_hovered:
                back_bg = (255, 210, 80)
                back_text_color = (30, 30, 35)
            else:
                back_bg = (45, 47, 55)
                back_text_color = (255, 220, 80)
            
            pygame.draw.rect(screen, back_bg, (back_x, back_y, back_width, back_height), border_radius=10)
            pygame.draw.rect(screen, (70, 72, 80), (back_x, back_y, back_width, back_height), 2, border_radius=10)
            
            back_font = FONTS[24]
            back_text = back_font.render("BACK", True, back_text_color)
            back_text_rect = back_text.get_rect(center=(back_x + back_width // 2, back_y + back_height // 2))
            screen.blit(back_text, back_text_rect)
        
        elif game_state == PLAYING or game_state == GAME_OVER or game_state == NAME_INPUT:
            # Check for biome changes based on score (check higher scores first)
            if score >= 5000 and target_biome != 'lava':
                previous_biome = current_biome
                target_biome = 'lava'
                biome_transition_progress = 0.0
                biome_transition_timer = 180
                biome_notification_text = "LAVA BIOME"
                biome_changed = True
            elif score >= 4000 and score < 5000 and target_biome != 'underwater' and target_biome != 'lava':
                previous_biome = current_biome
                target_biome = 'underwater'
                biome_transition_progress = 0.0
                biome_transition_timer = 180
                biome_notification_text = "UNDERWATER BIOME"
                biome_changed = True
            elif score >= 3000 and score < 4000 and target_biome != 'winter' and target_biome != 'underwater' and target_biome != 'lava':
                previous_biome = current_biome
                target_biome = 'winter'
                biome_transition_progress = 0.0
                biome_transition_timer = 180
                biome_notification_text = "WINTER BIOME"
                biome_changed = True
            elif score >= 2000 and score < 3000 and target_biome != 'cherry_blossom' and target_biome != 'winter' and target_biome != 'underwater' and target_biome != 'lava':
                previous_biome = current_biome
                target_biome = 'cherry_blossom'
                biome_transition_progress = 0.0
                biome_transition_timer = 180
                biome_notification_text = "CHERRY BLOSSOM"
                biome_changed = True
            elif score >= 1000 and score < 2000 and target_biome != 'autumn' and target_biome != 'cherry_blossom' and target_biome != 'winter' and target_biome != 'underwater' and target_biome != 'lava':
                previous_biome = current_biome
                target_biome = 'autumn'
                biome_transition_progress = 0.0
                biome_transition_timer = 180
                biome_notification_text = "AUTUMN BIOME"
                biome_changed = True
            
            # Smoothly transition biome colors
            if target_biome != current_biome and biome_transition_progress < 1.0:
                biome_transition_progress = min(1.0, biome_transition_progress + biome_transition_speed)
                if biome_transition_progress >= 1.0:
                    current_biome = target_biome
                    biome_transition_progress = 1.0
            
            # Get blended grass color for background fill
            if biome_transition_progress > 0 and biome_transition_progress < 1:
                blended_grass = blend_color(BIOMES[previous_biome]['grass'], BIOMES[target_biome]['grass'], biome_transition_progress)
            else:
                blended_grass = BIOMES[current_biome]['grass']
            
            # Draw everything to game_surface
            game_surface.fill(blended_grass)
            draw_road(game_surface, lane_lines, road_speed if game_state == PLAYING and not showing_incident else 0, road_offset, current_biome, biome_transition_progress, previous_biome, target_biome)
            
            # Draw incident
            if current_incident:
                current_incident.draw(game_surface)
            
            # Draw coins
            for coin in coins:
                coin.draw(game_surface)
            
            # Draw obstacle cars
            for car in obstacle_cars:
                car.draw(game_surface, current_biome)
            
            # Draw player car
            player_car.draw(game_surface, current_biome)
            
            # Draw falling embers - only in lava biome
            if current_biome == 'lava' or target_biome == 'lava':
                ember_alpha_mult = 1.0
                if target_biome == 'lava' and current_biome != 'lava':
                    # Fade in embers when transitioning to lava
                    ember_alpha_mult = biome_transition_progress
                
                if ember_alpha_mult > 0:
                    for ember in falling_embers:
                        ember.update()
                        original_alpha = ember.alpha
                        ember.alpha = int(original_alpha * ember_alpha_mult)
                        ember.draw(game_surface)
                        ember.alpha = original_alpha
            
            # Draw bubbles - only in underwater biome
            if current_biome == 'underwater' or target_biome == 'underwater':
                bubble_alpha_mult = 1.0
                if target_biome == 'underwater' and current_biome != 'underwater':
                    # Fade in bubbles when transitioning to underwater
                    bubble_alpha_mult = biome_transition_progress
                elif target_biome == 'lava' and current_biome == 'underwater':
                    # Fade out bubbles when transitioning from underwater to lava
                    bubble_alpha_mult = 1.0 - biome_transition_progress
                
                if bubble_alpha_mult > 0:
                    for bubble in bubbles:
                        bubble.update()
                        original_alpha = bubble.alpha
                        bubble.alpha = int(original_alpha * bubble_alpha_mult)
                        bubble.draw(game_surface)
                        bubble.alpha = original_alpha
            
            # Draw falling petals - only in cherry blossom biome
            if current_biome == 'cherry_blossom' or target_biome == 'cherry_blossom':
                petal_alpha_mult = 1.0
                if target_biome == 'cherry_blossom' and current_biome != 'cherry_blossom':
                    # Fade in petals when transitioning to cherry blossom
                    petal_alpha_mult = biome_transition_progress
                elif target_biome == 'winter' and current_biome == 'cherry_blossom':
                    # Fade out petals when transitioning from cherry blossom to winter
                    petal_alpha_mult = 1.0 - biome_transition_progress
                
                if petal_alpha_mult > 0:
                    for petal in falling_petals:
                        petal.update()
                        original_alpha = petal.alpha
                        petal.alpha = int(original_alpha * petal_alpha_mult)
                        petal.draw(game_surface)
                        petal.alpha = original_alpha
            
            # Draw falling leaves - only in autumn biome
            if current_biome == 'autumn' or target_biome == 'autumn':
                leaf_alpha_mult = 1.0
                if target_biome == 'autumn' and current_biome != 'autumn':
                    # Fade in leaves when transitioning to autumn
                    leaf_alpha_mult = biome_transition_progress
                elif target_biome == 'cherry_blossom' and current_biome == 'autumn':
                    # Fade out leaves when transitioning from autumn to cherry blossom
                    leaf_alpha_mult = 1.0 - biome_transition_progress
                
                if leaf_alpha_mult > 0:
                    for leaf in falling_leaves:
                        leaf.update()
                        original_alpha = leaf.alpha
                        leaf.alpha = int(original_alpha * leaf_alpha_mult)
                        leaf.draw(game_surface)
                        leaf.alpha = original_alpha
            
            # Draw snowflakes - only in winter biome
            if current_biome == 'winter' or target_biome == 'winter':
                snow_alpha_mult = 1.0
                if target_biome == 'winter' and current_biome != 'winter':
                    # Fade in snow when transitioning to winter
                    snow_alpha_mult = biome_transition_progress
                
                if snow_alpha_mult > 0:
                    for snowflake in snowflakes:
                        snowflake.update()
                        original_alpha = snowflake.alpha
                        snowflake.alpha = int(original_alpha * snow_alpha_mult)
                        snowflake.draw(game_surface)
                        snowflake.alpha = original_alpha
            
            # Draw biome transition notification
            if biome_transition_timer > 0:
                biome_transition_timer -= 1
                # Calculate alpha for fade effect
                alpha = min(255, biome_transition_timer * 3)
                
                # Create notification surface - smaller font, top position
                notif_font = FONTS[32]
                
                # Biome-specific notification colors
                if target_biome == 'lava':
                    text_color = (255, 120, 40)
                    box_bg = (80, 20, 10, int(alpha * 0.7))
                    box_border = (255, 80, 20, int(alpha * 0.8))
                elif target_biome == 'underwater':
                    text_color = (100, 200, 255)
                    box_bg = (20, 60, 100, int(alpha * 0.7))
                    box_border = (80, 160, 220, int(alpha * 0.8))
                elif target_biome == 'cherry_blossom':
                    text_color = (255, 180, 200)
                    box_bg = (80, 40, 60, int(alpha * 0.7))
                    box_border = (255, 150, 180, int(alpha * 0.8))
                elif target_biome == 'autumn':
                    text_color = (255, 180, 80)
                    box_bg = (80, 50, 20, int(alpha * 0.7))
                    box_border = (200, 130, 50, int(alpha * 0.8))
                else:  # winter
                    text_color = (180, 220, 255)
                    box_bg = (40, 60, 100, int(alpha * 0.7))
                    box_border = (100, 150, 200, int(alpha * 0.8))
                
                notif_surface = notif_font.render(biome_notification_text, True, text_color)
                notif_rect = notif_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
                
                # Background box - smaller padding
                box_padding = 10
                box_rect = pygame.Rect(notif_rect.left - box_padding, notif_rect.top - box_padding,
                                       notif_rect.width + box_padding * 2, notif_rect.height + box_padding * 2)
                box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(box_surface, box_bg, (0, 0, box_rect.width, box_rect.height), border_radius=8)
                pygame.draw.rect(box_surface, box_border, (0, 0, box_rect.width, box_rect.height), width=2, border_radius=8)
                
                game_surface.blit(box_surface, (box_rect.x, box_rect.y))
                
                # Draw text with alpha
                text_surface = pygame.Surface((notif_rect.width, notif_rect.height), pygame.SRCALPHA)
                text_surface.blit(notif_surface, (0, 0))
                text_surface.set_alpha(alpha)
                game_surface.blit(text_surface, notif_rect)
            
            # === HUD Panel (Top Left) ===
            hud_x = 8
            hud_y = 8
            hud_width = 160
            hud_height = 115
            
            # Panel background with transparency
            hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
            pygame.draw.rect(hud_surface, (20, 20, 25, 200), (0, 0, hud_width, hud_height), border_radius=10)
            pygame.draw.rect(hud_surface, (80, 80, 85, 255), (0, 0, hud_width, hud_height), 2, border_radius=10)
            game_surface.blit(hud_surface, (hud_x, hud_y))
            
            # Score row
            hud_font = FONTS[22]
            score_label = hud_font.render("SCORE", True, (150, 150, 150))
            game_surface.blit(score_label, (hud_x + 10, hud_y + 10))
            score_text = hud_font.render(f"{score}", True, YELLOW)
            game_surface.blit(score_text, (hud_x + 70, hud_y + 10))
            
            # Coins row
            coins_label = hud_font.render("COINS", True, (150, 150, 150))
            game_surface.blit(coins_label, (hud_x + 10, hud_y + 34))
            coins_text = hud_font.render(f"{coins_collected}", True, (255, 215, 0))
            game_surface.blit(coins_text, (hud_x + 70, hud_y + 34))
            # Small coin icon next to value
            pygame.draw.circle(game_surface, (218, 165, 32), (hud_x + 140, hud_y + 40), 6)
            pygame.draw.circle(game_surface, (255, 215, 0), (hud_x + 140, hud_y + 40), 4)
            
            # Speed row
            speed_label = hud_font.render("SPEED", True, (150, 150, 150))
            game_surface.blit(speed_label, (hud_x + 10, hud_y + 58))
            speed_value = hud_font.render(f"{int(road_speed)}", True, WHITE)
            game_surface.blit(speed_value, (hud_x + 70, hud_y + 58))
            
            # Speed bar
            bar_width = 140
            bar_height = 8
            bar_x = hud_x + 10
            bar_y = hud_y + 82
            
            # Background bar
            pygame.draw.rect(game_surface, (40, 40, 45), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
            
            # Fill bar based on speed (5 to 15 range)
            speed_percent = min((road_speed - base_speed) / (15 - base_speed), 1.0)
            fill_width = int(bar_width * speed_percent)
            
            # Color gradient from green to yellow to red
            if speed_percent < 0.33:
                bar_color = (50, 205, 50)  # Green
            elif speed_percent < 0.66:
                bar_color = (255, 200, 50)  # Yellow
            else:
                bar_color = (255, 80, 50)  # Red-orange
            
            if fill_width > 0:
                pygame.draw.rect(game_surface, bar_color, (bar_x, bar_y, fill_width, bar_height), border_radius=4)
            
            # Subtle border
            pygame.draw.rect(game_surface, (60, 60, 65), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=4)
            
            # Speed markers
            for i in range(1, 4):
                marker_x = bar_x + (bar_width * i // 4)
                pygame.draw.line(game_surface, (80, 80, 85), (marker_x, bar_y), (marker_x, bar_y + bar_height), 1)
            
            # Min/Max labels
            tiny_font = FONTS[16]
            min_label = tiny_font.render("MIN", True, (100, 100, 100))
            max_label = tiny_font.render("MAX", True, (100, 100, 100))
            game_surface.blit(min_label, (bar_x, bar_y + 10))
            game_surface.blit(max_label, (bar_x + bar_width - 22, bar_y + 10))
            
            # Draw distance traveled (top right)
            distance_meters = int(distance_traveled / 10)  # Convert to meters
            distance_font = FONTS[28]
            distance_text = distance_font.render(f"{distance_meters}m", True, WHITE)
            distance_rect = distance_text.get_rect(topright=(SCREEN_WIDTH - 12, 12))
            
            # Background panel for distance
            dist_panel_width = distance_rect.width + 20
            dist_panel_height = 30
            dist_panel_x = SCREEN_WIDTH - dist_panel_width - 8
            dist_panel_y = 8
            
            dist_surface = pygame.Surface((dist_panel_width, dist_panel_height), pygame.SRCALPHA)
            pygame.draw.rect(dist_surface, (20, 20, 25, 200), (0, 0, dist_panel_width, dist_panel_height), border_radius=8)
            pygame.draw.rect(dist_surface, (80, 80, 85, 255), (0, 0, dist_panel_width, dist_panel_height), 2, border_radius=8)
            game_surface.blit(dist_surface, (dist_panel_x, dist_panel_y))
            
            game_surface.blit(distance_text, (dist_panel_x + 10, dist_panel_y + 6))
        
            # Draw incident reporting UI
            if showing_incident:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                game_surface.blit(overlay, (0, 0))
                
                # Main panel - sized for larger images
                panel_width = 750
                panel_height = 520
                panel_x = SCREEN_WIDTH // 2 - panel_width // 2
                panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
                
                # Panel background with gradient effect
                pygame.draw.rect(game_surface, (35, 35, 40), (panel_x, panel_y, panel_width, panel_height), border_radius=12)
                pygame.draw.rect(game_surface, (50, 50, 55), (panel_x + 2, panel_y + 2, panel_width - 4, panel_height - 4), border_radius=11)
                pygame.draw.rect(game_surface, YELLOW, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=12)
                
                # Header bar
                header_height = 45
                pygame.draw.rect(game_surface, (45, 45, 50), (panel_x + 3, panel_y + 3, panel_width - 6, header_height), border_radius=10)
                
                # Title (centered in header)
                title_font = FONTS[32]
                title_text = title_font.render("INCIDENT DETECTED!", True, BRIGHT_RED)
                title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + header_height // 2 + 3))
                game_surface.blit(title_text, title_rect)
                
                # Timer display (right side of header)
                seconds_left = max(0, report_timer // 60)
                timer_color = BRIGHT_RED if seconds_left <= 3 else YELLOW
                timer_font = FONTS[36]
                timer_text = timer_font.render(f"{seconds_left}s", True, timer_color)
                timer_x = panel_x + panel_width - 45
                timer_y = panel_y + header_height // 2 + 3
                
                # Timer circle
                pygame.draw.circle(game_surface, (30, 30, 35), (timer_x, timer_y), 22)
                pygame.draw.circle(game_surface, timer_color, (timer_x, timer_y), 22, 2)
                timer_rect = timer_text.get_rect(center=(timer_x, timer_y))
                game_surface.blit(timer_text, timer_rect)
                
                # Content area starts after header
                content_y = panel_y + header_height + 15
                
                # Incident display box - larger for better visibility
                display_box_width = panel_width - 40
                display_box_height = 240
                display_box_x = panel_x + 20
                display_box_y = content_y
                
                # Display box with subtle border
                pygame.draw.rect(game_surface, (25, 25, 30), (display_box_x, display_box_y, display_box_width, display_box_height), border_radius=8)
                pygame.draw.rect(game_surface, (80, 80, 85), (display_box_x, display_box_y, display_box_width, display_box_height), 2, border_radius=8)
                
                # Draw the incident image centered in display box
                if current_incident:
                    scene_image = current_incident.scene_image
                    
                    if scene_image:
                        scene_rect = scene_image.get_rect(center=(display_box_x + display_box_width // 2, display_box_y + display_box_height // 2))
                        game_surface.blit(scene_image, scene_rect)
                    else:
                        # Fallback to drawn incident
                        original_y = current_incident.y
                        original_x = current_incident.x
                        current_incident.y = display_box_y + display_box_height // 2
                        current_incident.x = display_box_x + display_box_width // 2
                        
                        clip_rect = pygame.Rect(display_box_x + 3, display_box_y + 3, display_box_width - 6, display_box_height - 6)
                        game_surface.set_clip(clip_rect)
                        
                        if current_incident.type == 'roadwork':
                            current_incident.draw_roadwork(game_surface)
                        elif current_incident.type == 'accident':
                            current_incident.draw_accident(game_surface)
                        elif current_incident.type == 'closure':
                            current_incident.draw_closure(game_surface)
                        elif current_incident.type == 'congestion':
                            current_incident.draw_congestion(game_surface)
                        
                        game_surface.set_clip(None)
                        current_incident.y = original_y
                        current_incident.x = original_x
                
                # Instruction text
                instruction_y = display_box_y + display_box_height + 18
                instruction_font = FONTS[24]
                instruction = instruction_font.render("Select the correct incident type:", True, WHITE)
                instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, instruction_y))
                game_surface.blit(instruction, instruction_rect)
                
                # Draw buttons in a clean grid
                mouse_pos = pygame.mouse.get_pos()
                for button in incident_buttons:
                    button.check_hover(mouse_pos)
                    button.draw(game_surface, small_font)
                
                # Footer with hints
                footer_y = panel_y + panel_height - 35
                
                # Keyboard hint
                hint_font = FONTS[20]
                keyboard_hint = hint_font.render("Press 1-4 or click to select", True, (140, 140, 140))
                keyboard_rect = keyboard_hint.get_rect(center=(SCREEN_WIDTH // 2, footer_y))
                game_surface.blit(keyboard_hint, keyboard_rect)
                
                # Points info
                points_font = FONTS[18]
                points_text = points_font.render("Correct: +50  |  Wrong: -25", True, (100, 180, 100))
                points_rect = points_text.get_rect(center=(SCREEN_WIDTH // 2, footer_y + 18))
                game_surface.blit(points_text, points_rect)
            
            # Draw name input screen
            if game_state == NAME_INPUT:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                game_surface.blit(overlay, (0, 0))
                
                # Congratulations text (centered)
                congrats_text = large_font.render("HIGH SCORE!", True, YELLOW)
                congrats_shadow = large_font.render("HIGH SCORE!", True, BLACK)
                congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                game_surface.blit(congrats_shadow, (congrats_rect.x + 3, congrats_rect.y + 3))
                game_surface.blit(congrats_text, congrats_rect)
                
                # Score display (centered)
                score_display = font.render(f"Score: {score}", True, WHITE)
                score_shadow = font.render(f"Score: {score}", True, BLACK)
                score_rect = score_display.get_rect(center=(SCREEN_WIDTH // 2, 160))
                game_surface.blit(score_shadow, (score_rect.x + 2, score_rect.y + 2))
                game_surface.blit(score_display, score_rect)
                
                # Input panel
                panel_width = 500
                panel_height = 120
                panel_x = SCREEN_WIDTH // 2 - panel_width // 2
                panel_y = 220
                
                pygame.draw.rect(game_surface, (40, 40, 45), (panel_x, panel_y, panel_width, panel_height), border_radius=12)
                pygame.draw.rect(game_surface, YELLOW, (panel_x, panel_y, panel_width, panel_height), 4, border_radius=12)
                
                # Instruction (centered in panel)
                instruction = small_font.render("Enter your slack username:", True, WHITE)
                instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
                game_surface.blit(instruction, instruction_rect)
                
                # Name input box
                input_box_width = panel_width - 40
                input_box_x = panel_x + 20
                input_box_y = panel_y + 55
                
                pygame.draw.rect(game_surface, (60, 60, 65), (input_box_x, input_box_y, input_box_width, 45), border_radius=8)
                pygame.draw.rect(game_surface, WHITE, (input_box_x, input_box_y, input_box_width, 45), 2, border_radius=8)
                
                # Display name being typed
                name_display = font.render(player_name + "_", True, YELLOW)
                game_surface.blit(name_display, (input_box_x + 15, input_box_y + 8))
                
                # Instructions
                hint = small_font.render("Press ENTER to submit (max 20 characters)", True, (180, 180, 180))
                game_surface.blit(hint, (SCREEN_WIDTH // 2 - 190, panel_y + panel_height + 20))
            
            # Draw popup feedback
            if show_popup and game_state == PLAYING:
                # Small popup at top of screen
                popup_width = 140
                popup_height = 36
                popup_x = SCREEN_WIDTH // 2 - popup_width // 2
                popup_y = 80
                
                # Fade effect based on timer
                alpha = min(230, int((popup_timer / popup_duration) * 230))
                
                popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
                
                if popup_type == 'wrong':
                    # Red background for wrong
                    popup_surface.fill((180, 40, 40, alpha))
                    pygame.draw.rect(popup_surface, (255, 80, 80), (0, 0, popup_width, popup_height), 2, border_radius=8)
                    
                    # Wrong text
                    popup_font = FONTS[28]
                    wrong_text = popup_font.render("WRONG", True, WHITE)
                    text_rect = wrong_text.get_rect(center=(popup_width // 2, popup_height // 2))
                    popup_surface.blit(wrong_text, text_rect)
                else:
                    # Green background for correct
                    popup_surface.fill((40, 150, 40, alpha))
                    pygame.draw.rect(popup_surface, (80, 200, 80), (0, 0, popup_width, popup_height), 2, border_radius=8)
                    
                    # Correct text
                    popup_font = FONTS[28]
                    correct_text = popup_font.render("CORRECT", True, WHITE)
                    text_rect = correct_text.get_rect(center=(popup_width // 2, popup_height // 2))
                    popup_surface.blit(correct_text, text_rect)
                
                game_surface.blit(popup_surface, (popup_x, popup_y))
            
            # Draw game over
            if game_state == GAME_OVER:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                game_surface.blit(overlay, (0, 0))
                
                # Game over text with shadow (centered)
                game_over_shadow = large_font.render("GAME OVER", True, BLACK)
                game_over_text = large_font.render("GAME OVER", True, BRIGHT_RED)
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 70))
                game_surface.blit(game_over_shadow, (game_over_rect.x + 3, game_over_rect.y + 3))
                game_surface.blit(game_over_text, game_over_rect)
                
                # Final score (centered)
                final_score_shadow = font.render(f"Final Score: {score}", True, BLACK)
                final_score_text = font.render(f"Final Score: {score}", True, WHITE)
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 130))
                game_surface.blit(final_score_shadow, (final_score_rect.x + 2, final_score_rect.y + 2))
                game_surface.blit(final_score_text, final_score_rect)
                
                # Draw leaderboard
                if len(leaderboard) > 0:
                    draw_leaderboard(game_surface, leaderboard, font, title_font, y_start=220)
                
                # Menu text (centered)
                menu_shadow = font.render("Press SPACE for Menu", True, BLACK)
                menu_text = font.render("Press SPACE for Menu", True, YELLOW)
                menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                game_surface.blit(menu_shadow, (menu_rect.x + 2, menu_rect.y + 2))
                game_surface.blit(menu_text, menu_rect)
            
            # Apply shake effect and blit to screen
            screen.fill(BLACK)  # Fill screen with black first
            screen.blit(game_surface, (shake_offset_x, shake_offset_y))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

