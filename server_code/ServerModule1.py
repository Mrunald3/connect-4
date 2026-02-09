import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def check_winner_server(board, piece):
  # Optimized 4-in-a-row detection
  for r in range(6):
    for c in range(4):
      if all(board[r][c+i] == piece for i in range(4)): return True
  for r in range(3):
    for c in range(7):
      if all(board[r+i][c] == piece for i in range(4)): return True
  for r in range(3):
    for c in range(4):
      if all(board[r+i][c+i] == piece for i in range(4)): return True
  for r in range(3, 6):
    for c in range(4):
      if all(board[r-i][c+i] == piece for i in range(4)): return True
  return False

@anvil.server.callable
def get_ai_move(board):
  import random
  valid_cols = [c for c in range(7) if board[0][c] == 0]
  return random.choice(valid_cols) if valid_cols else None