import anvil.server

@anvil.server.callable
def check_winner_server(board, piece):
  # Check horizontal
  for c in range(4):
    for r in range(6):
      if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
        return True
    # Check vertical
  for c in range(7):
    for r in range(3):
      if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
        return True
    # Add diagonal checks similarly...
  return False

@anvil.server.callable
def get_ai_move(board, model_type):
  # This represents your Competitive Intelligence Engine [cite: 123, 220]
  import random
  # In production, this would call your Transformer/CNN weights
  return random.randint(0, 6)
