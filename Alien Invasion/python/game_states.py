class GameStates:
    """ Track statics for Alien Invasion """

    def __init__(
            self,
            ai_settings
    ):
        """Initialize statics"""
        self.ai_settings = ai_settings
        self.reset_states()

        # Start "Alien invasion" in active state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0

    def reset_states(self):
        """ Initialize statics that can change during the game """
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
