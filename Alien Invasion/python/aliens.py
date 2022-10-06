# ========================================== Modules =============================================
# ------------------------------------ Open modules --------------------------------------------
import pygame
from pygame.sprite import Sprite


# ====================================== aliens class ===============================================
class Aliens(Sprite):
    """ A class to represent a single alien in the fleet"""

    def __init__(
            self,
            ai_settings,
            screen,
    ):
        """ Initialize the alien and set its starting position"""
        super(Aliens, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("../assets/img/blue.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.y = float(self.rect.y)

    def check_edge(self):
        """ Return true ir alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.bottom >= screen_rect.bottom:
            return True

        elif self.rect.top <= 41:
            return True

    def update(self):
        """ Move the aliens to down. """
        self.y += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
        self.rect.y = self.y

    def blit_alien(self):
        """ Draw the alien at its current location """
        self.screen.blit(
            self.image,
            self.rect
        )
