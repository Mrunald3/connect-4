from ._anvil_designer import CNNTemplate # Change this from TransformerTemplate
from anvil import *
import anvil.server
import anvil.js
import time

class CNN(CNNTemplate): 
  def __init__(self, **properties):
    self.init_components(**properties)

    # Initialize board state for the "Healthcare Vertical Mapping"
    self.board = [[0] * 7 for _ in range(6)]
    self.canvas_1.width = 580
    self.canvas_1.height = 580
    self.draw_board()

  def draw_board(self, custom_board=None):
    board_to_draw = custom_board if custom_board else self.board
    c = self.canvas_1
    c.clear_rect(0, 0, 580, 580)
    c.fill_style = "#005235" # Dark greenish theme
    c.fill_rect(0, 0, 580, 580)

    colors = {0: "white", 1: "red", 2: "yellow"}
    for r in range(6):
      for col in range(7):
        x = col * (580//7) + (580//14)
        y = r * (580//6) + (580//12)
        c.fill_style = colors[board_to_draw[r][col]]
        c.begin_path()
        c.arc(x, y, 35, 0, 2 * 3.14)
        c.fill()

  def on_column_click(self, col):
    # 1. Drop User Piece
    row = self.drop_piece_locally(col, 1)
    if row is not None:
      self.animate_fall(col, row, 1)
      # 2. Check Winner
      if anvil.server.call('check_winner_server', self.board, 1):
        alert("You Won!")
        return
        # 3. Get AI Move from Processing Layer
      ai_col = anvil.server.call('get_ai_move', self.board, self.selected_model)
      ai_row = self.drop_piece_locally(ai_col, 2)
      self.animate_fall(ai_col, ai_row, 2)

  def drop_piece_locally(self, col, piece):
    for r in range(5, -1, -1):
      if self.board[r][col] == 0:
        self.board[r][col] = piece
        return r
    return None