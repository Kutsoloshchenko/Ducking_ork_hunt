import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SKY = (88, 157, 214)
BROWN= (127, 51, 0)


class Animated_sprite(pygame.sprite.Sprite):

    def _get_animation(self, sprite_image, sprite_list):
        walking_frames_r = []

        for sprite in sprite_list:
            walking_frames_r.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))

        walking_frames_l = [pygame.transform.flip(image, True, False) for image in walking_frames_r]

        return (walking_frames_r, walking_frames_l)

    def _get_image(self, x, y, width, height, sprite_sheet):
        image = pygame.Surface([width, height]).convert()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image