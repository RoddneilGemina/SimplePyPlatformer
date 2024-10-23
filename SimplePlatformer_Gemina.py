import pygame
pygame.init()

pygame.display.set_caption("Simple Platformer")
movx = 0
movy = 0
speed = 4
crouched_speed = speed / 2
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height)) 
curr_state = 0
playerstates = [
[2, 1, 0, 0, 3,-1],
[0, 1, 1, 1, 1,-1],
[2, 1, 2, 2, 3,-1],
[3, 3, 3, 3,-1, 0],
]

class FloorBlock:
    def __init__(self, x, y, width, height, color=(255,255,211)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Ladder:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        rung_count = 4
        rung_height = self.rect.height // (rung_count + 1)
        for i in range(1, rung_count + 1):
            y = self.rect.top + i * rung_height
            pygame.draw.line(surface, (0,0,0), (self.rect.left, y), (self.rect.right, y), 2)


class Player:
    global speed, crouched_speed
    color = (0,0,255)
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vely = 0
        self.gravity = 0.7
        self.onGround = False
        self.onLadder = False
        self.isCrouching = False

    def move(self, movx, floor_blocks, ladder_blocks):
        self.rect.x += movx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        if not self.onLadder:
            self.vely += self.gravity
            self.rect.y += self.vely

        if self.rect.bottom > ladder_blocks[self.onLadder].rect.bottom:
                self.rect.bottom = ladder_blocks[self.onLadder].rect.bottom
                self.vely = 0

        self.check_collision(floor_blocks)
        self.check_ladder_collision(ladder_blocks)

    def check_collision(self, floor_blocks):
        self.onGround = False
        for floor in floor_blocks:
            if self.rect.colliderect(floor.rect):
                if self.vely > 0:
                    self.rect.bottom = floor.rect.top
                    self.vely = 0
                    self.onGround = True   

    def check_ladder_collision(self, ladder_blocks):
        self.onLadder = False
        for ladder in ladder_blocks:
            if self.rect.colliderect(ladder.rect):
                self.onLadder = True
                break

    def jump(self):
        if self.onGround:
            self.vely = -10

    def climb(self, direction):
        if self.onLadder and not self.isCrouching:
            self.rect.y += direction * 5

    def crouch(self):
        if not self.onLadder:
            self.isCrouching = True
            self.rect.height = 15
            return crouched_speed
        return speed
    
    def stand(self):
        self.isCrouching = False
        self.rect.height = 30
        return speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def main():
    global movx, movy, screen, curr_state, playerstates
    running = True
    clock = pygame.time.Clock()
    player = Player(500, 400)
    ladder_blocks = []

    curr_x = 100
    curr_y = 450

    floor_blocks = [
        FloorBlock(150, 250, 300, 20), 
        FloorBlock(500, 120, 300, 20), 
        FloorBlock(0, screen_height - 20, screen_width, 20)
    ]

    for x in range(5):
        temp_ladder = Ladder(curr_x,curr_y,width=50,height=50,color=(211,211,211))
        ladder_blocks.append(temp_ladder)
        curr_y -= 50

    curr_x = 450
    curr_y += 20

    for x in range(3):
        temp_ladder = Ladder(curr_x,curr_y,width=50,height=50,color=(211,211,211))
        ladder_blocks.append(temp_ladder)
        curr_y -= 50
        

    while running:
        screen.fill((255, 255, 255))

        for ladder in ladder_blocks:
            ladder.draw(screen)

        for floor in floor_blocks:
            floor.draw(screen)

        player.move(movx, floor_blocks, ladder_blocks)
        player.draw()
        pygame.display.update()
        clock.tick(60)

        keys = pygame.key.get_pressed()
        movx = 0
        match curr_state:
            case 0:
                if player.onLadder:
                    curr_state = playerstates[curr_state][4]
                if keys[pygame.K_DOWN]:
                    movx = player.crouch()
                    curr_state = playerstates[curr_state][1]
                if keys[pygame.K_UP]:
                    curr_state = playerstates[curr_state][2]
                if keys[pygame.K_LEFT]:
                    movx = -speed
                if keys[pygame.K_RIGHT]:
                    movx = speed
            case 1:
                if keys[pygame.K_LEFT]:
                    movx = -crouched_speed
                if keys[pygame.K_RIGHT]:
                    movx = crouched_speed
                if not player.onLadder and keys[pygame.K_UP]:
                    movx = player.stand()
                    curr_state = playerstates[curr_state][0]
            case 2:
                if player.onLadder:
                    curr_state = playerstates[curr_state][4]
                if keys[pygame.K_LEFT]:
                    movx = -speed
                if keys[pygame.K_RIGHT]:
                    movx = speed
                if keys[pygame.K_DOWN]:
                    player.crouch()
                    curr_state = playerstates[curr_state][1]
            case 3:
                player.vely = 0
                if not player.onLadder:
                    curr_state = playerstates[curr_state][5]
                if keys[pygame.K_LEFT]:
                    movx = -speed
                if keys[pygame.K_RIGHT]:
                    movx = speed
                if keys[pygame.K_UP]:
                    player.climb(-1)
                if keys[pygame.K_DOWN]:
                    player.climb(1)

        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if not player.onLadder and not player.isCrouching:
                            player.jump()
                    if event.key == pygame.K_DOWN:
                        movy = speed
                    if event.key == pygame.K_LEFT:
                        movx = -speed
                    if event.key == pygame.K_RIGHT:
                        movx = speed
                if event.type == pygame.QUIT:
                    running = False    

if __name__ == "__main__":
    main()
