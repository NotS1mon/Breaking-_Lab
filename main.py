import pygame
import sys
from pygame import mixer
from settings import *
from level import *

class Game:
    def __init__(self):
          
        # Allgemein
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Breaking Lab')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.start_time = 0  # Startzeit des Timers 
        self.timer_font = pygame.font.SysFont(None, 36)
        self.timer_stopped = False
        self.showing_start_screen = True 
        
        # Musik
        mixer.init()
        mixer.music.load('Music/Music1.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play()
        music_end_event = pygame.USEREVENT + 1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.showing_start_screen:
                    # Wenn der Spieler auf den Startbildschirm klickt, wird das Spiel gestartet
                    self.start_game()

            self.screen.fill('lightgrey')
            if self.showing_start_screen:
                self.show_start_screen()
            else:
                self.level.run()
                self.level.Professor.draw_chemical_count(self.screen)  # Anzeige der Anzahl der eingesammelten Chemikalien
                
                if not self.timer_stopped:  # Timer nur ausführen, wenn er nicht gestoppt wurde
                    self.draw_timer()
                

                if self.level.Professor.chemikalien_counter >= 7 and not self.timer_stopped:  # Wenn 7 Chemikalien aufgesammelt wurden
                    self.stop_timer()  # Timer anhalten und Endbildschirm anzeigen
                    self.show_end_screen()

            pygame.display.update()
            self.clock.tick(FPS)

    # Festlegen und Anzeigen des Timers
    def draw_timer(self):
        current_time = pygame.time.get_ticks() - self.start_time
        minutes = current_time // 60000
        seconds = (current_time // 1000) % 60
        milliseconds = current_time % 1000  # Millisekunden berechnen
        timer_text = self.timer_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 50))

    def stop_timer(self):
        self.timer_stopped = True
        
    def show_end_screen(self):
        self.screen.fill('black')
        current_time = pygame.time.get_ticks() - self.start_time
        minutes = current_time // 60000
        seconds = (current_time // 1000) % 60
        milliseconds = current_time % 1000  # Millisekunden berechnen
        timer_text = self.timer_font.render(f"Time taken: {minutes:02d}:{seconds:02d}.{milliseconds:03d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH // 2 - 150, HEIGTH // 2 - 50))
        pygame.display.update()
        pygame.time.wait(5000)  # 5 Sekunden warten, bevor das Spiel beendet wird
        pygame.quit()
        sys.exit()

    def show_start_screen(self):
        self.screen.fill('black')
        start_font = pygame.font.SysFont(None, 48)
        start_text = start_font.render("Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
        self.screen.blit(start_text, start_rect)

    def start_game(self):
        self.start_time = pygame.time.get_ticks()  # Startzeit des Timers setzen
        self.showing_start_screen = False  # Startbildschirm ausblenden

if __name__ == '__main__':
    game = Game()
    game.run()