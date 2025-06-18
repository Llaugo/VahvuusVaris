import pygame

class Text():
    # font: font that the text is written in
    # text: text to be written
    # pos: location of the text on the screen
    def __init__(self, font, text, pos):
        self.font = font
        self.text = text
        self.pos = pos
        self.surf = font.render(text,False,(50,50,50))
        self.rect = self.surf.get_rect(center = pos)

    # pos: new pos of the button
    def updatePos(self, pos):
        self.pos = pos
        self.rect = self.surf.get_rect(center = (pos))
    
    def draw(self, screen, text = None):
        if text and text != self.text:
            self.text = text
            self.surf = self.font.render(text,False,(50,50,50))
            self.rect = self.surf.get_rect(center = self.pos)
        screen.blit(self.surf,self.rect)