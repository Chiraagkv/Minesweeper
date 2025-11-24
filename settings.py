#(Width,height,mines)
difficulty_settings = {
    'Easy': (9, 9, 10),    
    'Medium': (15, 15, 40),  
    'Hard': (20, 20, 99),    
}

tile_size = 40

#Colors for various parts of game
COLOR_STATUS_BAR = (58, 100, 52)      
COLOR_UNCLICKED_LIGHT = (170, 215, 81)  
COLOR_UNCLICKED_DARK = (162, 209, 73)  

# Dual colors for revealed tiles
COLOR_REVEALED_LIGHT = (229, 194, 159) 
COLOR_REVEALED_DARK = (217, 185, 153)  

COLOR_MINE = (255, 0, 0)              
COLOR_TEXT = (25, 25, 25)             
COLOR_FLAG = (200, 30, 30)            
COLOR_FLAG_POLE = (100, 100, 100)     
COLOR_BOMB = (170, 33, 33)            
COLOR_ICON = (255, 255, 100)          #timer 
COLOR_POPUP_BG = (80, 80, 80)
COLOR_BUTTON = (100, 150, 100)
COLOR_BUTTON_HOVER = (120, 170, 120)
COLOR_BORDER = (100, 130, 70)         

NUMBER_COLORS = {
    1: (0, 0, 255),    # blue
    2: (0, 128, 0),    # green
    3: (255, 0, 0),    # red
    4: (0, 0, 128),    # dark blue
    5: (128, 0, 0),    # maroon
    6: (0, 128, 128),  # teal
    7: (0, 0, 0),      # black
    8: (128, 128, 128) # grey
}