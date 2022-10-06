import pygame.image
import pygame.transform


class Settings:
    """ A class to manage the game settings"""

    def __init__(
        self
    ):
        # Initialize the game's static settings

        # Color
        self.lime_soup = (123, 237, 159)
        self.electron_blue = (9, 132, 227)
        self.light_greenish_blue = (85, 239, 196)
        self.lynx_white = (245, 246, 250)

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 620
        self.fps = 90
        self.caption = "Alien invasion"

        # Files
        self.screen_bg = pygame.transform.scale(
            pygame.image.load("../assets/img/bg.png"),
            (1300, 700)
        )
        self.icon = pygame.image.load("../assets/img/logo-2.png")
        self.shoot_sound = pygame.mixer.Sound("../assets/sound/Gun+Silencer.mp3")
        self.hit_sound = pygame.mixer.Sound("../assets/sound/Grenade+1.mp3")
        self.big_bomb = pygame.mixer.Sound("../assets/sound/bigbomb.wav")
        self.state_font = pygame.font.Font("../assets/Font/Flappy.TTF", 32)
        self.btn_font = pygame.font.Font("../assets/Font/Flappy.TTF", 48)

        # Spaceship
        self.ship_width = 50
        self.ship_height = 50
        self.ship_limit = 3

        # Bullets
        self.bullet_width = 30
        self.bullet_height = 4
        self.bullets_allowed = 4

        # Buttons
        self.btn_width = 230
        self.btn_height = 100
        self.btn_msg = "Play"

        # Aliens
        self.fleet_drop_speed = 5

        # How quickly the game speed up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # How quickly the aliens point values increase
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """ Initialize the settings that change through the game"""
        self.ship_speed = 5
        self.alien_speed = 3
        self.bullets_speed = 10

        self.fleet_direction = 1

        # Scoring
        self.alien_point = 10

    def increase_speed(self):
        """ Increase speed settings and alien point value """
        self.ship_speed *= self.speedup_scale
        self.bullets_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)
