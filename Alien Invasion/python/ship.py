# ========================================== Modules =============================================
# ------------------------------------ Open modules --------------------------------------------
import pygame
from pygame.sprite import Sprite


# ====================================== Ship class ===============================================
class Ship(Sprite):
    """ A class to creat a ship object """

    def __init__(
            self,
            ai_settings,
            screen
    ):
        """ Initialize the ship and set its starting position. """
        super(Ship, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("../assets/img/space-ship.png"), (50, 50)
            ), -90
        )
        self.rect = self.image.get_rect()

        # Start each new ship in the left-center of the screen
        self.rect.right = self.screen_rect.right - 5
        self.rect.centery = self.screen_rect.centery

        # Spaceship movement
        self.move_up = False
        self.move_down = False

    def update_ship(self):
        """ Move the spaceship by pressing keyboard"""

        # Move up
        if self.move_up and self.rect.top > self.screen_rect.top + 5:
            self.rect.y -= self.ai_settings.ship_speed

        # Move down
        elif self.move_down and self.rect.bottom < self.screen_rect.bottom - 5:
            self.rect.y += self.ai_settings.ship_speed

    def center_ship(self):
        """ Center the ship on the screen """
        self.center = self.screen_rect.centerx

    def blit_ship(self):
        """ Draw the ship at it current position"""
        self.screen.blit(
            self.image,
            self.rect
        )
