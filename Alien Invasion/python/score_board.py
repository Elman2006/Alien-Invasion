from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """ A class to report scoring information"""

    def __init__(
            self,
            ai_settings,
            screen,
            states
    ):
        """ initialize score keeping attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.states = states

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    # ----------------------------------------------- Score --------------------------------------
    def prep_score(self):
        """ Turn the score to a rendered image """
        round_score = int(self.states.score)
        score_str = f"Score: {round_score:,}"
        self.score_img = self.ai_settings.state_font.render(
            score_str,
            True,
            self.ai_settings.lynx_white
        )

        # Display the score at the top-left of the screen
        self.score_rect = self.score_img.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.bottom = self.screen_rect.bottom - 20

    # ----------------------------------------- HighScore ------------------------------------------
    def prep_high_score(self):
        """ Turn the high score into a rendered image. """
        high_score = int(self.states.high_score)
        high_score_str = "High Score: {:,}".format(high_score)

        self.high_score_image = self.ai_settings.state_font.render(
            high_score_str,
            True,
            self.ai_settings.lynx_white
        )

        # Display the score at the top-left of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    # ====================================== Level ===================================================
    def prep_level(self):
        """ Turn the level into a rendered image. """
        self.level_img = self.ai_settings.state_font.render(
            f"level: {self.states.level}",
            True,
            self.ai_settings.lynx_white
        )

        # Position the level below the score
        self.level_rect = self.level_img.get_rect()
        self.level_rect.centery = self.screen_rect.centery
        self.level_rect.left = self.level_rect.left + 20

    # ====================================== Ships ==================================
    def prep_ships(self):
        """ Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.states.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10
            ship.rect.y = 10 + ship_number * ship.rect.height
            self.ships.add(ship)

    # ===================================== Draw ======================================
    def show_states(self):
        """ Draw score to the screen"""

        # Score
        self.screen.blit(
            self.score_img,
            self.score_rect
        )

        # High score
        self.screen.blit(
            self.high_score_image,
            self.high_score_rect
        )

        # Level
        self.screen.blit(
            self.level_img,
            self.level_rect
        )

        # Ships
        self.ships.draw(self.screen)
