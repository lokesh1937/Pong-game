import pygame

# Initialize pygame
pygame.init()
#width and height of window
width, height = 720, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG")
#font of the score
game_font=pygame.font.SysFont("comicsans",50)
fps = 60
pad_width = 20
pad_height = 150
radius = 10
radius1=60
target_score=10
font_color=(255,255,0)

#class for paddles
class pad:
    color = (242, 95, 31)
    velocity = 5

    def __init__(self, x, y, width, height):
        self.x =self.original_x= x
        self.y =self.original_y=y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def movement(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y
        
 
#class for ball
class ball:
    color1 = (173, 135, 92)
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x =self.original_x=x
        self.y =self.original_y=y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color1, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
     self.x=self.original_x
     self.y=self.original_y
     self.y_vel=0
     self.x_vel*=-1

#collision conditions
def collisions(bball,left_pad,right_pad,bounce_effect):
    if bball.y-bball.radius<=0:
        bball.y_vel=-1* bball.y_vel
    elif bball.y+bball.radius>=height:
        bball.y_vel=-1*bball.y_vel
    
    if bball.x_vel<0:
        if bball.y>=left_pad.y and bball.y<=left_pad.y+left_pad.height:
            if bball.x-bball.radius<=left_pad.x+left_pad.width:
               if bball.x_vel<0:
                   bball.x_vel-=0.5
                   bball.x_vel=-1*bball.x_vel
               elif bball.x_vel>0:
                   bball.x_vel+=0.5
                   bball.x_vel=-1*bball.x_vel
               bounce_effect.play()
               middle_y=left_pad.y+left_pad.height/2
               diff_y=middle_y-bball.y
               reduction_factor=(left_pad.height/2)/bball.MAX_VEL
               y_vel=diff_y/reduction_factor
               bball.y_vel=-1*y_vel
        
    else:
        if bball.y>=right_pad.y and bball.y<=right_pad.height+right_pad.y:
            if bball.x+bball.radius>=right_pad.x:
              if bball.x_vel<0:
                   bball.xvel-=0.5
                   bball.x_vel=-1*bball.x_vel
              elif bball.x_vel>0:
                   bball.x_vel+=0.5
                   bball.x_vel=-1*bball.x_vel
              bounce_effect.play()
              middle_y=right_pad.y+right_pad.height/2
              diff_y=middle_y-bball.y
              reduction_factor=(right_pad.height/2)/bball.MAX_VEL
              y_vel=diff_y/reduction_factor
              bball.y_vel=-1*y_vel

    
#movement keys
def pad_movement(keys, left_pad, right_pad):
    if keys[pygame.K_w] and left_pad.y - left_pad.velocity >= 0:
        left_pad.movement(up=True)
    if keys[pygame.K_s] and left_pad.y + left_pad.height + left_pad.velocity <= height:
        left_pad.movement(up=False)
    if keys[pygame.K_UP] and right_pad.y - right_pad.velocity >= 0:
        right_pad.movement(up=True)
    if keys[pygame.K_DOWN] and right_pad.y + right_pad.height + right_pad.velocity <= height:
        right_pad.movement(up=False)


#drawing 
def draw(screen, pads, bball,left_score,right_score):
    screen.fill((46, 219, 188))
    pygame.draw.circle(screen,(255,255,255),(width//2,height//2),radius1,2)
    for x in range(10,height,height//20):
        pygame.draw.rect(screen,(245, 239, 237),(width//2-2,x,4,10))
    left_text=game_font.render(f"{left_score}",1,font_color)
    right_text=game_font.render(f"{right_score}",1,font_color)
    screen.blit(left_text,(width//4-left_text.get_width()//2,20))
    screen.blit(right_text,(width*(3/4)-right_text.get_width()//2,20))
    
    for pad in pads:
        pad.draw(screen)
    bball.draw(screen)
    pygame.display.update()


def main():
    running = True
    clock = pygame.time.Clock()
    left_pad = pad(10, height // 2 - pad_height // 2, pad_width, pad_height)
    right_pad = pad(width - 10 - pad_width, height // 2 - pad_height // 2, pad_width, pad_height)
    bball = ball(width // 2, height // 2, radius)
    left_score=0
    right_score=0
    
    #sound effects
    bounce_effect=pygame.mixer.Sound("bounce2.wav")
    leave_effect=pygame.mixer.Sound("bounce1.mp3")
    victory_sound=pygame.mixer.Sound("victory.mp3")
    leave_effect.set_volume(0.7)
    bounce_effect.set_volume(0.8)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if right_score<target_score and left_score<target_score:
         pad_movement(keys, left_pad, right_pad)
         bball.move()
         draw(screen, [left_pad, right_pad], bball,left_score,right_score)
         collisions(bball,left_pad,right_pad,bounce_effect)
         
        
        if bball.x<0:
            right_score+=1
            leave_effect.play()
            bball.reset()
        elif bball.x>width:
            left_score+=1
            leave_effect.play()
            bball.reset()
        
        won=False
        if right_score>=target_score:
            won=True
            title="RIGHT PLAYER WON!"
        elif left_score>=target_score:
            won=True
            title="LEFT PLAYER WON!"
        if won:
            text=game_font.render(f"{title}",1,font_color)
            screen.blit(text,(width//2-text.get_width()//2,height//2-text.get_height()//2))
            victory_sound.play()
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
            pygame.display.update()
            pygame.time.delay(6000)
            left_score=0
            right_score=0
            bball.reset()
            left_pad.reset()
            right_pad.reset()
            

    pygame.quit()


if __name__ == "__main__":
    main()
