import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
import time
import random

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
RED = (255, 0, 120)
BLUE_SNAKE = (0, 0, 255)
RED_SNAKE = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,102)

dis_width = 800
dis_height = 600

SNAKE_SPEED_EASY = 7
SNAKE_SPEED_MEDIUM = 14
SNAKE_SPEED_HARD = 20

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold = True)
    surface, _ = font.render(text = text, fgcolor = text_rgb, bgcolor =bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action = None):
        super().__init__()
        
        self.mouse_over = False

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)

        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb, bg_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center = center_position),
            highlighted_image.get_rect(center = center_position)] 
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self,surface):
        surface.blit(self.image, self.rect)
        
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    SNAKE_EASY = 1
    SNAKE_MEDIUM = 2
    SNAKE_HARD = 3
    PAUSE = 4
    RUNNING = 5
    ABOUT_US = 6

def main():
    pygame.init()

    screen = pygame.display.set_mode((800,600))

    done = False
    
    game_state = GameState.TITLE
    pygame.display.set_caption('SNAKE ARCADE')


    while not done:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.SNAKE_EASY:
            game_state = play_snake(screen, SNAKE_SPEED_EASY)

        if game_state == GameState.SNAKE_MEDIUM:
            game_state = play_snake(screen, SNAKE_SPEED_MEDIUM)

        if game_state == GameState.SNAKE_HARD:
            game_state = play_snake(screen, SNAKE_SPEED_HARD)

        if game_state == GameState.ABOUT_US:
            game_state = about_us(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return
        
    pygame.quit()

def title_screen(screen):

    banner = pygame.image.load('img//banner.png')
    snake_img = pygame.image.load('img//snake_img.png')
    start_easy_btn = UIElement(
        center_position = (400,200),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "EASY",
        action = GameState.SNAKE_EASY
        )

    start_medium_btn = UIElement(
        center_position = (400,290),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "MEDIUM",
        action = GameState.SNAKE_MEDIUM
        )

    start_hard_btn = UIElement(
        center_position = (400,380),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "HARD",
        action = GameState.SNAKE_HARD
        )

    quit_btn = UIElement(
        center_position = (400,500),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "QUIT",
        action = GameState.QUIT
        )

    about_btn = UIElement(
        center_position = (60,560),
        font_size = 15,
        bg_rgb = BLUE,
        text_rgb = RED,
        text = "ABOUT US",
        action = GameState.ABOUT_US
        )

    buttons = [start_easy_btn, start_medium_btn,start_hard_btn, quit_btn, about_btn]
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT
        screen.fill(BLUE)
        screen.blit(snake_img, (150,150))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
            
        screen.blit(banner, (220,50))
        
        pygame.display.flip()

def message(msg, color, screen):
    font_style = pygame.font.SysFont("bahnschrift", 50)
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [300, 250])

def your_score(score,screen):
    score_font = pygame.font.SysFont("courier", 25)
    value = score_font.render("Your Score: "+ str(score), True, YELLOW)
    screen.blit(value, [0, 0])
    
def our_snake(snake_block, snake_list, screen):
    for x in snake_list:
        pygame.draw.rect(screen, BLUE_SNAKE, [x[0],x[1],snake_block, snake_block])

def play_snake(screen, snake_speed):
    
    return_btn = UIElement(
        center_position = (140,570),
        font_size = 20,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "Return to main menu",
        action = GameState.TITLE
        )

    game_over = False
    game_close = False

    x1 = dis_width/2
    y1 = dis_height/2

    snake_List = []
    length_of_snake = 1

    snake_block = 10
    
    x1_change = 0
    y1_change = 0

    clock = pygame.time.Clock()
    
    foodx = round(random.randrange(50, dis_width - snake_block)/ 10.0)*10.0
    foody = round(random.randrange(50, dis_height - snake_block)/10.0)*10.0

    while not game_over:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p :
                    pass
                    
        

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            message("You Lost :(", RED, screen)
            pygame.display.update()
            time.sleep(2)
            return GameState.TITLE
        x1 += x1_change
        y1 += y1_change
                    
        screen.fill(BLUE)

        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > length_of_snake:
            del snake_List[0]

        our_snake(snake_block, snake_List, screen)
        your_score(length_of_snake-1,screen)    

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(20, dis_width - snake_block)/10.0)*10.0
            foody = round(random.randrange(20, 500 - snake_block)/10.0)*10.0
            length_of_snake += 1

        clock.tick(snake_speed)
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)
        
        pygame.display.flip()

    pygame.quit()

def about_us(screen):

    banner = pygame.image.load('img//about_us.png')

    return_btn = UIElement(
        center_position = (140,570),
        font_size = 20,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "Return to main menu",
        action = GameState.TITLE
        )

    screen.blit(banner, (100,40))
    

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)
        
        pygame.display.flip()
    
main()

