import pygame
import sys
import random


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE
#กำหนดขนาดหน้าต่างของเกมและสร้างตารางเพื่อกำหนดตัวงูขนาด 1 บล็อก
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)
#กำหนดชื่อทิศทางว่าต้องไปทางไหน
#โดยเราจะกำหนด class มาสองตัวนั่นคือตัวงูและอาหาร
class Snake():
    #องค์ประกอบของงู
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.color = (17,24,47)
        self.score = 0
        #กำหนดค่าเริ่มต้นของงู เป็นค่าพื้นฐานโดยให้งูเริ่มขนาดเท่าใด เริ่มที่ตำแหน่งไหน เริ่มไปทางไหน สีอะไร คะแนนเริ่มที่เท่าไหร่
    
    def get_head_position(self):
        return self.positions[0]
        #กำหนดการหันหัวของงู
    def turn(self,point):
        if self.length > 1 and (point[0] * -1,point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
        #กำหนดให้งูไม่สามารถเดินย้อนได้ในกรณีที่ตัวยาวกว่า 1 ช่อง แต่ถ้าทิศไหนเดินได้ก็เดิน
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+(x*GRIDSIZE))% SCREEN_WIDTH),(cur[1] + (y*GRIDSIZE))% SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()
                
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.score = 0
        #ตัวแปรรีเซ็ต ถ้าถูกเรียกใช้งูจะกลับไปเป็นค่าเริ่มต้นใหม่
    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0],p[1]),(GRIDSIZE , GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface,(0,0,0),r,1)
            #โชว์ตัวงูในเกม

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                #กำหนดอีเว้นการเคลื่อนที่ว่าว่าการกดคีย์บอร์ดแต่ละตัวหมายความว่าต้องแสดงผลอะไร
class Food():
    #class ของอาหารที่จะให้งูกิน
    def __init__(self):
        self.positions = (0,0)
        self.color = (223,163,49)
        self.randomize_position()
        #กำหนดค่าเริ่มต้นของอาหาร
    def randomize_position(self):
        self.positions = (random.randint(0,GRID_WIDTH-1)*GRIDSIZE,random.randint(0,GRID_HEIGHT-1)*GRIDSIZE)
        #กำหนดให้มีการ random 
    def draw(self,surface):
        r = pygame.Rect((self.positions[0],self.positions[1]),(GRIDSIZE,GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface,(0,0,0),r,1)
        #กำหนดให้โชว์อาหาร
def drawGrid(surface):
    for y in range(0,int(GRID_HEIGHT)):
        for x in range(0,int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE),(GRIDSIZE , GRIDSIZE))
                pygame.draw.rect(surface,(139,119,101),r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE),(GRIDSIZE , GRIDSIZE))
                pygame.draw.rect(surface,(139,119,101),rr)
                

def main():
    #ฟังก์ชันหลักในการดำเนินเกม
    pygame.init()
    
    pygame.display.set_caption('Makok the Snake')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
    #ตั้งค่าขนาดหน้าจอ
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",16)


    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.positions:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            #ถ้าหัวงูกับอาหารอยู่ตำแหน่งเดียวกัน ขนาดกับคะแนนจะเพิ่มขึ้นทีละ 1
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface,(0,0))
        text = myfont.render("Score {0}".format(snake.score),1,(0,0,0))
        # กำหนดให้โชว์ข้อความคะแนน
        screen.blit(text,(5,10))
        pygame.display.update()

main()
