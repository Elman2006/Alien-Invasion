# ======================================== Modules ==================================================
# ---------------------------------------- Open Modules --------------------------------------------
import pygame
from sys import exit
from time import sleep

# ---------------------------------------- My modules ------------------------------------------------
from bullet import Bullets
from aliens import Aliens


# ========================================== Events =====================================================
def check_keyup(
        event,
        ship
):
    """ Respond to un press the key"""
    # ******************************* Spaceship movement ****************************************
    # Move up
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.move_up = False

    # Moe down
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.move_down = False


def check_keydown(
        ai_settings,
        bullets,
        event,
        screen,
        ship
):
    """ To check key presses in keyboard"""

    # Exit from the game
    if event.key == pygame.K_ESCAPE:
        exit()

    # **************************** Spaceship movement **********************************
    # Move up
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.move_up = True

    # Move down
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.move_down = True

    # **************************** Fire bullets *************************************
    elif event.key == pygame.K_RCTRL or event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bullets, screen, ship)


def check_events(
    ai_settings,
    aliens,
    bullets,
    play_btn,
    sb,
    screen,
    ship,
    states
):
    """ Check for events """
    for event in pygame.event.get():

        # Exit from the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Fix screen
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h))

        # Check for mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_btn(
                ai_settings,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
                play_btn,
                sb,
                screen,
                ship,
                states
            )

        # Check for key presses
        elif event.type == pygame.KEYDOWN:
            check_keydown(
                ai_settings,
                bullets,
                event,
                screen,
                ship
            )

        # Check for key up
        elif event.type == pygame.KEYUP:
            check_keyup(
                event,
                ship
            )


# ========================================= Collides ================================================
def check_play_btn(
        ai_settings,
        aliens,
        bullets,
        mouse_x,
        mouse_y,
        play_btn,
        sb,
        screen,
        ship,
        states
):
    """ Start a new game when player clicked 'Play' """
    btn_clicked = play_btn.rect.collidepoint(mouse_x, mouse_y)
    if btn_clicked and not states.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide mouse curser
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        states.reset_states()
        states.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(
            ai_settings,
            aliens,
            screen,
            ship,
        )
        ship.center_ship()


def check_bullet_alien_collision(
        ai_settings,
        aliens,
        bullets,
        sb,
        screen,
        ship,
        states,
):
    """ Respond to bullet-alien collision """
    # Remove any bullets and aliens that have collided

    # Check for any bullets that hit the aliens
    # If so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        ai_settings.hit_sound.play()

        for aliens in collisions.values():
            states.score += ai_settings.alien_point * len(aliens)
        sb.prep_score()

        check_high_score(sb, states)

    if len(aliens) == 0:
        # Destroy existing bullets, speedup the game and create new fleet.
        bullets.empty()

        # Increase level
        states.level += 1
        sb.prep_level()

        ai_settings.increase_speed()
        create_fleet(ai_settings, aliens, screen, ship)


def game_over(
        ai_settings,
        aliens,
        bullets,
        sb,
        screen,
        ship,
        states
):
    """ Respond to alien-ship collision """
    if states.ship_left > 0:

        # Play sound
        ai_settings.big_bomb.play()

        # Decrement ship hit
        states.ship_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create the new fleet and center the ship
        create_fleet(ai_settings, aliens, screen, ship)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        pygame.mouse.set_visible(True)
        states.game_active = False


def check_alien_right(
        ai_settings,
        aliens,
        bullets,
        sb,
        screen,
        ship,
        states
):
    """ Check if any aliens have reached the right of screen"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.right >= screen_rect.right - ship.rect.width:

            # game over
            game_over(ai_settings, aliens, bullets, sb, screen, ship, states)

            break


# ========================================== Score board ====================================
def check_high_score(
        sb,
        states
):
    """ Check to see if there's a new high score"""
    if states.score >= states.high_score:
        states.high_score = states.score
        sb.prep_high_score()


# ========================================= Bullets ====================================================
def fire_bullet(
        ai_settings,
        bullets,
        screen,
        ship
):
    """ Fire a bullet if limit not reached yet. """
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullets(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ai_settings.shoot_sound.play()


def update_bullets(
        ai_settings,
        aliens,
        bullets,
        sb,
        screen,
        ship,
        states
):
    """ Update position of bullets and get rid of old bullets"""
    # Update bullet position
    bullets.update()
    for bullet in bullets:
        if bullet.rect.right <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, aliens, bullets, sb, screen, ship, states)


# ========================================== Aliens ======================================================
def get_number_alien_y(
        ai_settings,
        alien_width
):
    """ Determine the number if aliens that fir in a column"""
    available_space_y = ai_settings.screen_height - 2 * alien_width
    number_aliens_y = int(available_space_y / (2 * alien_width))
    return number_aliens_y


def create_alien(
        ai_settings,
        aliens,
        alien_number,
        column_number,
        screen,
):
    """ Create an alien and place it in the row"""
    alien = Aliens(ai_settings, screen)
    alien_height = alien.rect.height
    alien.y = alien_height + 2 * alien_height * alien_number
    alien.rect.y = alien.y
    alien.rect.x = alien.rect.width + 2 * alien.rect.width * column_number
    aliens.add(alien)


def get_number_columns(
        ai_settings,
        alien_width,
        ship_width
):
    """ Determine the number or columns of aliens that fit on the screen """
    available_space_x = (ai_settings.screen_width - (3 * alien_width) - ship_width)
    number_columns = int(available_space_x / (2 * alien_width))
    return number_columns


def create_fleet(
        ai_settings,
        aliens,
        screen,
        ship,
):
    """ Create a full fleet of aliens """
    # Creat an alien and find the number of aliens in column.
    alien = Aliens(ai_settings, screen)
    number_aliens_y = get_number_alien_y(ai_settings, alien.rect.height)
    number_columns = get_number_columns(ai_settings, alien.rect.width, ship.rect.width)

    # Create the first column of aliens
    for column_number in range(number_columns):
        for alien_number in range(number_aliens_y):
            create_alien(ai_settings, aliens, alien_number, column_number, screen)


def check_fleet_edges(
        ai_settings,
        aliens
):
    """ Respond appropriately of any aliens have reached an edge. """
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(
        ai_settings,
        aliens
):
    """ Drop the entire fleet and change the fleet's direction. """
    for alien in aliens.sprites():
        alien.rect.x += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def update_aliens(
        ai_settings,
        aliens,
        bullets,
        sb,
        screen,
        ship,
        states
):
    """ check if the fleet at the edge and then update the position of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collision and reach the alien to right
    check_alien_right(ai_settings, aliens, bullets, sb, screen, ship, states)


# ========================================= Update the screen ===============================================
def update_screen(
        ai_settings,
        aliens,
        bullets,
        play_btn,
        sb,
        screen,
        ship,
        states
):
    """ To make the most recent screen """
    # Screen
    pygame.display.set_caption(ai_settings.caption)
    pygame.display.set_icon(ai_settings.icon)
    screen.blit(ai_settings.screen_bg, (0, 0))

    # Bullet
    for bullet in bullets:
        bullet.update_bullet_position()
        bullet.draw_bullet()

    # Ship
    ship.blit_ship()

    # Aliens
    aliens.draw(screen)

    if not states.game_active:
        play_btn.draw_btn()

    # States
    sb.show_states()

    pygame.display.flip()
