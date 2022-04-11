from typing import Any, Callable

import pygame


class Text:
    def __init__(self, font: pygame.font.Font | tuple | None,
                 text: str | bytes, color: Any, *, antialias: bool = True,
                 background: Any | None = None, center: tuple = None):
        if isinstance(font, pygame.font.Font):
            self.font = font
        elif isinstance(font, tuple):
            self.font = pygame.font.Font(font[0], font[1])
        else:
            self.font = pygame.font.Font(None, 0)
        self.text = text
        self.color = color
        self.antialias = antialias
        self.background = background
        self.surface = self.font.render(text, antialias, color, background)
        if center is None:
            self.rect = self.surface.get_rect()
        else:
            self.rect = self.surface.get_rect(center=center)
        self.center = self.rect.center

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: Text, rect: pygame.Rect | tuple,
                 inactive: Any, active: Any,
                 onclick: Callable = None, *args):
        self.text = text
        self.rect = rect
        self.inactive = inactive
        self.active = active
        self.onclick = onclick
        self.args = args

    def __bool__(self):
        return self.collidepoint(pygame.mouse.get_pos())

    def collidepoint(self, *args):
        if len(args) == 1:
            return self.rect.collidepoint(args[0])
        else:
            return self.rect.collidepoint(args[0], args[1])

    def draw(self, surface):
        if self:
            pygame.draw.rect(surface, self.active, self.rect)
        else:
            pygame.draw.rect(surface, self.inactive, self.rect)
        surface.blit(self.text.surface, self.text.rect)

    def click(self):
        if self.onclick is not None:
            self.onclick(*self.args)
