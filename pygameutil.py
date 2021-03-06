from typing import Any, Callable

import pygame


class Text:
    def __init__(self, font: pygame.font.Font | tuple,
                 text: str | bytes, color: Any, *, antialias: bool = True,
                 background: Any | None = None):
        if isinstance(font, pygame.font.Font):
            self.font = font
        elif isinstance(font, tuple):
            self.font = pygame.font.Font(*font)
        self.text = text
        self.color = color
        self.antialias = antialias
        self.background = background
        self.surface = self.font.render(text, antialias, color, background)
        self.rect = self.surface.get_rect()

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: Text, inactive: Any, active: Any,
                 rect: pygame.Rect | tuple | None = None,
                 onclick: Callable = lambda *args, **kwargs: None):
        self.text = text
        self.inactive = inactive
        self.active = active
        if isinstance(rect, pygame.Rect):
            self.rect = rect
        elif isinstance(rect, tuple):
            self.rect = pygame.Rect(*rect)
        else:
            self.rect = self.text.rect
        self.onclick = onclick

    def __bool__(self):
        return self.collidepoint(pygame.mouse.get_pos())

    def collidepoint(self, *args):
        return self.rect.collidepoint(*args)

    def draw(self, surface):
        if self:
            pygame.draw.rect(surface, self.active, self.rect)
        else:
            pygame.draw.rect(surface, self.inactive, self.rect)
        surface.blit(self.text.surface, self.text.rect)

    def click(self, *args, **kwargs):
        self.onclick(*args, **kwargs)
