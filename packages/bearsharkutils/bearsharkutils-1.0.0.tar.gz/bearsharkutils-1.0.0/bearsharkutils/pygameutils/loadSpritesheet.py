from .datastructures import Frame
import pygame


def loadSpritesheet(
    filename: str, frameSize: tuple[int, int], rows: int, durationsMs: list[int]
) -> list[Frame]:
    """
    @brief Load spritesheet and return list of Frames. This is a convenience function for loading spritesheet and creating a list of Frame objects.
    @param filename Name of the file to load. Must be a path to an image file
    @param frameSize Tuple of x and y dimensions of each frame
    @param rows Number
    @param durationsMs
    """
    frameList: list[Frame] = []
    spritesheet = pygame.image.load(filename)
    for i in range(rows):
        frameList.append(
            Frame(
                spritesheet.subsurface(pygame.Rect(i * frameSize[0], 0, *frameSize)),
                durationsMs[i],
            )
        )

    return frameList


def text(
    surf: pygame.Surface,
    text: str,
    size: int,
    color: tuple,
    antialias: bool,
    **rectkvargs
):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, antialias, color)
    rect = img.get_rect(**rectkvargs)
    surf.blit(img, rect)
