# -*- coding: utf-8 -*-

#Import Modules
import os
import math
import pygame

from pygame.locals import *
# from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# global variables - values utilized
move_val = 4
target_fps = 60
resolution = (750,750)
border_buff1 = 0.015 
border_buff2 = .1
# global vars - initialized with zero values
fps = [0]
prey_loc = [0,0]
pred_loc = [0,0]

### FUNCTIONS

# function to load image
def load_image(name, colorkey=None):
    # make OS agnostic
    fullname = os.path.join(data_dir, name)
    # controlled error
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    # convert to match format and depth of display
    image = image.convert()
    # what color should be transparent?
    if colorkey is not None:
        if colorkey is -1:
            # use topleft most pixel color
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    # returns image & rect
    return image, image.get_rect()

# calc dev rectangle function
def calc_dev_rec(resolution, buff):
    rectres = [
            (resolution[0]*buff)
            , (resolution[1]*buff)
            , (resolution[0]-2*(resolution[0]*buff))
            , (resolution[1]-2*(resolution[1]*buff))
            ]
    return rectres

# rounded distance function: returns single whole integer
def r_dist(p0, p1):
    return round(math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2))

# raw slope between two points: returns [x,y] of slope
# points w/ slope of .5 could return [2,1] or [4,2] depending on distance
def raw_sl(p0, p1):
    res = [0,0]
    res[0], res[1] = (p1[0]-p0[0]), (p1[1]-p0[1])
    return res

# function to scale raw_sl output maximum to move value maximum
def scale_sl(p0, p1, move_val):
    # get raw slope coords
    raw_sl_out = raw_sl(p0,p1)
    # ensure they aren't zero
    if raw_sl_out[0] == 0:
        raw_sl_out[0] = 1
    if raw_sl_out[1] == 0:
        raw_sl_out[1] = 1
    # intit output 
    new_out = [0,0] 
    # absolute values of raw_sl_out
    abs_raw_sl = list(map(abs, raw_sl_out))
    
    # raw_sl_out has negative values?
    if raw_sl_out[0] < 0 or raw_sl_out[1] < 0:
        has_neg = "T"
    else:
        has_neg = "F"
    
    # what is max slope / abs_slope value
    # index of max slope value
    if has_neg == "T":
        rsl_max = max(abs_raw_sl)
        max_ind = abs_raw_sl.index(rsl_max)
        # init negative value binary indicators
        is_neg = [0,0]
        # what slope coords are negative
        if raw_sl_out[0] < 0: 
            is_neg[0] = 1
        if raw_sl_out[1] < 0: 
            is_neg[1] = 1
    else:
        rsl_max = max(raw_sl_out)
        max_ind = raw_sl_out.index(rsl_max)
    
    # which index is not the max value / abs value
    if max_ind == 0:
        other_ind = 1
    else:
        other_ind = 0
    
    # assign P/N move value to new_out[max_ind]
    if has_neg == "T":
        if is_neg[max_ind] == 1:
            new_out[max_ind] = move_val*-1
            perc_app = (move_val*-1)/raw_sl_out[max_ind]
        else:
            new_out[max_ind] = move_val
            perc_app = move_val/raw_sl_out[max_ind]
    else:
        new_out[max_ind] = move_val
        perc_app = move_val/raw_sl_out[max_ind]
    
    new_out[other_ind] = round(perc_app*raw_sl_out[other_ind])
    return(new_out)

### testing
#move_val = 2
#p0 = [579,440] # pred
#p1 = [440,506] # prey
#r_dist(p0,p1)
#raw_sl(p0,p1)
#scale_sl(p0,p1,move_val)
#
#p0 = [0, 0]
#p1 = [800, 111]
#raw_sl(p0,p1)
#scale_sl(p0,p1,move_val)

### CLASSES

class Prey(pygame.sprite.Sprite):
    # this is what will flee from curser input
    def __init__(self):
        # call Sprite intializer
        pygame.sprite.Sprite.__init__(self)
        # loads image & rect
        self.image, self.rect = load_image('redC.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centerx = resolution[0]/2
        self.rect.centery = resolution[1]/2
        self.move = move_val
        self.last_dir = [0,0]
        buff = border_buff1
        self.boundLRTB = [
                (resolution[0]*buff)
                , (resolution[0]-(resolution[0]*buff))
                , (resolution[1]*buff)
                , (resolution[1]-(resolution[1]*buff))
                ]
        
    def update(self):
        self._flee()
        self._checkbounds()
        
    def _checkbounds(self):
        ybords = 0
        xbords = 0
        if self.rect.left < self.boundLRTB[0] or \
            self.rect.right > self.boundLRTB[1] or \
            self.rect.top < self.boundLRTB[2] or \
            self.rect.bottom > self.boundLRTB[3]:
                
                # flag horizontal and vertical breaches
                if self.rect.left < self.boundLRTB[0] or self.rect.right > self.boundLRTB[1]:
                    xbords = 1    
                #  vertical boundries
                if self.rect.top < self.boundLRTB[2] or self.rect.bottom > self.boundLRTB[3]:
                    ybords = 1
                    
                # correct horizontal, vertical, and both breaches
                if xbords == 1 and ybords == 0:
                    newpos = self.rect.move([-self.last_dir[0], self.last_dir[1]])
                    #self.image = pygame.transform.flip(self.image, 1, 0)
                elif xbords == 0 and ybords == 1:
                    newpos = self.rect.move([self.last_dir[0], -self.last_dir[1]])
                    #self.image = pygame.transform.flip(self.image, 0, 1)
                elif xbords == 1 and ybords == 1:
                    newpos = self.rect.move([-self.last_dir[0]*2, -self.last_dir[1]*2])
                    
                # move rect
                self.rect = newpos

                # update global with location
                prey_loc[0], prey_loc[1] = self.rect.centerx, self.rect.centery
            
    def _flee(self):
       # is pred close to prey?
       # current distance
       cd = r_dist(pred_loc, prey_loc)
       
       if cd < 200:
           scale_out = scale_sl(pred_loc, prey_loc, move_val)
           
           # set new position to scaled out
           if cd < 100:
               newpos = self.rect.move(scale_out[0]*2, scale_out[1]*2)
           else:
               newpos = self.rect.move(scale_out[0], scale_out[1])
               
           # move rect
           self.rect = newpos
           # update last direction
           self.last_dir = [scale_out[0], scale_out[1]]
           # update global with location
           prey_loc[0], prey_loc[1] = self.rect.centerx, self.rect.centery
             
            
class Pred(pygame.sprite.Sprite):
    # this is what will do chasing, controlled by input
    def __init__(self):
        # call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        # loads image & rect
        self.image, self.rect = load_image('blueC.png', -1)

    def update(self):
        # control the Predator with mouse
        pos = pygame.mouse.get_pos()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
        pred_loc[0], pred_loc[1] = pos[0], pos[1]


### Development helper classes/functions/tools
class DevStats(pygame.sprite.Sprite):
    def __init__(self):
        # call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.color = Color("gray")
    
    def update(self):
        self.textlist = [
                " FPS: " + str(fps)
                , " Pred_Loc: " + str(pred_loc)
                , " Prey_Loc: " + str(prey_loc)
                , " Distance: " + str(r_dist(pred_loc, prey_loc))
                , " Raw_Slope: " + str(raw_sl(pred_loc, prey_loc))
                , " Scaled_Slope: " + str(scale_sl(pred_loc, prey_loc, move_val))
                ]
        
        width = max(self.font.size(line)[0] for line in self.textlist)
        height = self.font.get_linesize()
        
        self.image = pygame.Surface(
                (width+3, height*len(self.textlist))
                , SRCALPHA)
        
        for y, line in enumerate(self.textlist):
            text_surf = self.font.render(line, True, self.color)
            self.image.blit(text_surf, (0, y*height))
            
        self.rect = self.image.get_rect()


def DevShapes(screen, resolution, border_buff1, border_buff2):
    # left, top, right, bottom
    borders1 = calc_dev_rec(resolution, border_buff1)
    borders2 = calc_dev_rec(resolution, border_buff2)
            
    pygame.draw.rect(screen, Color("black"), borders1, 2)
    pygame.draw.rect(screen, Color("gray"), borders2, 2)


def main():
    # Initialize Everything
    pygame.init()
    # screen size
    screen = pygame.display.set_mode(resolution)
    # hide mouse
    pygame.mouse.set_visible(0)
    
    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    

    # Display The Background
    screen.blit(background, (0, 0))
    
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    prey = Prey()
    pred = Pred()
    devstats = DevStats()
    allsprites = pygame.sprite.RenderPlain((prey, pred, devstats))

    # Main Loop
    going = True
    while going:
        clock.tick(target_fps)
        fps[0] = round(clock.get_fps())

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
        
        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        
        DevShapes(screen, resolution, border_buff1, border_buff2)
        pygame.display.flip()

    pygame.quit()

# call the 'main' function when this script is executed
if __name__ == '__main__':
    main() 