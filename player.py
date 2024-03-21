import pygame 
from settings import *
from Objekte import Chemical

screen_height = 720

# Erstellung des Professors
class Professor(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('bilder/prof_r.png').convert_alpha() 
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.chemikalien_counter = 0
        self.font = pygame.font.Font(None, 36)  # Schriftart und größe festlegen
        
    # Bewegung des Professors 
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.image = pygame.image.load('bilder/prof_r.png').convert_alpha()
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.image = pygame.image.load('bilder/prof_l.png').convert_alpha()
        else:
            self.direction.x = 0

            
    # Kollisionen und Hitboxen
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
     
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if isinstance(sprite, Chemical):  # Überprüfen, ob es sich um eine Chemikalie handelt
                        self.pickup_chemical(sprite)  # Die Chemikalie einsammeln
                    else:
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if isinstance(sprite, Chemical):  # Überprüfen, ob es sich um eine Chemikalie handelt
                        self.pickup_chemical(sprite)  # Die Chemikalie einsammeln
                    else:
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

    def pickup_chemical(self, chemical):
        chemical.kill()  # Chemikalie entfernen
        self.chemikalien_counter += 1
        
    # Anzeigen der aufgsammleten Chemikalien 
    def draw_chemical_count(self, screen):
        text = self.font.render(f"Chemikalien: {self.chemikalien_counter}/7", True, (255, 255, 255))  # Text definieren 
        screen.blit(text, (10, 10))  # Den Text auf dem Bildschirm anzeigen 


    def update(self):
        self.input()
        self.move(self.speed)