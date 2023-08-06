import pygame

pygame.init()


class DoubleStateSim:
    def __init__(self, screen, font:str, messages: tuple, colors: tuple, xy: tuple, size:tuple, default: int):
        self.screen = screen
        self.messages = messages
        self.colors = colors
        self.xy = xy
        self.state = default
        self.size = size
        self.rect = pygame.Rect(self.xy[0],self.xy[1],size[0],size[1])
        self.font = font
        self.font = pygame.font.SysFont(self.font,size[0])
        self.text1 = self.font.render(self.messages[self.state], False, self.colors[2], self.colors[self.state])
        self.text2 = self.font.render(self.messages[self.state+1], False, self.colors[2], self.colors[self.state+1])
        self.text = [self.text1,self.text2]

    def Draw(self):
        pygame.draw.rect(self.screen, self.colors[self.state],self.rect)
        self.screen.blit(self.text[self.state],self.rect.topleft)

    def Detect(self, mousexy, event):
        x = mousexy[0]
        y = mousexy[1]
        if ((x >= self.rect.topleft[0]) and (x <= self.rect.bottomright[0])) and (
                (y >= self.rect.topleft[1]) and (y <= self.rect.bottomright[1])):

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state==1:
                    self.state = 0
                else:
                   self.state+=1