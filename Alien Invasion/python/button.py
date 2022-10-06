import pygame


class Button:

    def __init__(
            self,
            ai_settings,
            screen
    ):
        """ Initialize button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Build button's rect object and center it
        self.rect = pygame.Rect(
            0,
            0,
            ai_settings.btn_width,
            ai_settings.btn_height
        )
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self.prep_msg()

    def prep_msg(self):
        """ Turn message to a rendered image and center the text on the button """
        self.msg_img = self.ai_settings.btn_font.render(
            self.ai_settings.btn_msg,
            True,
            self.ai_settings.electron_blue,
            self.ai_settings.light_greenish_blue
        )

        self.msg_rect = self.msg_img.get_rect()
        self.msg_rect.center = self.rect.center

    def draw_btn(self):
        """ Draw blanc button and then draw message"""
        self.screen.fill(
            self.ai_settings.light_greenish_blue,
            self.rect
        )
        self.screen.blit(
            self.msg_img,
            self.msg_rect
        )
