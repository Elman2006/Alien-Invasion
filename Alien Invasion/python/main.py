# ========================================== Modules =============================================
# ------------------------------------ Open modules --------------------------------------------
import pygame
from pygame.sprite import Group
# ------------------------------------ My modules ---------------------------------------------
from settings import Settings
import game_functions as gf
from ship import Ship
from game_states import GameStates
from button import Button
from score_board import ScoreBoard
# ========================================== Infinity loop ============================================


def run_game():
    # initialize
    pygame.init()

    # Create objects
    ai_settings = Settings()
    info_object = pygame.display.Info()
    screen = pygame.display.set_mode((info_object.current_w, ai_settings.screen_height), pygame.RESIZABLE)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    states = GameStates(ai_settings)
    play_btn = Button(ai_settings, screen)
    sb = ScoreBoard(ai_settings, screen, states)
    clock = pygame.time.Clock()
    gf.create_fleet(ai_settings, aliens, screen, ship)

    while True:
        """ An infinity loop for updating the screen. """

        # Set the FPS
        clock.tick(ai_settings.fps)

        gf.check_events(
            ai_settings,
            aliens,
            bullets,
            play_btn,
            sb,
            screen,
            ship,
            states
        )

        if states.game_active:
            gf.update_aliens(
                ai_settings,
                aliens,
                bullets,
                sb,
                screen,
                ship,
                states
            )

            gf.update_bullets(
                ai_settings,
                aliens,
                bullets,
                sb,
                screen,
                ship,
                states
            )

            ship.update_ship()

        gf.update_screen(
            ai_settings,
            aliens,
            bullets,
            play_btn,
            sb,
            screen,
            ship,
            states
        )


# ======================================== Call the start function =========================================
run_game()
