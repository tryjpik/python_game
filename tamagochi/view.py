import pygame, random


class Actor(pygame.sprite.Sprite):
    boredom_delta = 0.05
    hunger_delta = 0.25
    tiredness_delta = 0.15

    max_char_value = 1000

    boredom_threshold = 200
    hunger_threshold = 100
    tiredness_threshold = 300

    progress_bar_widht = 300
    progress_bar_height = 30

    action_time = 20

    normal_actor = pygame.image.load("smile.jpg")
    sad_actor = pygame.image.load("bored.png")

    play_actor = pygame.image.load("gaming.jpg")
    feed_actor = pygame.image.load("eating.jpg")
    sleep_actor = pygame.image.load("sleeping.jpg")

    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.normal_actor
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
                            
        self.boredom = 100      
        self.hunger = 200                   
        self.tiredness = 300                   
        self.is_sleeping = False                    
                            
        self.boredom_progress_bar = ProgressBar(self.progress_bar_widht, self.progress_bar_height, 570, 50, self.max_char_value, self.boredom)                    
        self.hunger_progress_bar = ProgressBar(self.progress_bar_widht, self.progress_bar_height, 570, 95, self.max_char_value, self.hunger)
        self.tiredness_progress_bar = ProgressBar(self.progress_bar_widht, self.progress_bar_height, 570, 140, self.max_char_value, self.tiredness)                    
        self.actions = []                    

                            
    def update(self, surface):                        
        self.boredom = max(1, self.boredom - self.boredom_delta)                       
        self.hunger = max(1, self.hunger - self.hunger_delta)                      
        if self.is_sleeping == True:                       
            self.tiredness = self.max_char_value
        else:
            self.tiredness = max(1, self.tiredness - self.tiredness_delta)
        self.boredom_progress_bar.update(self.boredom)
        self.hunger_progress_bar.update(self.hunger)
        self.tiredness_progress_bar.update(self.tiredness)

        self.boredom_progress_bar.draw(surface, (174, 74, 87))
        self.hunger_progress_bar.draw(surface, (206, 134, 39))
        self.tiredness_progress_bar.draw(surface, (125, 181, 205))

        if not(self.is_sleeping):
            if len(self.actions) == 0:            
                if self.boredom <=self.boredom_threshold or \
                self.hunger <=self.hunger_threshold or \
                self.tiredness <=self.tiredness_threshold:
                    self.image = self.sad_actor
                else:
                    self.image = self.normal_actor     
            else:
                action = self.actions[0]  
                if (action[0] == 0):
                    self.image = self.play_actor
                elif (action[0] == 1):
                        self.image = self.feed_actor
                self.actions[0][1] -= 1
                print(self.actions[0][1])
                if self.actions[0][1] == 0:
                    self.actions.pop(0)

    def play(self):
        if not(self.is_sleeping):
            self.boredom = self.max_char_value
            self.boredom_progress_bar.update(self.boredom)
            self.actions.append([0,self.action_time])

    def feed(self):
        if not(self.is_sleeping):
            self.hunger = self.max_char_value
            self.hunger_progress_bar.update(self.hunger)
            self.actions.append([1, self.action_time])

    def sleep(self):
        self.tiredness = self.max_char_value
        self.tiredness_progress_bar.update(self.tiredness)
        if self.is_sleeping ==True:
            self.is_sleeping = False
            self.image = self.normal_actor
        else:
            self.is_sleeping = True
            self.image = self.sleep_actor


class ProgressBar():
    def __init__(self, width, height, x_pos, y_pos, max_val, current_percent = 0):
        self.width = width
        self.height = height
        self.current_percent = current_percent
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.max_val = max_val

    def update(self, current_val):
        self.current_percent = current_val / self.max_val

    def draw(self, surface, color):
        filled = self.current_percent * self.width        
        pygame.draw.rect(surface, color, pygame.Rect(self.x_pos, self.y_pos, filled, self.height))
        pygame.draw.rect(surface, (0, 0, 0,), pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 5)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cursor.png") 
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

        

