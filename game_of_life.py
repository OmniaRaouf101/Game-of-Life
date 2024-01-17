import pygame
import random

pygame.init()

B= (0,0,0)
G= (128, 128, 128)
Y= (255, 255, 0)

W, H = 600, 600
TILE_SIZE = 20
GRID_W= W // TILE_SIZE
GRID_H= H // TILE_SIZE

FBS= 60
screen = pygame.display.set_mode((W, H))
clock= pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRID_H), random.randrange(0, GRID_W)) for _ in range(num)])

def draw_grid(positions):
    for pos in positions:
        col, row = pos
        top_left= (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, Y, (*top_left, TILE_SIZE, TILE_SIZE))
        
    for row in range(GRID_H):
        pygame.draw.line(screen, B, (0, row * TILE_SIZE),(W, row * TILE_SIZE))
    for col in range(GRID_W):
        pygame.draw.line(screen, B, (col * TILE_SIZE, 0),(col * TILE_SIZE, H))    

def adjust_grid(positions):
    all_neighbours= set()
    new_positions= set()

    for pos in positions:
        neighbours= get_neighbours(pos)
        all_neighbours.update(neighbours)

        neighbours= list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) in [2, 3]:
            new_positions.add(pos)

    for pos in all_neighbours:
        neighbours= get_neighbours(pos)
        neighbours= list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 3:
            new_positions.add(pos)

    return new_positions                

def get_neighbours(pos):
    x, y= pos
    neighbours= []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_W:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_H:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbours.append((x+dx, y+dy))

    return neighbours        



def main():
    running= True
    playing= False
    count= 0
    update_freq= 120

    positions= set()


    while running:
        clock.tick(FBS)
        if playing:
            count+= 1
        if count >= update_freq:
            count = 0
            positions= adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")    
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y= pygame.mouse.get_pos()
                col= x // TILE_SIZE
                row= y // TILE_SIZE
                pos= (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)       

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        playing= not playing

                    if event.key == pygame.K_c:
                        positions= set()
                        playing= False
                        count = 0

                    if event.key == pygame.K_g:
                        positions= gen(random.randrange(4, 10)*GRID_W)
    
        screen.fill(G)
        draw_grid(positions)
        pygame.display.update()
    
    pygame.quit()

if __name__ == '__main__':
    main()                