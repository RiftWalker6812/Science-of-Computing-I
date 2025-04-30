import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1536  # 1250 (dungeon) + 286 (UI)
SCREEN_HEIGHT = 864
GRID_SIZE = 5  # 5x5 grid
ROOM_SIZE = 150
DUNGEON_WIDTH = GRID_SIZE * ROOM_SIZE  # 750 pixels
UI_WIDTH = 286
ROOM_COUNT = 10  # Increased to 10 rooms
DOOR_SIZE = 12
STARSHIP_SIZE = 30

# Colors
STARRY_BLUE = (10, 20, 50)
SILVER = (200, 200, 200)
BLUE = (50, 100, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Pagoda")
font = pygame.font.SysFont("arial", 24)

# Room Descriptions Dictionary
ROOM_DESCRIPTIONS = {
    "pagoda_wooden": ["Pagoda Style", "The floors are woody, polished to a mirror sheen, reflecting cyan lights."],
    "quantum_vault": ["Quantum Vault", "Metallic walls pulse with unstable energy, humming softly."],
    "starlit_chamber": ["Starlit Chamber", "A domed ceiling reveals a starry void, serene yet unsettling."],
    "mirror_hall": ["Mirror Hall", "Mirrored walls create infinite reflections, distorting reality."],
    "core_sanctum": ["Core Sanctum", "A white platform glows faintly, the heart of the pagoda’s anomaly."]
}

# Item Class
class Item:
    def __init__(self, name: str, unrevealed_name, description, unrevealed_description, revealed=False):
        self.name = name
        self.unrevealed_name = unrevealed_name
        self.description = description
        self.unrevealed_description = unrevealed_description
        self.revealed = revealed

# Global Items Dictionary with Item instances
ITEMS = {
    "quantum_crystal": Item(
        name="Quantum Crystal",
        unrevealed_name="Glowing Shard",
        description="A pulsating crystal containing 1 unit of Quantium.",
        unrevealed_description="A mysterious shard emitting faint light.",
        revealed=False
    ),
    "nano_repair_kit": Item(
        name="Nano Repair Kit",
        unrevealed_name="Strange Device",
        description="Restores 20 HP to the droid.",
        unrevealed_description="A compact device with unknown function.",
        revealed=False
    ),
    "quantum_disruptor": Item(
        name="Quantum Disruptor",
        unrevealed_name="Odd Gadget",
        description="Deals 10 extra damage to Einstein-Entities.",
        unrevealed_description="A peculiar gadget with erratic energy.",
        revealed=False
    )
}

class Room:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * ROOM_SIZE, grid_y * ROOM_SIZE, ROOM_SIZE, ROOM_SIZE)
        self.doors = {"north": False, "south": False, "east": False, "west": False}
        self.items = random.sample(list(ITEMS.values()), k=random.randint(0, 3))
        self.starship = grid_x == 0 and grid_y == 2
        # Assign room description
        if grid_x == 0 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["starlit_chamber"]
        elif grid_x == 2 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["core_sanctum"]
        else:
            self.description = random.choice(list(ROOM_DESCRIPTIONS.values()))

    def get_door_rects(self):
        door_rects = []
        if self.doors["north"]:
            door_rects.append(pygame.Rect(
                self.rect.centerx - DOOR_SIZE // 2, self.rect.top - DOOR_SIZE // 2,
                DOOR_SIZE, DOOR_SIZE
            ))
        if self.doors["south"]:
            door_rects.append(pygame.Rect(
                self.rect.centerx - DOOR_SIZE // 2, self.rect.bottom - DOOR_SIZE // 2,
                DOOR_SIZE, DOOR_SIZE
            ))
        if self.doors["east"]:
            door_rects.append(pygame.Rect(
                self.rect.right - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                DOOR_SIZE, DOOR_SIZE
            ))
        if self.doors["west"]:
            door_rects.append(pygame.Rect(
                self.rect.left - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                DOOR_SIZE, DOOR_SIZE
            ))
        return door_rects

class Dungeon:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.rooms = []
        self.generate_dungeon()

    def generate_dungeon(self):
        start_x, start_y = 0, 2  # Starting room
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

class Player:
    def __init__(self, dungeon):
        self.current_room = dungeon.rooms[0]
        self.hp = 50
        self.quantium = 0
        self.inventory = []

    def move(self, direction, popup):
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
            print(f"No portal to the {direction}")
            return False

        new_room = dungeon.grid[new_y][new_x]
        if new_room:
            self.current_room = new_room
            print(f"Moved to Room at ({new_room.grid_x}, {new_room.grid_y})")
            # Show room description popup
            popup.show(["Room Entry", new_room.description[0], new_room.description[1]])
            return True
        print(f"No room to the {direction}")
        return False

class UI:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH - UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)
        self.buttons = {
            "north": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 200, 120, 50),
            "south": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 150, 200, 120, 50),
            "east": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 260, 120, 50),
            "west": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 150, 260, 120, 50),
            "scan": pygame.Rect(SCREEN_WIDTH - UI_WIDTH + 20, 320, 250, 50)
        }

    def draw(self, screen, player):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text = font.render(f"Droid-E002: HP {player.hp}/50", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 20))
        text = font.render(f"Quantium: {player.quantium}/20", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 60))

        for direction, rect in self.buttons.items():
            enabled = direction != "scan" and player.current_room.doors.get(direction, False)
            color = WHITE if enabled or direction == "scan" else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text = font.render(direction.capitalize(), True, BLACK)
            screen.blit(text, (rect.x + 10, rect.y + 15))

        text = font.render("Inventory", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 400))
        for i, [item, quantity] in enumerate(player.inventory):
            name = item.name if item.revealed else item.unrevealed_name
            text = font.render(f"{name}: {quantity}", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - UI_WIDTH + 20, 430 + i * 30))

    def handle_click(self, pos, player, popup):
        for direction, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if direction == "scan":
                    text = ["Quantum Scan Results:"]
                    if player.current_room.items:
                        text.append("Items: " + ", ".join(item.unrevealed_name for item in player.current_room.items))
                        for item in player.current_room.items:
                            item.revealed = True
                            for inv_item, qty in player.inventory:
                                if inv_item.name == item.name:
                                    qty += 1
                                    break
                            else:
                                player.inventory.append([item, 1])
                            if item.name == "Quantum Crystal":
                                player.quantium += 1
                            print(f"Collected {item.name}")
                        player.current_room.items = []
                    else:
                        text.append("No items found.")
                    popup.show(text)
                elif player.move(direction, popup):
                    return True
        return False

class Popup:
    def __init__(self):
        self.active = False
        self.text = []
        self.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.close_button = pygame.Rect(self.rect.right - 60, self.rect.bottom - 40, 50, 30)

    def show(self, text):
        self.active = True
        self.text = text if isinstance(text, list) else [text]

    def draw(self, screen):
        if not self.active:
            return
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        for i, line in enumerate(self.text):
            text = font.render(line, True, WHITE)
            screen.blit(text, (self.rect.x + 20, self.rect.y + 20 + i * 30))
        pygame.draw.rect(screen, WHITE, self.close_button)
        text = font.render("Close", True, BLACK)
        screen.blit(text, (self.close_button.x + 5, self.close_button.y + 5))

    def handle_click(self, pos):
        if self.active and self.close_button.collidepoint(pos):
            self.active = False
            return True
        return False

# Main game
dungeon = Dungeon()
player = Player(dungeon)
ui = UI()
popup = Popup()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not popup.handle_click(event.pos):
                ui.handle_click(event.pos, player, popup)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and popup.active:
                popup.active = False

    screen.fill(STARRY_BLUE)
    offset = (250, 57)
    for room in dungeon.rooms:
        offset_rect = room.rect.move(offset)
        color = BLUE if room == player.current_room else SILVER
        pygame.draw.rect(screen, color, offset_rect)
        pygame.draw.rect(screen, CYAN, offset_rect, 4)
        for door_rect in room.get_door_rects():
            offset_door = door_rect.move(offset)
            pygame.draw.rect(screen, WHITE, offset_door)
        if room.starship:
            starship_rect = pygame.Rect(offset_rect.x + 10, offset_rect.y + 60, STARSHIP_SIZE, STARSHIP_SIZE)
            pygame.draw.rect(screen, GREEN, starship_rect)

    ui.draw(screen, player)
    popup.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()