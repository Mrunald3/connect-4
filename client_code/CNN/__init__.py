from ._anvil_designer import CNNTemplate
from anvil import *
import anvil.server
import anvil.js
import time

class CNN(CNNTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # --- UI SETUP ---
    self.content_panel.clear() 
    self.content_panel.background = "white" #

    # ROOT CONTAINER: Centers the whole game stack
    self.main_container = ColumnPanel(width=600)
    self.content_panel.add_component(self.main_container)

    # 1. BUTTON GRID: Force 1 row for all 7 buttons
    self.grid = GridPanel()
    self.main_container.add_component(self.grid)

    self.buttons = []
    for i in range(7):
      # Red background, white text
      btn = Button(text=str(i+1), 
                   tag=i, 
                   background='red', 
                   foreground='white', 
                   role='raised', 
                   bold=True,
                   font_size=16)
      btn.set_event_handler('click', self.on_column_click)
      # col_xs=i locks them into one row to prevent button 7 dropping
      self.grid.add_component(btn, row='A', col_xs=i, width_xs=1)
      self.buttons.append(btn)

      # 2. BOARD CANVAS
    self.canvas_1 = Canvas(width=580, height=580)
    self.main_container.add_component(self.canvas_1)

    # 3. CENTERED STATUS & RESTART
    self.status_panel = FlowPanel(align='center')
    self.main_container.add_component(self.status_panel)
    self.turn_label = Label(text="Your Turn 🔴", foreground="black", font_size=20)
    self.status_panel.add_component(self.turn_label)

    self.reset_panel = FlowPanel(align='center')
    self.main_container.add_component(self.reset_panel)
    self.reset_button = Button(text="Restart Game", role='secondary-color')
    self.reset_button.set_event_handler('click', self.restart_click)
    self.reset_panel.add_component(self.reset_button)

    # --- STATE & INITIAL DRAW ---
    self.board = [[0] * 7 for _ in range(6)]
    self.canvas_1.set_event_handler('show', lambda **e: self.draw_board())

    # Add to CNN form __init__
    self.back_button = Button(text="Main Menu", role='link')
    self.back_button.set_event_handler('click', lambda **e: open_form('Home'))
    self.main_container.add_component(self.back_button)

  def draw_board(self, custom_board=None):
    board_to_draw = custom_board if custom_board else self.board
    c = self.canvas_1
    c.fill_style = "#0000FF" # Blue Board Frame
    c.fill_rect(0, 0, 580, 580)

    colors = {0: "white", 1: "red", 2: "yellow"} # Holes match white background
    for r in range(6):
      for col in range(7):
        x = col * (580//7) + (580//14)
        y = r * (580//6) + (580//12)
        c.fill_style = colors[board_to_draw[r][col]]
        c.begin_path()
        c.arc(x, y, 35, 0, 2 * 3.14159)
        c.fill()

  def animate_fall(self, col, final_row, piece):
    c = self.canvas_1
    x = col * (580//7) + (580//14)
    target_y = final_row * (580//6) + (580//12)
    color = "red" if piece == 1 else "yellow"
    for y in range(0, target_y, 30): 
      c.clear_rect(0, 0, 580, 580)
      self.draw_board() 
      c.fill_style = color
      c.begin_path()
      c.arc(x, y, 35, 0, 2 * 3.14159)
      c.fill()
      time.sleep(0.01)

  def on_column_click(self, **event_args):
    col = event_args['sender'].tag
    self.toggle_buttons(False)
    row = self.drop_piece(col, 1)
    if row is not None:
      self.board[row][col] = 0 
      self.animate_fall(col, row, 1)
      self.board[row][col] = 1
      self.draw_board()
      if anvil.server.call('check_winner_server', self.board, 1):
        self.play_sound("win.mp3")
        alert("Red Wins!")
        self.restart_click()
        return
      self.turn_label.text = "AI Thinking... 🟡"
      ai_col = anvil.server.call('get_ai_move', self.board)
      if ai_col is not None:
        ai_row = self.drop_piece(ai_col, 2)
        self.board[ai_row][ai_col] = 0
        self.animate_fall(ai_col, ai_row, 2)
        self.board[ai_row][ai_col] = 2
        self.draw_board()
        if anvil.server.call('check_winner_server', self.board, 2):
          self.play_sound("win.mp3")
          alert("Yellow Wins!")
          self.restart_click()
          return
      self.turn_label.text = "Your Turn 🔴"
    self.toggle_buttons(True)

  def drop_piece(self, col, piece):
    for r in range(5, -1, -1):
      if self.board[r][col] == 0:
        self.board[r][col] = piece
        return r
    return None

  def toggle_buttons(self, enabled):
    for b in self.buttons:
      b.enabled = enabled

  def restart_click(self, **event_args):
    self.board = [[0] * 7 for _ in range(6)]
    self.draw_board()
    self.turn_label.text = "Your Turn 🔴"
    self.toggle_buttons(True)

  def play_sound(self, sound_file):
    file_url = f"{anvil.server.get_app_origin()}/_/theme/{sound_file}"
    js_code = f"new Audio('{file_url}').play();"
    anvil.js.window.eval(js_code)