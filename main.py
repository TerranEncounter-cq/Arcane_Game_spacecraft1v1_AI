import pygame
import os
import neat
import game as u
import pickle  # 1. Add this
import time 

pygame.init()

WIDTH, HEIGHT = u.WIDTH, u.HEIGHT
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Training")

def eval_genomes(genomes, config):
    start_time = time.time()  # Record the start time

    for _, genome1 in genomes:
        genome1.fitness = 0  # Initialize fitness

    for i, (genome_id1, genome1) in enumerate(genomes):
        for j, (genome_id2, genome2) in enumerate(genomes):
            if j <= i:  # Skip already paired genomes
                continue

            game = u.game()  # Pass the display window to the game

            force_quit = game.train_ai(genome1, genome2, config, start_time)
            
            # Handle pygame events and screen updates here if needed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            if force_quit:
                quit()
def checkpoint_exists(filename):
    return os.path.isfile(filename)

def run_neat(config):
    if checkpoint_exists("neat-checkpoint-75"):
        # Load population from the checkpoint
        p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-11")
        print("Loaded checkpoint 'neat-checkpoint-11'.")
    else:
        # If checkpoint doesn't exist, start a fresh population
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10, filename_prefix="neat-checkpoint-"))

    print(f"Starting NEAT training for up to 100 generations...")
    try:
        winner = p.run(eval_genomes, 100)
    except KeyboardInterrupt:
        print("\nInterrupted! Saving current models...")
        with open("neat-checkpoint.pkl", "wb") as f:
            pickle.dump(p, f)
            print("Saved checkpoint!")
        pygame.quit()
        quit()

    return winner


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    winner = run_neat(config)
    # Here you can visualize or analyze the winner, etc.
