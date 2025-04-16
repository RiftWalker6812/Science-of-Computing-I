import pygame
from typing import List, Optional

# Item class: Represents collectible or usable items in rooms
class Item:
    def __init__(self, name: str, description: str, count: int):
        self.name = name
        self.description = description
        self.count = count
        # For 2D rendering: Optional sprite and position
        self.sprite: Optional[pygame.Surface] = None  # Placeholder for sprite image
        self.position: Optional[tuple] = None  # (x, y) for rendering in a room

    def load_sprite(self, image_path: str):
        """Load sprite image for rendering (call when initializing game)."""
        self.sprite = pygame.image.load(image_path).convert_alpha()

    def __str__(self) -> str:
        return f"{self.name} (x{self.count}): {self.description}"


# Room class: Represents a room within an area containing items and enemies
class Room:
    def __init__(self, enemy_count: int = 0, danger_level: int = 1):
        self.items: List[Item] = []  # Items in the room
        self.enemy_count = enemy_count  # Number of enemies
        self.danger_level = danger_level  # Affects difficulty or events
        self.adjacent_rooms: List['Room'] = []  # Connected rooms
        # For 2D rendering
        self.position: Optional[tuple] = None  # (x, y) for rendering room on map
        self.sprite: Optional[pygame.Surface] = None  # Optional room sprite

    def add_item(self, item: Item):
        """Add an item to the room."""
        self.items.append(item)

    def add_adjacent_room(self, room: 'Room'):
        """Connect this room to another (bidirectional)."""
        if room not in self.adjacent_rooms:
            self.adjacent_rooms.append(room)
            room.adjacent_rooms.append(self)

    def load_sprite(self, image_path: str):
        """Load sprite for rendering the room."""
        self.sprite = pygame.image.load(image_path).convert_alpha()

    def __str__(self) -> str:
        return f"Room(Enemies: {self.enemy_count}, Danger: {self.danger_level}, Items: {len(self.items)})"


# Area class: Represents a location the ship can dock at, containing rooms
class Area:
    def __init__(self, turns_left_until_unstable: int = 3):
        self.rooms: List[Room] = []  # Rooms in this area
        self.turns_left_until_unstable = turns_left_until_unstable
        # For 2D rendering
        self.background: Optional[pygame.Surface] = None  # Background image for area
        self.position: Optional[tuple] = None  # (x, y) for area on a world map

    def add_room(self, room: Room):
        """Add a room to this area."""
        self.rooms.append(room)

    def decrease_turns(self):
        """Reduce turns until unstable; trigger events if 0."""
        self.turns_left_until_unstable -= 1
        if self.turns_left_until_unstable <= 0:
            print("Warning: Area is now unstable!")  # Placeholder for instability logic

    def load_background(self, image_path: str):
        """Load background image for the area."""
        self.background = pygame.image.load(image_path).convert()

    def __str__(self) -> str:
        return f"Area(Rooms: {len(self.rooms)}, Turns until unstable: {self.turns_left_until_unstable})"


# Ship class: Represents the player's ship with resources and docking state
class Ship:
    def __init__(self):
        self.fuel: int = 5
        self.tools: List[Item] = []  # Tools are items stored on the ship
        self.drones: int = 3
        self.is_docked: bool = False
        self.nanom: int = 100  # Nanomaterial resource
        self.area_docked_at: Optional[Area] = None  # Current docked area
        # For 2D rendering
        self.sprite: Optional[pygame.Surface] = None
        self.position: tuple = (0, 0)  # (x, y) for rendering when not docked

    def dock(self, area: Area):
        """Dock the ship at an area."""
        if not self.is_docked:
            self.is_docked = True
            self.area_docked_at = area
            self.fuel -= 1  # Fuel cost for docking
            print(f"Ship docked at {area}. Fuel remaining: {self.fuel}")

    def undock(self):
        """Undock the ship."""
        if self.is_docked:
            self.is_docked = False
            self.area_docked_at = None
            print("Ship undocked.")

    def add_tool(self, item: Item):
        """Add a tool to the ship's inventory."""
        self.tools.append(item)

    def load_sprite(self, image_path: str):
        """Load sprite for rendering the ship."""
        self.sprite = pygame.image.load(image_path).convert_alpha()

    def __str__(self) -> str:
        return (f"Ship(Fuel: {self.fuel}, Drones: {self.drones}, Nanom: {self.nanom}, "
                f"Tools: {len(self.tools)}, Docked: {self.is_docked})")