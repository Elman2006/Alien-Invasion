# ========================================== Modules =============================================
# ------------------------------------ Open modules --------------------------------------------
import pygame
from pygame.sprite import Sprite


# ====================================== bullets class ===============================================
class Bullets(Sprite):
    """ A class to manage bullets fired from the ship."""

    def __init__(
            self,
            ai_settings,
            screen,
            ship
    ):
        """ Creat the bullet object and ship current position"""
        super(Bullets, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Creat a bullet rect at (0, 0) and then set current position.
        self.rect = pygame.Rect(
            0,
            0,
            ai_settings.bullet_width,
            ai_settings.bullet_height
        )
        self.rect.midleft = ship.rect.midleft

        # Store the bullet's position as a decimal value
        self.bullet_x = float(self.rect.x)

    def update_bullet_position(self):
        """ Move the bullet right to the screen """
        # Update the decimal position of the bullet
        self.bullet_x -= self.ai_settings.bullets_speed

        # Update the rect position
        self.rect.x = self.bullet_x

    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        pygame.draw.rect(
            self.screen,
            self.ai_settings.lime_soup,
            self.rect
        )
