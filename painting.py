import pygame

class Painting:
    def __init__(self, name, image_path, position, tag, size):
        self.name = name
        self.size = size
        self.tag = tag
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect= self.image.get_rect(topleft=position)
        self.font = pygame.font.Font(None, 18)


    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            scaled_img = pygame.transform.scale(self.image, (int(self.size[0] * 1.2), int(self.size[1] * 1.2)))
        
            hover_rect = scaled_img.get_rect(center=self.rect.center)
            surface.blit(scaled_img, hover_rect.topleft)
        else:
            surface.blit(self.image,self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)    