#Dungeon Test for AE_Terminus pygame
import pygame
import math
import random
from typing import List, Optional, Tuple

# initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Item:
    def __init__(self, name: str, description: str, count: int):
        self.name = name
        self.description = description
        self.count = count
        self.revealed: bool = False
        # For 2D rendering: Optional sprite and position
        self.sprite: Optional[pygame.Surface] = None
        self.position: Optional[Tuple[int, int]] = None  # (x, y) for rendering in a room

    def __str__(self) -> str:
        return f"{self.name} (x{self.count}): {self.description}"
    
class Dungeon:
    def __init__(self, name: str, description: str, room_count: int = 10):
        self.name = name
        self.description = description
        self.rooms: List[Room] = []  # Rooms in this dungeon
        self.current_room: Optional[Room] = 0  # Current room the player is in
        self.room_count: int  # Total number of rooms in the dungeon

    def add_room(self, room: 'Room'):
        """Add a room to the dungeon."""
        self.rooms.append(room)

    def set_current_room(self, room: 'Room'):
        """Set the current room."""
        self.current_room = room
    
    def Generate(self):
        """Generate rooms and items."""
        for i in range(self.room_count):
            
            if i == 0:
                # First room is the starting point
                # The First room is empty and has no enemies
                # It is special and also has a unique shape that represents the ship
                room = Room(enemy_count=0, danger_level=0)
                
            elif i == self.room_count - 1:
                # Last room is the exit
                room = Room(enemy_count=1, danger_level=5)
            else:
                room = Room(enemy_count=random.randint(0, 5), danger_level=random.randint(1, 5))
            #item = Item(name="Random Item", description="A random item.", count=random.randint(1, 10))
            #room.add_item(item)
            self.add_room(room)

class Room:
    def __init__(self, enemy_count: int = 0, danger_level: int = 1):
        self.items: List[Item] = []  # Items in the room
        self.enemy_count = enemy_count  # Number of enemies
        self.danger_level = danger_level  # Affects difficulty or events
        self.adjacent_rooms: List['Room'] = []  # Connected rooms
        self.doorways_count: int = 1  # Number of doorways in the room
        self.doorways: dict = {"N": -1, "E": -1, "S": -1, "W": -1}  # Dictionary to hold doorways and their room indexes, if -1 then there is no room in that direction
        self.DungPosition: Tuple[float, float] = (0, 0) # not position but instead araingement of the room in the dungeon 
    def add_item(self, item: Item):
        """Add an item to the room."""
        self.items.append(item) # needs to be added in at a random position in the room
        
    

    # def add_adjacent_room(self, room: 'Room'):
    #     """Connect this room to another (bidirectional)."""
    #     if room not in self.adjacent_rooms:
    #         self.adjacent_rooms.append(room)
    #         room.adjacent_rooms.append(self)
            
class Drone:
    def __init__(self):
        self.health: int = 100
        self.tools: List[Item] = []
        self.nanom: int = 50
        self.position: Tuple[float, float] = (0.0, 0.0)
        self.speed: float = 1.0  # Speed of the drone
    
    def update(self, keys):
        #update drone position based on input
        x, y = self.position
        if keys[pygame.K_w]:
            y -= self.speed
        if keys[pygame.K_s]:
            y += self.speed
        if keys[pygame.K_a]:
            x -= self.speed
        if keys[pygame.K_d]:    
            x += self.speed
        x = max(0, min(SCREEN_WIDTH, x))  # Keep within screen bounds
        y = max(0, min(SCREEN_HEIGHT, y))
        self.position = (x, y)
        
    def draw(self, screen):
        # Draw the drone as a circle for simplicity
        pygame.draw.circle(screen, BLUE, (int(self.position[0]), int(self.position[1])), 10)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Drone Dungeon Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    drone = Drone()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        keys = pygame.key.get_pressed()
        drone.update(keys)
        
        # draw everything
        screen.fill(WHITE)
        drone.draw(screen)
        pygame.display.flip()
        clock.tick(60)
           


if __name__ == "__main__":
    main()