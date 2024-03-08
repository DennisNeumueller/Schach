import pygame


class Sound():
    pygame.mixer.init()

    move_sound = pygame.mixer.Sound("sounds/move_sound.mp3")
    beat_sound = pygame.mixer.Sound("sounds/capture_sound.mp3")
    check_sound = pygame.mixer.Sound("sounds/check_sound.mp3")
    promote_sound = pygame.mixer.Sound("sounds/promote_sound.mp3")
    funny_sound = pygame.mixer.Sound("sounds/metal_pipe.mp3")

    def __init__(self, game_state):
        self.game_state = game_state

    # Methods for playing sounds
    def play_move_sound(self):
        self.move_sound.play()

    def play_beat_sound(self):
        self.beat_sound.play()

    def play_check_sound(self):
        self.check_sound.play()

    def play_promote_sound(self):
        self.promote_sound.play()

    def play_sound(self):
        self.funny_sound.play()
