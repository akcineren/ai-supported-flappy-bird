import time
import pygame
import neat
import os
import random
import math
from Pipe import Pipe
from Bird import Bird
from pathlib import Path


WIN_WIDTH = 500
WIN_HEIGHT = 800
PIPE_DIFF = 300
IS_QUIT = False
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))


def draw_window(win, birds, pipesLst, score):
    # Access the global variable 'highest_score' to update or compare with the current score
    global highest_score

    # Draw the background image on the window at position (0,0)
    win.blit(BG_IMG, (0,0))
    
    # Loop through each bird in the 'birds' list and draw them on the window
    for bird in birds:
        bird.draw(win)

    # Loop through each pipe in the 'pipesLst' and draw them on the window
    for pipe in pipesLst:
        pipe.draw(win)

    # Load the font 'font1.ttf' from the 'fonts' directory with a size of 100 for the score
    font = pygame.font.Font("fonts/font1.ttf", 100)
    # Load the same font with a size of 20 for the highest score
    font_small = pygame.font.Font("fonts/font1.ttf", 20)
    
    # Render the current score as a text surface in white color
    score_text = font.render(str(score), True, (255,255,255))
    # Render the highest score as a text surface in white color
    highest_text = font_small.render("Highest: " + str(highest_score), True, (255,255,255))
    
    # Blit (draw) the highest score text at the top left corner of the window
    win.blit(highest_text, (10,10))
    # Blit the current score text at the center top of the window
    win.blit(score_text, (WIN_WIDTH/2-30,WIN_HEIGHT/20))

    # Update the full display Surface to the screen
    pygame.display.update()


def check_collision(bird, pipesLst):
    # Iterate through each pipe in the list of pipes
    for pipe in pipesLst:
        # Check if there is an overlap between the bird's mask and the bottom pipe's mask
        # The overlap method checks if two masks overlap
        # The positions are adjusted by calculating the difference between the pipe's and bird's coordinates
        if bird.bird_mask.overlap(pipe.pipeBottom_mask, (pipe.x - bird.x, pipe.bottom - bird.y)):
            # Return True if there's a collision with the bottom pipe
            return True
        
        # Similarly, check for an overlap between the bird's mask and the top pipe's mask
        elif bird.bird_mask.overlap(pipe.pipeTop_mask, (pipe.x - bird.x, pipe.top - bird.y)):
            # Return True if there's a collision with the top pipe
            return True

    # If no collisions are detected with any of the pipes, return False (not included in the code, but implied)



def find_dist(bird, pipe):
    # Calculate the distance between the bird and the top part of the pipe.
    # This is done using the Pythagorean theorem to find the Euclidean distance.
    # 'abs(bird.x - pipe.x)' calculates the horizontal (x-axis) distance between the bird and pipe,
    # while 'abs(bird.y - pipe.height)' calculates the vertical (y-axis) distance from the bird to the top of the pipe.
    # 'math.sqrt' computes the square root of the sum of these squared distances.
    top_distance = math.sqrt(abs(bird.x - pipe.x)**2 + abs(bird.y - pipe.height)**2)

    # Similarly, calculate the distance between the bird and the bottom part of the pipe.
    # Here, 'abs(bird.y - pipe.bottom)' calculates the vertical distance from the bird to the bottom of the pipe.
    bottom_distance = math.sqrt(abs(bird.x - pipe.x)**2 + abs(bird.y - pipe.bottom)**2)

    # Return a tuple containing both distances: (distance to top of pipe, distance to bottom of pipe)
    return (top_distance, bottom_distance)


def main(genomes, config, last=False):
    # Access the global 'highest_score' variable for comparison and updating
    global highest_score
    # Initialize the score for this session
    score = 0

    # Initialize lists to store neural networks, genome data, bird objects, and pipe objects
    nets = []
    ge = []
    birds = []
    pipesLst = []

    # Create an initial pipe and add it to the pipes list
    pipe = Pipe(500)
    pipesLst.append(pipe)

    # Initialize neural networks, bird objects, and genomes for each genome passed to the function
    for _, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        birds.append(Bird(200, 350))
        genome.fitness = 0
        ge.append(genome)

    # Set up the Pygame window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Game loop control variable
    run = True
    # Pygame clock for controlling frame rate
    clock = pygame.time.Clock()
    while run:
        # Stop the game if highest score is greater than 50 and it's not the last round
        if highest_score > 50 and not last:
            break

        # Set frame rate for the last round
        if last:
            clock.tick(30)

        # Event handling (e.g., for quitting the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Determine which pipe should be the focus for the birds (either the first or second pipe)
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipesLst) > 1 and pipesLst[0].passed:
                pipe_ind = 1
        else:
            # End the loop if no birds are left
            run = False
            break

        # Iterate over each bird and neural network
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            dist_couple = find_dist(bird, pipesLst[pipe_ind])
            output = nets[i].activate((bird.y, dist_couple[0], dist_couple[1]))

            # Make the bird jump if the neural network output exceeds a threshold
            if output[0] > 0.5:
                bird.jump()

        # Increase score and fitness if the birds pass a pipe
        if (not pipesLst[0].passed) and birds[0].x >= pipesLst[0].x + 100:
            for g in ge:
                g.fitness += 5
            score += 1
            if score > highest_score:
                highest_score = score
            pipesLst[0].passed = True

        # Check for collisions and remove birds that collide
        for i, bird in enumerate(birds):
            if check_collision(bird, pipesLst):
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        # Move the pipes
        for pipe in pipesLst:
            pipe.move()

        # Add a new pipe when needed
        if pipesLst[0].passed and not pipesLst[0].QUEUE_CHECK:
            pipesLst[0].QUEUE_CHECK = True
            pipesLst.append(Pipe(500))

        # Remove pipes that have moved out of the screen
        if pipesLst[0].x <= -100:
            pipesLst.pop(0)

        # Check for birds hitting the ground or ceiling and remove them
        for i, bird in enumerate(birds):
            if bird.y == WIN_HEIGHT - 50 or bird.y == 0:
                ge[i].fitness -= 3
                birds.pop(i)
                ge.pop(i)
                nets.pop(i)

        # Draw the game window with the current state
        draw_window(win, birds, pipesLst, score)



def run(config):
    # Initialize a NEAT population using the provided configuration.
    # This population consists of a group of neural networks that will evolve over time.
    population = neat.Population(config)
    
    # Add a standard output reporter to show progress in the console.
    # This will print out the generation number and fitness statistics during the evolution.
    population.add_reporter(neat.StdOutReporter(True))
    
    # Initialize a statistics reporter.
    # This will collect and report statistics about the performance of the neural networks in the population.
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run the NEAT algorithm for 50 generations.
    # The 'main' function is called for each generation to evaluate the fitness of each genome.
    # The 'final' variable will hold the best genome after all generations have been processed.
    final = population.run(main, 50)

    # Return the best genome from the last generation.
    return final



if __name__ == '__main__':
    # Initialize the highest score to 0 at the start of the script.
    highest_score = 0

    # Initialize the Pygame library, which is likely used for creating a game window and handling game events.
    pygame.init()

    # Get the directory where the current script is located.
    file_dir = os.path.dirname(__file__)
    # Get the parent directory of the script's directory and convert it to an absolute path.
    file_dir = Path(file_dir).parent.absolute()
    # Construct the path to the NEAT configuration file.
    config_path = os.path.join(file_dir, "configs/config_feedforward.txt")

    # Set up the NEAT configuration using the specified config file.
    # This configuration defines how the NEAT algorithm will create, reproduce, and evolve neural networks.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    # Run the NEAT algorithm using the 'run' function, which returns the best neural network after evolution.
    final_nnet = run(config)
    # Wrap the final neural network in a list to match the expected format of the 'main' function.
    final_nnet = [(1, final_nnet)]
    
    # Run the 'main' function with the final evolved neural network.
    # This is likely to visualize or test the performance of the neural network in the game environment.
    main(final_nnet, config, True)

    
    