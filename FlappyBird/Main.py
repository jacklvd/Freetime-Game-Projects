try:
    import pygame, sys, random
    from pygame.constants import *

    pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)
    pygame.init()
    pygame.display.set_caption('Flappy Bird')

    #Global variables
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 432
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    #Background
    BG = pygame.image.load('J:/Personal Projects/FlappyBird/assets/background-night.png').convert()
    BG = pygame.transform.scale2x(BG) #double the background image
    #Floor
    FLOOR = pygame.image.load('J:/Personal Projects/FlappyBird/assets/floor.png').convert()
    FLOOR = pygame.transform.scale2x(FLOOR)
    #Bird
    bird_list = [pygame.image.load('J:/Personal Projects/FlappyBird/assets/yellowbird-downflap.png').convert_alpha(),
                pygame.image.load('J:/Personal Projects/FlappyBird/assets/yellowbird-midflap.png').convert_alpha(),
                pygame.image.load('J:/Personal Projects/FlappyBird/assets/yellowbird-upflap.png').convert_alpha()]
    birdimg = bird_list[0]
    bird_rect = birdimg.get_rect(center = (100, 300))
    #Bird timer
    bird_flap = pygame.USEREVENT + 1 #to let the program know that is another event
    pygame.time.set_timer(bird_flap, 200)
    #Tunnel/pipe
    PIPE = pygame.image.load('J:/Personal Projects/FlappyBird/assets/pipe-green.png').convert()
    PIPE = pygame.transform.scale2x(PIPE)
    #Game over background
    GAME_OVER = pygame.image.load('J:/Personal Projects/FlappyBird/assets/message.png').convert_alpha()
    GAME_OVER = pygame.transform.scale2x(GAME_OVER)
    game_over_rect = GAME_OVER.get_rect(center = (216, 300))
    #Spawn timer
    spawn_pipe = pygame.USEREVENT
    pygame.time.set_timer(spawn_pipe, 1200) #1200 equals 1.2s
    #Font game
    game_font = pygame.font.Font('J:/Personal Projects/FlappyBird/04B_19.TTF', 40)
    text_font = pygame.font.Font('freesansbold.ttf', 30)
    #Game sound
    flap_sound = pygame.mixer.Sound('J:/Personal Projects/FlappyBird/sound/sfx_wing.wav')
    hit_sound = pygame.mixer.Sound('J:/Personal Projects/FlappyBird/sound/sfx_hit.wav')
    score_sound = pygame.mixer.Sound('J:/Personal Projects/FlappyBird/sound/sfx_point.wav')

    class Bird:
        #needed variables
        def __init__(self, image):
            self.image = image
            self.gravity = 0.25
            self.movement = 0
            self.bird_index = 0

        #fly action
        def move(self):
            self.movement += self.gravity
            bird_rect.centery += self.movement

        def rotate(self):
            new_bird = pygame.transform.rotozoom(self.image, -self.movement * 3, 1)
            return new_bird

        def animation(self):
            new_bird_img = bird_list[self.bird_index]
            new_bird_rect = new_bird_img.get_rect(center = (100, bird_rect.centery))
            return new_bird_img, new_bird_rect

        def draw(self):
            rotated_bird = Bird.rotate(self)
            SCREEN.blit(rotated_bird, bird_rect)

    class Pipe:

        def __init__(self, image):
            self.image = image
            #create pipe with random height
            self.pipe_height = [200, 225, 250, 300, 400]

        def create(self):
            #random pipe position
            random_pipe_pos = random.choice(self.pipe_height)
            #create new pipe
            bottom_pipe = self.image.get_rect(midtop = (500, random_pipe_pos)) #midtop: central top angle
            top_pipe = self.image.get_rect(midtop = (500, random_pipe_pos - 600))
            return bottom_pipe, top_pipe

        #check collision among bird, pipes, floor
        def check(self, pipes):
            for pipe in pipes:
                if (bird_rect.colliderect(pipe)):
                    hit_sound.play()
                    pygame.time.delay(1300)
                    return False
            if (bird_rect.top <= -65 or bird_rect.bottom >= 550):
                return False
            return True
                
        def move(self, pipes):
            for pipe in pipes:
                pipe.centerx -= 5
            return pipes

        #draw pipes
        def draw(self, pipes):
            for pipe in pipes:
                if (pipe.bottom >= SCREEN_HEIGHT - 100):
                    SCREEN.blit(self.image, pipe)
                else:
                    flip_pipe = pygame.transform.flip(PIPE, False, True)
                    SCREEN.blit(flip_pipe, pipe)

    class Floor:

        def __init__(self, image):
            self.image = image
            self.game_speed = 1
            self.floor_x_pos = 0

        def draw_floor(self):
            SCREEN.blit(self.image, (self.floor_x_pos, 550))
            SCREEN.blit(self.image, (self.floor_x_pos + 432, 550))
            if (self.floor_x_pos + SCREEN_WIDTH <= 0):
                SCREEN.blit(self.image, (self.floor_x_pos + 432, 550))
                self.floor_x_pos = 0
            self.floor_x_pos -= self.game_speed
        
    def menu():

        global pipe_list, game_active, score, high_score, score_sound_countdown, bird_img
        #needed variables
        pipe_list = []
        score = 0
        high_score = 0
        game_active = True
        running = True
        score_sound_countdown = 100
        bird_img = bird_list[0]

        bird = Bird(bird_img)
        pipe = Pipe(PIPE)
        floor = Floor(FLOOR)

        def score_display(game_state):

            global score, high_score
            if (game_state == 'main_game'):
                score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
                score_rect = score_surface.get_rect(center = (216, 100))
                SCREEN.blit(score_surface, score_rect)
            if (game_state == 'game_over'):
                #display normal score
                score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
                score_rect = score_surface.get_rect(center = (216, 200))
                SCREEN.blit(score_surface, score_rect)
                #display high score
                high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
                high_score_rect = high_score_surface.get_rect(center = (216, 530))
                SCREEN.blit(high_score_surface, high_score_rect)

        def update_score(score, high_score):
            if (score > high_score):
                high_score = score
            return high_score

        while running:

            CLOCK.tick(100)

            #Draw background
            SCREEN.blit(BG, (0, 0))

            #Control the game rules
            if (game_active):
                #Draw bird and bird's movement
                bird.move()
                bird.rotate()
                bird.draw()

                #Draw pipes and pipe's movement
                pipe_list = pipe.move(pipe_list)
                pipe.draw(pipe_list)
                game_active = pipe.check(pipe_list)

                #Print score
                score += 0.01
                score_display('main_game')
                score_sound_countdown -= 1

                #Play score sound
                if (score_sound_countdown <= 0):
                    score_sound.play()
                    score_sound_countdown = 100
            else:
                SCREEN.blit(GAME_OVER, game_over_rect)
                high_score = update_score(score, high_score)
                score_display('game_over')

            #Draw floor
            floor.draw_floor()

            #processing loop
            for event in pygame.event.get():
                #exit game
                if (event.type == pygame.QUIT):
                    running = False
                    sys.exit()
                #start playing
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE and game_active):
                        bird.movement = 0
                        bird.movement = -11
                        flap_sound.play()
                    if (event.key == pygame.K_SPACE and game_active == False):
                        game_active = True
                        pipe_list.clear()
                        bird_rect.center = (100, 300)
                        bird.movement = 0
                        score = 0
                #start printing out pipes
                if (event.type == spawn_pipe):
                    pipe_list.extend(pipe.create())
                #bird animation
                if (event.type == bird_flap):
                    if (bird.bird_index < 2):
                        bird.bird_index += 1
                    else:
                        bird.bird_index = 0
                #update bird with animation
                bird_img, bird_rect = bird.animation()
    
            pygame.display.flip()

    def main(start):

        run = True

        while run:
            if (start == 0):
                text = text_font.render('Press Key Space to Start', True, (255, 255, 255))

            text_rect = text.get_rect(center = (216, 300))
            SCREEN.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break # break out of the for loop
                    if event.key == pygame.K_SPACE:
                        menu()
                if event.type == pygame.QUIT:
                    run = False
                    break # break out of the for loop
                
    if (__name__ == "__main__"):
        main(start = 0)

    pygame.quit() #delete all the memory of the program when exit

except Exception as bug:
    print(bug)

input()