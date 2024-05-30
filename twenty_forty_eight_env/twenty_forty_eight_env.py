import pygame as pg
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from .env_utils import WINDOW_SIZE, BG_COLOR, COLOR_TABLE, text_to_screen

# game function mostly based on www.geeksforgeeks.org/2048-game-in-python/
def rand_new_item(table: np.array):
    empty_spots = []
    for r in range(4):
        for c in range(4):
            if table[r][c] == 0:
                empty_spots.append((r, c))
    if len(empty_spots) >= 1:
        fill = 2 if np.random.rand() > 0.5 else 4
        row, col = empty_spots[np.random.randint(low=0, high=len(empty_spots))]
        table[row][col] = fill
    
def check_game_over(table: np.array):
    for r in range(4):
        for c in range(4):
            if table[r][c] == 0:
                return False
    return True

def compress(table: np.array):
    changed = False
    new_table = np.zeros((4, 4), dtype=np.float32)
    for r in range(4):
        p = 0
        for c in range(4):
            if table[r][c] != 0:
                new_table[r][p] = table[r][c]
                if c != p:
                    changed = True
                p += 1
    return new_table, changed

def merge(table: np.array):
    changed = False
    merged_sum = 0
    for r in range(4):
        for c in range(3):
            if table[r][c] == table[r][c+1] and table[r][c] != 0:
                table[r][c] = table[r][c]*2
                table[r][c+1] = 0
                merged_sum += table[r][c]
                changed = True
    return table, merged_sum, changed

def left(table: np.array):
    new_table, changed1 = compress(table)
    new_table, rew, changed2 = merge(new_table)
    new_table, _ = compress(new_table)
    return new_table, rew, changed1 or changed2

def right(table: np.array):
    new_table = np.flip(table, axis=1)
    new_table, rew, changed = left(new_table)
    new_table = np.flip(new_table, axis=1)
    return new_table, rew, changed

def up(table: np.array):
    new_table = np.transpose(table)
    new_table, rew, changed = left(new_table)
    new_table = np.transpose(new_table)
    return new_table, rew, changed

def down(table: np.array):
    new_table = np.transpose(table)
    new_table, rew, changed = right(new_table)
    new_table = np.transpose(new_table)
    return new_table, rew, changed
    

class TwentyFortyEightEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}
    
    def __init__(self, render_mode=None):
        pg.init()
         
        self.observation_space = spaces.Box(low=0, high=131_072, shape=[4, 4]) # observation is the 4x4 grid, 131072 is the largest possible tile
        self.action_space = spaces.Discrete(4)
        
        self.action_to_func = {
            0: up,
            1: down,
            2: left,
            3: right
        }
        
        square_size = (WINDOW_SIZE // 4) - 10
        square_locs = [[(x*square_size + x*10 + 5, y*square_size + y*10 + 5) for x in range(4)] for y in range(4)]
        self.rects = [[pg.Rect(square_locs[i][j][0], square_locs[i][j][1], square_size, square_size) for i in range(4)] for j in range(4)]
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.display = None
        self.clock = None
        
    def _get_obs(self):
        return self.table
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.table = np.zeros((4, 4), dtype=np.float32)
        rand_new_item(self.table)
        
        if self.render_mode == "human":
            self._init_render()
            self._render_frame()
        
        return self.table, {}
    
    def step(self, action: int):
        if action <= 3:
            self.table, rew, changed = self.action_to_func[action](self.table)
            if changed:
                rand_new_item(self.table)
        else:
            print("warning: invalid input")
            rew = 0
            
        if self.render_mode == "human":
            self._render_frame()
            
        done = check_game_over(self.table)
        obs = self._get_obs()
            
        return obs, rew, done, False, {}
        
    def _init_render(self):
        pg.display.init()
        self.display = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pg.display.set_caption("2048")
        self.clock = pg.time.Clock()
        
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def _render_frame(self):
        canvas = pg.Surface((WINDOW_SIZE, WINDOW_SIZE))
        canvas.fill(BG_COLOR)

        for i in range(4):
            for j in range(4):
                pg.draw.rect(canvas, COLOR_TABLE[self.table[i][j]], self.rects[i][j])
                
        if self.render_mode == "human":
            self.display.blit(canvas, canvas.get_rect())
                    
            for i in range(4):
                for j in range(4):
                    text_to_screen(self.display, int(self.table[i][j]), self.rects[i][j].centerx, self.rects[i][j].centery)
                    
            pg.event.pump()
            pg.display.update()
            self.clock.tick(self.metadata['render_fps'])
            
        else:
            return np.array(pg.surfarray.pixels3d(canvas))
        
    def close(self):
        if self.window is not None:
            pg.display.quit()
            pg.quit()