from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.users.login_with_form() 

    # Initialize game state
    self.current_player = 1 # 1 for You, 2 for Opponent
    self.board = [[0] * 7 for _ in range(6)] # 6 rows, 7 columns
    self.make_board_ui()

  def make_board_ui(self):
    # Clear the existing grid if any
    self.column_panel_board.clear()

    # Create 7 buttons representing columns to "drop" chips
    for i in range(7):
      btn = Button(text="↓", tag=i)
      btn.set_event_handler('click', self.drop_chip)
      self.column_panel_board.add_component(btn)

  def drop_chip(self, **event_args):
    column = event_args['sender'].tag
    # Call a server function to process the move (The "Processing Layer")
    result = anvil.server.call('process_move', self.board, column, self.current_player)

    if result['success']:
      self.board = result['new_board']
      self.refresh_board_display()
      if result['winner']:
        Notification(f"Player {result['winner']} Wins!").show()
    else:
      Notification("Column full!").show()

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.users.login_with_form() 

    # Initialize Game State
    self.board = [[0] * 7 for _ in range(6)]
    self.current_player = 1

    # Only try to build the UI if the panel exists
    if hasattr(self, 'column_panel_board'):
      self.make_board_ui()
    else:
      print("Please add a ColumnPanel named 'column_panel_board' in the Design view.")

  def make_board_ui(self):
    self.column_panel_board.clear()
    # Create 7 drop-buttons (representing the 7 healthcare sub-verticals) [cite: 40]
    for i in range(7):
      btn = Button(text="Drop", tag=i, role='secondary')
      btn.set_event_handler('click', self.drop_chip)
      self.column_panel_board.add_component(btn)
