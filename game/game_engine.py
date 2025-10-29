import pygame
from .paddle import Paddle
from .ball import Ball
import time

# Initialize mixer and load sounds
pygame.mixer.init()
PADDLE_HIT_SOUND = pygame.mixer.Sound("assets/paddle_hit.wav")
WALL_BOUNCE_SOUND = pygame.mixer.Sound("assets/wall_bounce.wav")
SCORE_SOUND = pygame.mixer.Sound("assets/score.wav")

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()

        # Wall bounce sound
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
            self.ball.velocity_y *= -1
            WALL_BOUNCE_SOUND.play()

        # Paddle collision
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x *= -1
            PADDLE_HIT_SOUND.play()
        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x *= -1
            PADDLE_HIT_SOUND.play()

        # Scoring and sound
        if self.ball.x <= 0:
            self.ai_score += 1
            SCORE_SOUND.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            SCORE_SOUND.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
            """Check if any player reached 5 points and display winner."""
            if self.player_score >= 5:
                winner_text = self.font.render("Player Wins!", True, (255, 255, 255))
                screen.blit(winner_text, (self.width // 2 - 180, self.height // 2 - 40))
                pygame.display.flip()
                self.game_over = True

            elif self.ai_score >= 5:
                winner_text = self.font.render("AI Wins!", True, (255, 255, 255))
                screen.blit(winner_text, (self.width // 2 - 120, self.height // 2 - 40))
                pygame.display.flip()
                self.game_over = True

            # If game over, delay for a few seconds before quitting
            if self.game_over:
                time.sleep(3)
                pygame.quit()
                quit()