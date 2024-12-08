import pygame
from pygame.locals import *
import sys
from moviepy.editor import VideoFileClip 
import random

# Initialize Pygame and set up the display
pygame.init()
fps = 32
s_width = 600
s_height = 360
display = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Flappy Bird Game')

# Initialize clock
fpsclock = pygame.time.Clock()

# Load and resize assets
game_images = {}
game_audio = {}

game_over = 'images/game_over.png'
player = 'images/FlappyBirdUp.png'
background = 'images/background.jpg'
pipe = 'images/pipe.png'
base = 'images/base.jpg'
# Function to resize image
def resize_image(image_path, width):
    image = pygame.image.load(image_path).convert_alpha()
    aspect_ratio = image.get_height() / image.get_width()
    height = int(width * aspect_ratio)
    return pygame.transform.scale(image, (width, height))

# Resize images
game_images['game_over'] = pygame.image.load('game_over.png').convert_alpha()
game_images['base'] = resize_image(base, s_width)  # Resize the base to fit screen width
base_height = game_images['base'].get_height()

game_images['numbers'] = [resize_image(f'images/Score/{i}.png', 30) for i in range(10)]
game_images['pipe'] = (
    pygame.transform.rotate(resize_image(pipe, 80), 180),  # Adjust width as needed
    resize_image(pipe, 80)
)

game_images['background'] = pygame.transform.scale(pygame.image.load(background).convert(), (s_width, s_height))
game_images['player'] = resize_image(player, 50)  # Adjust width as needed

# Load audio files
game_audio['hit'] = pygame.mixer.Sound('sounds/boing.wav')
game_audio['game_over'] = pygame.mixer.Sound('sounds/game_over.wav')
game_audio['intro'] = pygame.mixer.Sound('sounds/start.mp3')
game_audio['point'] = pygame.mixer.Sound('sounds/point.mp3')
game_audio['swoosh'] = pygame.mixer.Sound('sounds/swoosh.mp3')


# Function to play video as a welcome screen
def play_video(video_path):
   while True: 
    game_audio['intro'].play()
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                game_audio['intro'].stop()  
                game_audio['point'].play()
                return 

        # Convert frame to Pygame surface and display it
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        display.blit(pygame.transform.scale(frame_surface, (s_width, s_height)), (0, 0))
        pygame.display.update()
        fpsclock.tick(30)

def Iscollide(playerx, playery, upperPipes, lowerPipes):
    # Check if the player hits the ground (base) or goes above the screen
    if playery >= s_height - base_height - game_images['player'].get_height() or playery < 0:
        game_audio['hit'].play()
        return True
    
    # Check for collisions with upper pipes
    for pipe in upperPipes:
        if playery < pipe['y'] + game_images['pipe'][0].get_height() and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width():
            game_audio['hit'].play()
            return True
    
    # Check for collisions with lower pipes
    for pipe in lowerPipes:
        if playery + game_images['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width():
            game_audio['hit'].play()
            return True           
    

def welcomeScreen():
   play_video('images/message.mp4')
    

def mainGame():
    score = 0
    playerx = int(s_width / 5)
    playery = int(s_height / 2)

    TopPipe = getpipe()
    BottomPipe = getpipe()

    upperPipes = [
        {'x': s_width + 200, 'y': TopPipe[0]['y']},
        {'x': s_width + 200 + (s_width / 2.1), 'y': TopPipe[0]['y']}
    ]
    lowerPipes = [
        {'x': s_width + 200, 'y': TopPipe[1]['y'] + 102},
        {'x': s_width + 200 + (s_width / 2.1), 'y': BottomPipe[1]['y'] + 102}
    ]
    
    pipeVelx = -8
    playerVely = -9
    playerMaxVely = 8
    playerAccY = 1
    playerFlapVel = -8
    playerFlapeed = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                game_audio['swoosh'].play()
                if playery > 0:
                    playerVely = playerFlapVel
                    playerFlapeed = True
                    
        
        crashTest = Iscollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return score
        
        playerMidPos = playerx + game_images['player'].get_width() / 2
        
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos < playerMidPos and not pipe.get('scored', False):
                score += 1
                pipe['scored'] = True  # Mark this pipe as scored
                print(f'Your score is {score}')
                game_audio['point'].play()

        
        if playerVely < playerMaxVely and not playerFlapeed:
            playerVely += playerAccY
        
        if playerFlapeed:
            playerFlapeed = False
        
        playerHeight = game_images['player'].get_height()
        playery = playery + min(playerVely, s_height - playery - playerHeight)

        # Ensure the player does not fall below the base
        if playery > s_height - base_height - playerHeight:
            playery = s_height - base_height - playerHeight

        
        for upper_pipe, lower_pipe in zip(upperPipes, lowerPipes):
            upper_pipe['x'] += pipeVelx
            lower_pipe['x'] += pipeVelx

        if 0 < upperPipes[0]['x'] < 9:
            newpipe = getpipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        display.blit(game_images['background'], (0, 0))
       
        # Draw pipes
        for upper_pipe, lower_pipe in zip(upperPipes, lowerPipes):
            display.blit(game_images['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            display.blit(game_images['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        # Draw the base
        display.blit(game_images['base'], (0, s_height - base_height))

        # Draw player, score, and other elements
        display.blit(game_images['player'], (playerx, playery))

                # Draw score
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += game_images['numbers'][digit].get_width()
        offsetX = (s_width - width) / 2
        for digit in my_digits:
            display.blit(game_images['numbers'][digit], (offsetX, s_height * 0.12))
            offsetX += game_images['numbers'][digit].get_width()
        
        display.blit(game_images['player'], (playerx, playery))
        pygame.display.update()
        fpsclock.tick(fps)

def getpipe():
    pipeHeight = game_images['pipe'][0].get_height()
    offset = int(s_height / 3)
    y2 = random.randrange(int(base_height + 20), int(s_height - base_height - 20))
    pipex = s_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},  # Upper pipe
        {'x': pipex, 'y': y2}    # Lower pipe, positioned above the base
    ]
    return pipe

def Game_over(score):
    display.blit(game_images['game_over'], (1, 1))  # Display the game over image
    game_audio['game_over'].play()
    # Display the score at a specific position (adjust the x, y coordinates as needed)
    my_digits = [int(x) for x in list(str(score))]
    width = 0
    for digit in my_digits:
        width += game_images['numbers'][digit].get_width()
    offsetX = s_width / 1.47  # Center the score horizontally
    offsetY = s_height * 0.55  # Adjust the vertical position as needed

    for digit in my_digits:
        display.blit(game_images['numbers'][digit], (offsetX, offsetY))
        offsetX += game_images['numbers'][digit].get_width()

    pygame.display.update()  # Update the display to show the game over image and score

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                game_audio['game_over'].stop()
                return  # Exit the loop and restart the game
            
# Main game loop
if __name__ == '__main__':
    while True:
        welcomeScreen()
        score = mainGame()
        Game_over(score)