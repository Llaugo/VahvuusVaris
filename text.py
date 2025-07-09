import pygame

class Text():
    # font: font that the text is written in
    # text: text to be written
    # pos: location of the text (topleft) on the screen
    # color: color of the text (default black)
    # lineSpacing: spacing of multiline text
    def __init__(self, font, text, pos, color=(0,0,0), lineSpacing=2):
        self.font = font
        self.pos = pos
        self.color = color
        self.lineSpacing = lineSpacing
        self.lines = []     # Text rows as list rows
        self.surfaces = []  # Rendered text lines
        self.setText(text)

    # Set the text / modify the text
    def setText(self, text):
        if isinstance(text, str):   # Make str to list with newlines as breaks
            lines = text.splitlines()
        else:                       # Or just accept a list as is
            lines = text
        if self.lines != lines: # If given text has changed, log new text and render it
            self.lines = lines
            self.surfaces = [ self.font.render(line, True, self.color) for line in lines ]

    # pos: new pos of the button
    # center: alligns text to left if False and to center if True
    def updatePos(self, pos, center=False):
        if center:
            # Find the longest line, to center the text on
            longest = 0
            for surf in self.surfaces:
                if surf.get_width() > longest:
                    longest = surf.get_width()
            self.pos = (pos[0] - longest/2, pos[1] - len(self.surfaces)*self.surfaces[0].get_height()/2) # Set pos
        else:
            self.pos = pos

    # Draw the text on the screen
    # text: a possible modification to the text
    def draw(self, screen, text=None):
        if text: # Modify text
            self.setText(text)
        x,y = self.pos
        for surf in self.surfaces: # draw every line/surface on top of each other
            screen.blit(surf, (x, y))
            y += surf.get_height() + self.lineSpacing