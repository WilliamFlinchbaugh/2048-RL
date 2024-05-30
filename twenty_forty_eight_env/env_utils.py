import pygame as pg

rainbow = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
COLOR_TABLE = {2**i: rainbow[(i-1)%len(rainbow)] for i in range(1, 18)}
COLOR_TABLE[0] = (200, 200, 200)

WINDOW_SIZE = 512
BG_COLOR = (150, 150, 150)

def text_to_screen(screen, text, x, y, color=(0, 0, 0)):
    text = str(text)
    font = pg.font.Font(None, 32)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=(x, y)))