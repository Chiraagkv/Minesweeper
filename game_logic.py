import pygame
import random
import sys
import time
import os
import math



class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'safe'  # safe, flagged, revealed, mine_hit,flower
        self.clickable = True
        self.value = 0       # -1 for mine, 0-8 for number of adjacent mines

    def set_value(self, n):
        self.value = n

def mines(start_tile, tiles, n):
    w = len(tiles)
    h = len(tiles[0])
    mines_set = set()

    sx, sy = start_tile.x, start_tile.y
    blocked = set([(sx + temp_x, sy + temp_y) for temp_x in [-1, 0, 1] for temp_y in [-1, 0, 1] 
                          if 0 <= sx + temp_x < w and 0 <= sy + temp_y < h])

    while len(mines_set) < n:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if (x, y) in blocked:
            continue
        mines_set.add((x, y))

    for (x, y) in mines_set:
        tiles[x][y].set_value(-1)

    return tiles


def recursive_fill(tiles, tile):
    #reveals adjacent tiles if the current tile value = 0
    #Clearing
    #
    w = len(tiles)
    h = len(tiles[0])
    x, y = tile.x, tile.y

    #already revealed (clickable=false or a flag
    if not tile.clickable or tile.state == 'flagged':
        return tiles
    
    #current tile
    tile.clickable = False
    tile.state = 'revealed'

    #number (1-8) or a mine (-1), stop
    if tile.value != 0:
        return tiles
    
    #neighbors if value is 0
    for temp_x in [-1, 0, 1]:
        for temp_y in [-1, 0, 1]:
            if temp_x == 0 and temp_y == 0:
                continue

            nx, ny = x + temp_x, y + temp_y

            if 0 <= nx < w and 0 <= ny < h:
                n = tiles[nx][ny]
                recursive_fill(tiles, n)

    return tiles

def find_number(tiles, tile):
    #number of adjacent mines for a safe tile
    x = tile.x
    y = tile.y
    w = len(tiles)
    h = len(tiles[0])
    c = 0
    for temp_x in [-1, 0, 1]:
        for temp_y in [-1, 0, 1]:
            if temp_x == 0 and temp_y == 0:
                continue

            nx, ny = x + temp_x, y + temp_y

            if 0 <= nx < w and 0 <= ny < h:
                n = tiles[nx][ny]
                if n.value == -1:
                    c += 1
    return c

def compute_numbers(tiles):
    #sets the numerical value for all non-mine tiles
    for row in tiles:
        for t in row:
            if (t.value != -1):
                t.value = find_number(tiles, t)
    return tiles

def initialise(tiles, click, n, seed=None):
    #gen/set seed
    if seed is None: seed = int(time.time())
    random.seed(seed)

    #Reveal the board
    tiles = mines(click, tiles, n)
    tiles = compute_numbers(tiles)
    tiles = recursive_fill(tiles, click)
    return tiles,seed

def reveal_tile(tiles, tile):
    if not tile.clickable or tile.state == 'flagged':
        return "ok"

    if tile.value == -1:
        tile.clickable = False
        tile.state = 'mine_hit'
        return "mine"

    if tile.value == 0:
        recursive_fill(tiles, tile)
    else:
        tile.clickable = False
        tile.state = 'revealed'

    return "ok"

def flag_tile(tile):
    if tile.clickable:
        if tile.state == 'safe':
            tile.state = 'flagged'
        elif tile.state == 'flagged':
            tile.state = 'safe'
