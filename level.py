import pygame 
from settings import *
from Objekte import *
from player import *

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map() # Mein Sprite wird erschaffen
        
    # Erstellung der Map und deklaration von "x,p,c,t"
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Wand((x,y),[self.visible_sprites,self.obstacle_sprites]) 
                if col == 'p':
                    self.Professor = Professor((x,y),[self.visible_sprites],self.obstacle_sprites)
                if col == 'c':
                    Chemical((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 't':
                    Tisch((x,y),[self.visible_sprites,self.obstacle_sprites])
                    

    def run(self):
        # update und drawn des Spiels
        self.visible_sprites.custom_draw(self.Professor)
        self.visible_sprites.update()


class Camera(pygame.sprite.Group):
    def __init__(self):

        # generelle Einstellungen  
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self,Professor):

        self.offset.x = Professor.rect.centerx - self.half_width
        self.offset.y = Professor.rect.centery - self.half_height

        # für die sprites in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
