import pygame

class Text():
    # font: font that the text is written in
    # text: text to be written
    # pos: location of the text on the screen
    def __init__(self, font, text, pos, lineSpacing=2):
        self.font = font
        #self.text = text
        self.pos = pos
        self.lineSpacing = lineSpacing
        #self.surf = font.render(text,False,(50,50,50))
        #self.rect = self.surf.get_rect(topleft = pos)
        self.setText(text)

    def setText(self, text):
        if isinstance(text, str):
            lines = text.splitlines()
        else:
            lines = text

        if getattr(self, 'lines', None) != lines:
            self.lines = lines
            self.surfaces = [
                self.font.render(line, True, (50,50,50))
                for line in lines
            ]

    # pos: new pos of the button
    def updatePos(self, pos):
        self.pos = pos

    
    def draw(self, screen, text=None):
        if text:
            self.setText(text)
        x,y = self.pos
        for surf in self.surfaces:
            screen.blit(surf, (x, y))
            y += surf.get_height() + self.lineSpacing