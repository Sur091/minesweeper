import pygame as py
from random import random


def draw_board(surface):
    for a in range(0, width + tile, tile):
        py.draw.line(surface, (0, 0, 0), (a, 0), (a, height))
    for b in range(0, height + tile, tile):
        py.draw.line(surface, (0, 0, 0), (0, b), (width, b))


class Box:
    percent_of_bomb = 0.05  # 0.144

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.opened = False
        self.bomb = random() < Box.percent_of_bomb
        self.number = 0

    def show(self, surface):
        if not self.opened:
            py.draw.rect(surface, (255, 255, 255), py.Rect(self.x * tile, self.y * tile, tile, tile))
            py.draw.rect(surface, (0, 0, 0), py.Rect(self.x * tile, self.y * tile, tile, tile), 1)
        elif self.bomb:
            center = self.x * tile + tile // 2, self.y * tile + tile // 2
            py.draw.circle(surface, (162, 20, 42), center, tile // 3)
        elif self.number > 0:
            text = font.render(str(self.number), True, (0, 0, 0))
            surface.blit(text, (self.x * tile + 8, self.y * tile + 4))
        py.draw.rect(surface, (0, 0, 0), py.Rect(self.x * tile, self.y * tile, tile, tile), 1)

    def neighbours(self, lst1):
        lst = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if -1 < self.x + a < width // tile and -1 < self.y + b < height // tile and not (a == 0 and b == 0):
                    lst.append(lst1[a + self.x][b + self.y])
        return lst


class Board:
    def __init__(self):
        lst = []
        for a in range(width // tile):
            lst.append([Box(a, b) for b in range(height // tile)])
        for a in lst:
            for b in a:
                b.number = sum(1 for box in b.neighbours(lst) if box.bomb)
        self.board = lst

    def show(self, surface):
        for a in self.board:
            for b in a:
                b.show(surface)

    def update(self):
        for a in self.board:
            for b in a:
                if b.opened and b.bomb:
                    pass
                    # print("Game Over")

    def open(self, box, surface):
        box.opened = True
        window.fill((200, 200, 200))
        self.show(surface)
        py.display.update()
        clock.tick(frame_rate)
        if box.number == 0:
            for neighbour in box.neighbours(self.board):
                if not neighbour.opened:
                    self.open(neighbour, surface)


py.init()

width, height = 600, 300
tile = 30
window = py.display.set_mode((width, height))
clock = py.time.Clock()
frame_rate = 60

running = True

player1 = Board()
font = py.font.Font('freesansbold.ttf', 25)

while running:
    clock.tick(frame_rate)
    window.fill((200, 200, 200))

    draw_board(window)
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            x_, y_ = pos[0] // tile, pos[1] // tile
            player1.open(player1.board[x_][y_], window)
    player1.show(window)
    player1.update()
    py.display.update()
