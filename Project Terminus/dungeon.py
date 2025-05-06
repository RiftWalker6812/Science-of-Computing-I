import random
import pygame
from constants import ROOM_SIZE, GRID_SIZE, DOOR_SIZE

class Room:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * ROOM_SIZE, grid_y * ROOM_SIZE, ROOM_SIZE, ROOM_SIZE)
        self.doors = {"north": False, "south": False, "east": False, "west": False}
        self.items = random.sample(list(ITEMS.values()), k=random.randint(0, 3))
        self.entity = None
        self.does_have_sleeping_entity = False
        self.scanned = False
        if grid_x == 0 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["starlit_chamber"]
        elif grid_x == 2 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["core_sanctum"]
        else:
            self.description = random.choice(list(ROOM_DESCRIPTIONS.values()))

    def get_door_rects(self):
        door_rects = []
        for direction in ["north", "south", "east", "west"]:
            if self.doors[direction]:
                if direction == "north":
                    door_rects.append(pygame.Rect(
                        self.rect.centerx - DOOR_SIZE // 2, self.rect.top - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "south":
                    door_rects.append(pygame.Rect(
                        self.rect.centerx - DOOR_SIZE // 2, self.rect.bottom - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "east":
                    door_rects.append(pygame.Rect(
                        self.rect.right - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "west":
                    door_rects.append(pygame.Rect(
                        self.rect.left - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
        return door_rects

class Dungeon:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.rooms = []
        self.visited = set()
        self.generate_dungeon()

    def generate_dungeon(self):
        start_x, start_y = 0, 2
        start_room = Room(start_x, start_y)
        self.grid[start_y][start_x] = start_room
        self.rooms.append(start_room)
        available = [(start_x, start_y)]

        while len(self.rooms) < ROOM_COUNT and available:
            curr_x, curr_y = random.choice(available)
            curr_room = self.grid[curr_y][curr_x]

            directions = []
            if curr_y > 0 and not self.grid[curr_y - 1][curr_x]:
                directions.append("north")
            if curr_y < GRID_SIZE - 1 and not self.grid[curr_y + 1][curr_x]:
                directions.append("south")
            if curr_x < GRID_SIZE - 1 and not self.grid[curr_y][curr_x + 1]:
                directions.append("east")
            if curr_x > 0 and not self.grid[curr_y][curr_x - 1]:
                directions.append("west")

            if not directions:
                available.remove((curr_x, curr_y))
                continue

            direction = random.choice(directions)
            new_x, new_y = curr_x, curr_y
            if direction == "north":
                new_y -= 1
                curr_room.doors["north"] = True
            elif direction == "south":
                new_y += 1
                curr_room.doors["south"] = True
            elif direction == "east":
                new_x += 1
                curr_room.doors["east"] = True
            elif direction == "west":
                new_x -= 1
                curr_room.doors["west"] = True

            new_room = Room(new_x, new_y)
            new_room.doors[{"north": "south", "south": "north", "east": "west", "west": "east"}[direction]] = True
            self.grid[new_y][new_x] = new_room
            self.rooms.append(new_room)
            available.append((new_x, new_y))

            if (new_x, new_y) != (0, 2) and random.random() < 0.1:
                new_room.entity = random.choice(list(EE_ENTITIES.values()))