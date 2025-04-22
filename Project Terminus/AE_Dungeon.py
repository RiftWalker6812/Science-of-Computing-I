import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1536  # 1250 (dungeon) + 286 (UI)
SCREEN_HEIGHT = 864
GRID_SIZE = 20  # 20x20 grid
ROOM_SIZE = 250
DUNGEON_WIDTH = GRID_SIZE * ROOM_SIZE  # 5000 pixels
UI_WIDTH = 286  # Fixed UI width
ROOM_COUNT = 10
DOOR_WIDTH = 20
DOOR_HEIGHT = 10

# Colors
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Game")
font = pygame.font.SysFont("arial", 24)

class Room:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * ROOM_SIZE, grid_y * ROOM_SIZE, ROOM_SIZE, ROOM_SIZE)
        self.doors = {"north": False, "south": False, "east": False, "west": False}
        self.id = None

    def get_door_rects(self):
        """Return rectangles for door placeholders."""
        door_rects = []
        if self.doors["north"]:
            door_rects.append(pygame.Rect(
                self.rect.centerx - DOOR_WIDTH // 2, self.rect.top - DOOR_HEIGHT // 2,
                DOOR_WIDTH, DOOR_HEIGHT
            ))
        if self.doors["south"]:
            door_rects.append(pygame.Rect(
                self.rect.centerx - DOOR_WIDTH // 2, self.rect.bottom - DOOR_HEIGHT // 2,
                DOOR_WIDTH, DOOR_HEIGHT
            ))
        if self.doors["east"]:
            door_rects.append(pygame.Rect(
                self.rect.right - DOOR_HEIGHT // 2, self.rect.centery - DOOR_WIDTH // 2,
                DOOR_HEIGHT, DOOR_WIDTH
            ))
        if self.doors["west"]:
            door_rects.append(pygame.Rect(
                self.rect.left - DOOR_HEIGHT // 2, self.rect.centery - DOOR_WIDTH // 2,
                DOOR_HEIGHT, DOOR_WIDTH
            ))
        return door_rects

class Dungeon:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.rooms = []
        self.generate_dungeon()

    def generate_dungeon(self):
        # Start at left-center (grid_x=0, grid_y=10)
        start_x, start_y = 0, GRID_SIZE // 2
        start_room = Room(start_x, start_y)
        start_room.id = 1
        self.grid[start_y][start_x] = start_room
        self.rooms.append(start_room)

        available = [(start_x, start_y)]
        room_id = 2
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
            new_room.id = room_id
            new_room.doors[{"north": "south", "south": "north", "east": "west", "west": "east"}[direction]] = True
            self.grid[new_y][new_x] = new_room
            self.rooms.append(new_room)
            available.append((new_x, new_y))
            room_id += 1

    def draw(self, screen, player_room, camera_offset):
        for room in self.rooms:
            offset_rect = room.rect.move(camera_offset)
            if offset_rect.colliderect((0, 0, SCREEN_WIDTH - UI_WIDTH, SCREEN_HEIGHT)):
                color = RED if room == player_room else GRAY
                pygame.draw.rect(screen, color, offset_rect)
                pygame.draw.rect(screen, BLACK, offset_rect, 4)  # 4-pixel thick walls
                for door_rect in room.get_door_rects():
                    offset_door = door_rect.move(camera_offset)
                    if offset_door.colliderect((0, 0, SCREEN_WIDTH - UI_WIDTH, SCREEN_HEIGHT)):
                        pygame.draw.rect(screen, WHITE, offset_door)
                text = font.render(str(room.id), True, WHITE)
                screen.blit(text, (offset_rect.centerx - 10, offset_rect.centery - 10))

class Player:
    def __init__(self, dungeon):
        self.current_room = dungeon.rooms[0]

    def move(self, direction):
        new_x, new_y = self.current_room.grid_x, self.current_room.grid_y
        if direction == "north" and self.current_room.doors["north"]:
            new_y -= 1
        elif direction == "south" and self.current_room.doors["south"]:
            new_y += 1
        elif direction == "east" and self.current_room.doors["east"]:
            new_x += 1
        elif direction == "west" and self.current_room.doors["west"]:
            new_x -= 1
        else:
            print(f"No door to the {direction}")
            return False

        new_room = dungeon.grid[new_y][new_x]
        if new_room:
            self.current_room = new_room
            print(f"Moved to Room {new_room.id}")
            return True
        print(f"No room to the {direction}")
        return False

class Camera:
    def __init__(self):
        self.offset = [0, 0]
        self.screen_width = SCREEN_WIDTH - UI_WIDTH  # Dungeon viewport width
        self.screen_height = SCREEN_HEIGHT  # Dungeon viewport height

    def update(self, player_room):
        # Center the room exactly in the viewport, no clamping to grid edges
        target_x = -player_room.rect.centerx + self.screen_width // 2
        target_y = -player_room.rect.centery + self.screen_height // 2
        self.offset = [target_x, target_y]

class UI:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH - UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)
        self.buttons = {
            "north": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 300, 120, 50),
            "south": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 150, 300, 120, 50),
            "east": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 360, 120, 50),
            "west": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 150, 360, 120, 50),
            "scan": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 420, 250, 50)
        }

    def draw(self, screen, player):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        for i in range(3):
            text = font.render(f"Member {i+1}: HP 100", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 20 + i * 40))

        for direction, rect in self.buttons.items():
            enabled = direction != "scan" and player.current_room.doors.get(direction, False)
            color = WHITE if enabled or direction == "scan" else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text = font.render(direction.capitalize(), True, BLACK)
            screen.blit(text, (rect.x + 10, rect.y + 15))

        text = font.render("Inventory", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 600))

    def handle_click(self, pos, player):
        for direction, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if direction == "scan":
                    print("Scan Room clicked (placeholder)")
                elif player.move(direction):
                    return True
        return False

# Main game
dungeon = Dungeon()
player = Player(dungeon)
ui = UI()
camera = Camera()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ui.handle_click(event.pos, player)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                player.move("north")
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                player.move("south")
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                player.move("east")
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                player.move("west")

    camera.update(player.current_room)
    screen.fill(CYAN)
    dungeon.draw(screen, player.current_room, camera.offset)
    ui.draw(screen, player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()