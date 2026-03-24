import pygame
from newMain import draw_text

def pauseScreen():
	draw_text("Game Paused.. Press ESCAPE to Unpause.", pause_font, WHITE, screenWidth // 2 - 230, screenHeight // 2)
		
