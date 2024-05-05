import pygame
import sys
import math
'''
import tkinter as tk

isValueGenuine = False
while not isValueGenuine:
    try:
        tickvalue = abs(int(input("Please enter the tick value (Less values results in a slow experience, whereas higher values result in a fast one. Recommended: 60 to 120 for satisfying, 1000 to 2000 for quick, 10000 to 20000 for super quick): ")))
        isValueGenuine = True
    except:
        print("Invalid format. Try typing integers.")


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.destroy()

WIDTH, HEIGHT = screen_width-70, screen_height - 70
'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 10, 10)
BLUE =  (30, 40, 255)
GRAVITY = 9.81
WIND_SPEED = 0

tickvalue = 80

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
screen_height, screen_width = HEIGHT, WIDTH

pygame.display.set_caption("Projectile Motion Simulation")

#font_path = "D:/Aadarsh Stuff/Roboto/Roboto-Black.ttf"
font = pygame.font.SysFont(None, 24)

divy = screen_height-100

textbox_rect = pygame.Rect(20, divy + 40, 300, 40)
textbox_color = BLACK
text = ""

textboxoutlinerect = pygame.Rect(18, divy + 38, 304, 44)

div_rect = pygame.Rect(0, divy, screen_width, 100)

div_img = pygame.image.load("bgforprojectile.jpg")
div_img = pygame.transform.scale(div_img, (div_img.get_width()/2, 100))
img_rect = pygame.Rect(0, divy, screen_width, 100)

toUse = None

ballIsThrown = False

isboundarylimited = True

istextboxactive = False

ticks = 0

mode = 1

checkbox_br = 25

height = 0
range = 0

dist = 0
angle = 0

checkbox_rect = pygame.Rect(350, divy + 40, 60, 30)

exit_rect = pygame.Rect(screen_width - 200, divy + 40, 150, 40)

def draw_divider():
    global screen_width, screen_height
    pygame.draw.rect(screen, WHITE, div_rect)
    screen.blit(div_img, img_rect)
    #pygame.draw.line(screen, BLACK, (0, divy), (screen_width, divy))
    if type(range) == float and type(height) == float:
        font_2 = pygame.font.SysFont(None, 30)
        text_surface_2 = font_2.render('Velocity: ' + str(round(dist, 2)) + ' Angle: ' + str(round(angle-180, 2)), True, WHITE)
        text_surface_3 = font_2.render('Range: '+str(round(range, 2))+' Height: '+str(round(height, 2)), True, WHITE)
        screen.blit(text_surface_2, (screen.get_width()/2, screen.get_height()-70))
        screen.blit(text_surface_3, (screen.get_width()/2, screen.get_height()-40))

def draw_textbox():
    global screen_width, screen_height
    #pygame.draw.rect(screen, WHITE, textbox_rect)
    pygame.draw.rect(screen, WHITE, textbox_rect, 2)
    if istextboxactive:
        pygame.draw.rect(screen, BLUE, textboxoutlinerect, 2)
    text_surface_2 = font.render("Wind factor:", True, WHITE)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (textbox_rect.x + 5, textbox_rect.y + 10))
    screen.blit(text_surface_2, (textbox_rect.x + 5, textbox_rect.y - 30))

def draw_checkbox():
    global screen_width, screen_height
    checkboxtextsurface = font.render("Boundary is at bottom of screen:", True, WHITE)
    if isboundarylimited:
        pygame.draw.rect(screen, WHITE, checkbox_rect, 0, checkbox_br)
        pygame.draw.rect(screen, BLACK, checkbox_rect, 3, checkbox_br)
        pygame.draw.circle(screen, WHITE, (360, divy + 55), 20)
        pygame.draw.circle(screen, BLACK, (360, divy + 55), 20, 3)
    else:
        pygame.draw.rect(screen, BLUE, checkbox_rect, 0, checkbox_br)
        pygame.draw.rect(screen, WHITE, checkbox_rect, 3, checkbox_br)
        pygame.draw.circle(screen, BLUE, (400, divy + 55), 20)
        pygame.draw.circle(screen, WHITE, (400, divy + 55), 20, 3)
        #pygame.draw.line(screen, WHITE, (checkbox_rect.x + 8, checkbox_rect.y + 17), (checkbox_rect.x + 17, checkbox_rect.y + 30), 3) #tick
        #pygame.draw.line(screen, WHITE, (checkbox_rect.x + 17, checkbox_rect.y + 30), (checkbox_rect.x + 32, checkbox_rect.y + 8), 3) #tick  
    screen.blit(checkboxtextsurface, (checkbox_rect.x + 5, checkbox_rect.y - 30))

def draw_exitbutton():
    global screen_width, screen_height
    exittextsurface = font.render("EXIT", True, WHITE)
    #pygame.draw.rect(screen, WHITE, exit_rect)
    pygame.draw.rect(screen, WHITE, exit_rect, 10, 10)
    screen.blit(exittextsurface, (exit_rect.x + 53, exit_rect.y + 12))

if not pygame.font.get_init():
    print("Font initialization failed.")
    pygame.quit()
    sys.exit()
    
screen.fill(WHITE)
pygame.display.update()

class Target:
    def __init__(self, start_pos, velocity, angle, color):
        self.start_pos = start_pos
        self.x, self.y = start_pos
        self.angle = math.radians(angle)
        self.vx = velocity * math.cos(self.angle)
        self.vy = velocity * math.sin(self.angle)
        self.time = 0
        self.color = color
        self.time_step = 0.08

    def update(self):
        self.x = self.start_pos[0] + self.vx * self.time
        self.y = self.start_pos[1] + self.vx * self.time
        self.time += self.time_step
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

class Projectile:
    def __init__(self, start_pos, velocity, angle, wind):
        self.start_pos = start_pos
        self.x, self.y = start_pos
        self.angle = math.radians(angle)
        self.vx = velocity * math.cos(self.angle)
        self.vy = velocity * math.sin(self.angle)
        self.time = 0
        self.time_step = 0.08
        self.wind = wind

    def update(self):
        try:
            float(self.wind)
        except:
            self.wind = 0
        self.x = self.start_pos[0] + self.vx * self.time + 0.5 * float(self.wind) * self.time**2
        self.y = self.start_pos[1] - self.vy * self.time + 0.5 * GRAVITY * self.time**2
        self.time += self.time_step

    def draw(self):
        try:
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)
        except TypeError:
            errorFont = font.render('Could not display due to program limitations. Please consider decreasing the wind factor. NOTE: Display does not affect the simulation. Range and Height are given below.', False, RED)
            screen.blit(errorFont, (10, 10))

def main():
    global screen_width, screen_height
    global dist
    global angle
    global isboundarylimited
    global toUse
    global height
    global istextboxactive
    global WIDTH
    global HEIGHT
    clock = pygame.time.Clock()
    global text
    global ticks
    global font
    global range
    global textbox_rect
    global textbox_color
    global running
    running = True
    if mode == 1:
        while running:
            global font
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t and not istextboxactive:
                        if isboundarylimited == True:
                            isboundarylimited = False
                        else:
                            isboundarylimited = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_TAB and not istextboxactive:
                        istextboxactive = True
                    elif event.key == pygame.K_TAB and istextboxactive:
                        istextboxactive = False
                    if istextboxactive:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1] if len(text) > 0 else ""
                        elif event.key == pygame.K_TAB:
                            pass
                        else:
                            text += event.unicode

            draw_divider()
            draw_textbox()
            draw_checkbox()
            draw_exitbutton()
            pygame.display.update()
            # Render text
            """
            rendered_text = font.render(text, True, BLACK)
            text_rect = rendered_text.get_rect()
            text_rect.center = textbox_rect.center

            # Draw textbox
            pygame.draw.rect(screen, textbox_color, textbox_rect, 2)
            screen.blit(rendered_text, text_rect)
            """

            mouse_pos = pygame.mouse.get_pos()

            if not pygame.mouse.get_pressed()[0]:
                hasmouseinteracted = False

            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] >= divy and not hasmouseinteracted:
                hasmouseinteracted = True
                inactivvemousex = mouse_pos[0]
                inactivvemousey = mouse_pos[1]
                if inactivvemousey > textbox_rect.top and inactivvemousey < textbox_rect.top + textbox_rect.height and inactivvemousex > textbox_rect.left and inactivvemousex < textbox_rect.left + textbox_rect.width:
                    istextboxactive = True
                else:
                    istextboxactive = False
                    if inactivvemousey > checkbox_rect.top and inactivvemousey < checkbox_rect.top + checkbox_rect.height and inactivvemousex > checkbox_rect.left and inactivvemousex < checkbox_rect.left + checkbox_rect.width:
                        if isboundarylimited == False:
                            isboundarylimited = True
                        else:
                            isboundarylimited = False

                    if inactivvemousey > exit_rect.top and inactivvemousey < exit_rect.top + exit_rect.height and inactivvemousex > exit_rect.left and inactivvemousex < exit_rect.left + exit_rect.width:
                        pygame.quit()
                        sys.exit()

            if pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pos()[1] >= divy:
                ballIsThrown = True
                pygame.draw.circle(screen, BLACK, mouse_pos, 10)
                pygame.display.update()
                mouse_pos = pygame.mouse.get_pos()
                initialX = mouse_pos[0]
                initialY = mouse_pos[1]

                while pygame.mouse.get_pressed()[0]:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    if not ballIsThrown:
                        break
                    draw_divider()
                    draw_textbox()
                    draw_checkbox()
                    draw_exitbutton()
                    pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, screen_width, divy))
                    pygame.draw.circle(screen, BLACK, (initialX, initialY), 10)
                    mouse_pos = pygame.mouse.get_pos()
                    finalX = mouse_pos[0]
                    finalY = mouse_pos[1]
                    dist = math.sqrt((finalX-initialX)**2 + (finalY-initialY)**2)
                    dx = finalX - initialX
                    dy = finalY - initialY

                    if dx == 0:
                        dx = 0.0001

                    angle = math.degrees(math.atan(-dy / dx))  # Calculate angle in degrees
                    if dx < 0:
                        angle += 180
                    
                    text_surface = font.render('Velocity: '+str(round(dist, 2))+' Angle: '+str(round(angle-180, 2)), True, BLACK)
                    screen.blit(text_surface, (finalX, finalY + 20))
                    
                    pygame.draw.line(screen, BLACK, (initialX, initialY), (finalX, finalY), 5)
                    pygame.display.update()
                ballIsThrown = False
                draw_divider()
                draw_textbox()
                draw_checkbox()
                draw_exitbutton()
                pygame.display.update()

                pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, screen_width, divy))
                pygame.draw.circle(screen, BLACK, (initialX, initialY), 10)
                pygame.display.update()
                mouse_pos = pygame.mouse.get_pos()
                finalX = mouse_pos[0]
                finalY = mouse_pos[1]
                dist = math.sqrt((finalX-initialX)**2 + (finalY-initialY)**2)
                dx = finalX - initialX
                dy = finalY - initialY

                if dx == 0:
                    dx = 0.0001

                angle = math.degrees(math.atan(-dy / dx))
                if dx < 0:
                    angle += 180

                angle += 180

                projectile = Projectile([initialX, initialY], dist, angle, text)
                heights = []
                if isboundarylimited:
                    toUse = initialY
                else:
                    toUse = divy
                running_2 = True
                while projectile.y <= toUse and running_2:
                    #pygame.time.delay(50)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running_2 = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_s:
                                running_2 = False

                    projectile.update()
                    projectile.draw()
                    infoText = font.render("Press s to halt", False, BLACK)
                    screen.blit(infoText, (50, 50))
                    heights.append(projectile.y)
                    draw_divider()
                    draw_textbox()
                    draw_checkbox()
                    draw_exitbutton()
                    pygame.display.update()
                    clock.tick(tickvalue)
                istextboxactive = False
                max_height = min(heights) # minimum cuz height in pygame is calculated from the top
                range = projectile.x - initialX
                height = initialY - max_height
                pygame.draw.rect(screen, WHITE, pygame.Rect(50, 50, 115, 35)) # to cover infotext
                #font_path_2 = "D:/Aadarsh Stuff/Roboto/Roboto-Black.ttf"
                pygame.display.update()

            clock.tick(60)
    elif mode == 2:
        targetpositionSet = False
        shooterpositionSet = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit() 
            while not pygame.mouse.get_pressed()[0] and not targetpositionSet:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()          
                screen.fill(WHITE)
                mousex = pygame.mouse.get_pos()[0]
                mousey = pygame.mouse.get_pos()[1]
                target = Target((mousex, mousey), 0, 0, RED)
                target.update()
                target.draw()
                pygame.display.update()
            if not targetpositionSet:
                targetpositionSet = True
                target = Target((mousex, mousey), 0, 0, RED)
                target.update()
                target.draw()
                pygame.display.update()

            if targetpositionSet and not pygame.mouse.get_pressed()[0]:
                while not pygame.mouse.get_pressed()[0] and not shooterpositionSet:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()          
                    screen.fill(WHITE)
                    target.update()
                    target.draw()
                    mousex = pygame.mouse.get_pos()[0]
                    mousey = pygame.mouse.get_pos()[1]
                    shooter = Target((mousex, mousey), 0, 0, BLACK)
                    shooter.update()
                    shooter.draw()
                    pygame.display.update()
                shooterpositionSet = True
                distance = math.sqrt((target.x - mousex)**2 + (target.y - mousey)**2)
                dx = target.x - mousex
                dy = target.y - mousey
                angle = math.atan2(dy, dx)  # Calculate angle in radians

                v = distance * 0.14
                shooter = Projectile([mousex, mousey], v, math.radians(angle), 0)
                clock.tick(tickvalue)
            try:
                shooter.update()
                shooter.draw()
                pygame.display.update()
            except:
                pass



    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
