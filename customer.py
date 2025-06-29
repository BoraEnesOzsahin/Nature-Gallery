import random
import pygame

class Customer:
    def __init__(self, tags_available):
        self.tag_wanted = random.choice(tags_available)
        self.display_name = self.tag_wanted.replace("_", " ").title()
        self.font = pygame.font.Font(None, 18)


    def draw(self, surface): 
        # the text

        text = f"I want such beauty of the nature and civilization which is a painting about {self.display_name}."
        label = self.font.render(text, True, (0, 0, 0))

        text_width = label.get_width()
        bubble_width = text_width + 30
        bubble_height = 50

        # the speech bubble
        bubble_rect = pygame.Rect(125, 50, bubble_width, bubble_height)
        pygame.draw.ellipse(surface, (255, 255, 255), bubble_rect)
        pygame.draw.ellipse(surface, (0, 0, 0), bubble_rect, 2)


        # the text
        surface.blit(label, (bubble_rect.x + 15, bubble_rect.y + 15))