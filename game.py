import os
from painting import Painting
import pygame
from customer import Customer
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nature Gallery")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        self.score = 0
        self.paintings = []
        
        self.axe_cursor = pygame.image.load("cursor/sAxe.png")
        self.use_axe_cursor = False
        pygame.mouse.set_visible(True)

        
        self.music_list = [
            "music/Evening.ogg",
            "music/Floating.ogg",
            "music/Forgotten.ogg",
            "music/Polar.ogg",
            "music/Sunlight.ogg"
        ]


        self.current_track_index = 0
        pygame.mixer.music.load(self.music_list[self.current_track_index])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        self.create_painting_grid()

        self.tags_available = [painting.tag for painting in self.paintings]
        self.customer = Customer(self.tags_available)



    def create_painting_grid(self):
        self.paintings = []
        grid_cols = 3
        spacing = 20
        image_size = (100, 100)
        start_x = 210
        start_y = 250

        painting_dir = "paintings"

        files = [f for f in os.listdir(painting_dir) if f.endswith(".jpg")]
        random.shuffle(files)
        files = files[:6]

        for i, filename in enumerate(files):
            name_part = (
                filename.replace("_1.jpg", "").replace("_", " ")
                .title())
            tag = filename.replace("_1.jpg", "").lower()
            image_path = os.path.join(painting_dir, filename)

            row = i // grid_cols
            col = i % grid_cols
            x = start_x + col * (image_size[0] + spacing)
            y = start_y + row * (image_size[1] + spacing)

            painting = Painting(name_part, image_path, (x, y), tag, size=image_size)
            self.paintings.append(painting)
            

    def handle_click(self, pos):

        for painting in self.paintings:
            if painting.is_clicked(pos):
                if painting.tag == self.customer.tag_wanted:
                    self.score += 1

                    self.create_painting_grid()  # Refresh the grid with new paintings
                    self.tags_available = [p.tag for p in self.paintings]

                    if self.tags_available:
                        self.customer = Customer(self.tags_available) 

                        
                else:
                    self.score -= 1
                    self.create_painting_grid()  # Refresh the grid with new paintings
                    self.tags_available = [p.tag for p in self.paintings]

                    if self.tags_available:
                        self.customer = Customer(self.tags_available)

                    else:
                        self.customer = None
                        print("No more paintings available.")  
                    
                break

    
    def draw(self):
        self.screen.fill((220, 240, 255))

        for painting in self.paintings:
            
            pygame.draw.rect(self.screen, (200, 180, 140), painting.rect.inflate(8, 8))
            painting.draw(self.screen)

        # Customer request bubble
        if self.customer:
            self.customer.draw(self.screen)

            restart_hint = self.font.render("Press R to restart", True, (80, 80, 80))
            self.screen.blit(restart_hint, (325, 110))

        else:
            # Game over if no paintings left but since we are refreshing the grid, this won't happen
            game_over = self.font.render("Game Over! Final Score: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(game_over, (200, 50))

            

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))

        if self.use_axe_cursor:
            mx, my = pygame.mouse.get_pos()

            offset_x = -32
            offset_y = -32
            self.screen.blit(self.axe_cursor, (mx + offset_x, my + offset_y))    


    def reset(self):
        self.score = 0
        self.create_painting_grid()
        self.tags_available = [painting.tag for painting in self.paintings]
        self.customer = Customer(self.tags_available)

    def run(self):
        running = True
        while running:
            self.draw()

            # Check if score reached threshold
            if self.score >= 10:
                if not self.use_axe_cursor:
                    pygame.mouse.set_visible(False)
                    self.use_axe_cursor = True
            else:
                if self.use_axe_cursor:
                    pygame.mouse.set_visible(True)
                    self.use_axe_cursor = False


            pygame.display.flip()

            if not pygame.mixer.music.get_busy():
                self.current_track_index = (self.current_track_index + 1) % len(self.music_list)
                pygame.mixer.music.load(self.music_list[self.current_track_index])
                pygame.mixer.music.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)     

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()    



            self.clock.tick(60)
        pygame.quit()                                    


    def load_axe_frames(self):
        sheet = pygame.image.load("cursor/axeSwing.png").convert_alpha()
        frame_width, frame_height = 64, 64

        sheet_width, sheet_height = sheet.get_size()
        cols = sheet_width // frame_width  # should be 8
        rows = sheet_height // frame_height

        self.axe_frames = []
        for row in range(rows):
            for col in range(cols):
                x = col * frame_width
                y = row * frame_height
                frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                self.axe_frames.append(frame)

