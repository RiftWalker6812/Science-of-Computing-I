import pygame
import math
import random
from typing import List, Optional, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
AREA_SIZE = 100
SHIP_SIZE = 20
FUEL_CONSUMPTION = 0.01  # Fuel used per frame when moving
STAR_COUNT = 50  # For starry background

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

    def __str__(self) -> str:
        return f"{self.name} (x{self.count}): {self.description}"

class Ship:
    def __init__(self, x: int, y: int):
        self.fuel: float = 50.0
        self.tools: List[Item] = []
        self.drones: int = 3
        self.nanom: int = 100
        self.x, self.y = float(x), float(y)  # Precise position
        self.angle: float = 0.0  # Facing direction in degrees
        self.velocity: Tuple[float, float] = (0.0, 0.0)  # (vx, vy)
        self.rect = pygame.Rect(int(x), int(y), SHIP_SIZE, SHIP_SIZE)
        self.thrust: float = 0.1  # Acceleration per frame
        self.max_speed: float = 5.0
        self.rotation_speed: float = 3.0  # Degrees per frame

    def update(self, moving: bool):
        """Update position, velocity, and fuel."""
        if moving and self.fuel > 0:
            rad = math.radians(self.angle)
            self.velocity = (
                self.velocity[0] + math.cos(rad) * self.thrust,
                self.velocity[1] + math.sin(rad) * self.thrust
            )
            self.fuel -= FUEL_CONSUMPTION
            if self.fuel <= 0:
                print("Out of fuel!")
                self.fuel = 0

        # Cap speed
        speed = math.hypot(*self.velocity)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity = (self.velocity[0] * scale, self.velocity[1] * scale)

        # Update position
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.x = max(SHIP_SIZE / 2, min(self.x, SCREEN_WIDTH - SHIP_SIZE / 2))
        self.y = max(SHIP_SIZE / 2, min(self.y, SCREEN_HEIGHT - SHIP_SIZE / 2))
        self.rect.center = (int(self.x), int(self.y))

        # Apply drag
        self.velocity = (self.velocity[0] * 0.98, self.velocity[1] * 0.98)

    def rotate(self, direction: str):
        """Rotate left or right."""
        if direction == "left":
            self.angle -= self.rotation_speed
        elif direction == "right":
            self.angle += self.rotation_speed
        self.angle %= 360

class Camera:
    def __int__(self):
        self.x = 0.0
        self.y = 0.0
         


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sunless Skies-Inspired Game - Ship Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
 # Create ship
    ship = Ship(150, 150)  # Start near Area Zero
    
    # create camera 
    camera = Camera()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_UP]:
            moving = True
        if keys[pygame.K_LEFT]:
            ship.rotate("left")
        if keys[pygame.K_RIGHT]:
            ship.rotate("right")
        """ if keys[pygame.K_s] and ship.rect.colliderect(area_zero.rect):
            if area_zero.shop_items:
                # Buy first item (Fuel Can) for now
                ship.buy_item(area_zero.shop_items[0], cost=20) """
                
# Update
        ship.update(moving)

        # Draw
        screen.fill(BLACK)
        # Draw stars
        # for star in stars:
        #     pygame.draw.circle(screen, WHITE, star, 1)
        # Draw Area Zero
        #pygame.draw.rect(screen, GREEN, area_zero.rect)
        # Draw ship (rotated rectangle)
        ship_surface = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(ship_surface, BLUE, (0, 0, SHIP_SIZE, SHIP_SIZE))
        rotated_ship = pygame.transform.rotate(ship_surface, -ship.angle)
        rotated_rect = rotated_ship.get_rect(center=ship.rect.center)
        screen.blit(rotated_ship, rotated_rect)

        # Draw HUD
        hud = [
            f"Fuel: {ship.fuel:.1f}",
            f"Drones: {ship.drones}",
            f"Nanom: {ship.nanom}"
        ]
        for i, line in enumerate(hud):
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()