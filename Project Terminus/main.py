import pygame
import os
from constants import *
from entities import *
from dungeon import *
from player import *
from ui import *

# Initialize Pygame
pygame.init()

# Load sci-fi font (Orbitron, fallback to Arial)
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, "ASSETS", "orbitron.ttf")
try:
    font = pygame.font.Font(font_path, 24)
    font_small = pygame.font.Font(font_path, 18)
    font_large = pygame.font.Font(font_path, 28)
except FileNotFoundError:
    print(f"Error: Could not find '{font_path}'. Falling back to Arial.")
    font = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)
    font_large = pygame.font.SysFont("arial", 28)

# Load starship sprite
sprite_path = os.path.join(script_dir, "ASSETS", "prufer.png")
try:
    starship_sprite = pygame.image.load(sprite_path).convert_alpha()
    starship_sprite = pygame.transform.scale(starship_sprite, (STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE))
except FileNotFoundError:
    print(f"Error: Could not find '{sprite_path}'. Using placeholder.")
    starship_sprite = pygame.Surface((STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE), pygame.SRCALPHA)
    for x in range(STARSHIP_SPRITE_SIZE):
        for y in range(STARSHIP_SPRITE_SIZE):
            color = CYAN if (x + y) % 2 == 0 else WHITE
            starship_sprite.set_at((x, y), color)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Pagoda")

# Main game
dungeon = Dungeon()
player = Player(dungeon)
left_ui = LeftUI()
right_ui = RightUI()
popup = Popup()
clock = pygame.time.Clock()
running = True

# Removed popup.show() for initial room entry
dungeon.visited.add((0, 2))

while running:
    delta_time = clock.get_time() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if popup.active and not popup.rect.collidepoint(event.pos):
                continue
            if popup.handle_click(event.pos, player, player.current_room):
                if popup.game_over:
                    running = False
                continue
            if left_ui.handle_click(event.pos, player, player.current_room):
                continue
            if right_ui.handle_click(event.pos, player, popup):
                if player.current_room.grid_x == 0 and player.current_room.grid_y == 2 and player.quanta >= 10:
                    running = False
                continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and popup.active and not popup.combat_mode:
                popup.active = False
        elif event.type in (pygame.MOUSEWHEEL, pygame.MOUSEMOTION):
            popup.handle_event(event)

    screen.fill(STARRY_BLUE)
    left_ui.draw(screen, player.current_room)
    offset = (573, 57)
    for room in dungeon.rooms:
        offset_rect = room.rect.move(offset)
        if (room.grid_x, room.grid_y) in dungeon.visited:
            color = GREEN if room == player.current_room else SILVER
        else:
            color = GRAY
        pygame.draw.rect(screen, color, offset_rect)
        pygame.draw.rect(screen, CYAN, offset_rect, 4)
        for door_rect in room.get_door_rects():
            offset_door = door_rect.move(offset)
            pygame.draw.rect(screen, WHITE, offset_door)
    starship_pos = (573 - STARSHIP_SPRITE_SIZE, 357 + ROOM_SIZE//2 - STARSHIP_SPRITE_SIZE//2)
    screen.blit(starship_sprite, starship_pos)
    right_ui.draw(screen, player)
    popup.draw(screen, delta_time)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()