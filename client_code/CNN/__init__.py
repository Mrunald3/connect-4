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
    self.content_panel.background = "white"

    # Initialize Win Counters
    self.player_wins = 0
    self.ai_wins = 0

    # 1. ROOT CONTAINER: Centered 580px wide stack
    self.main_container = ColumnPanel(width=580)
    self.content_panel.add_component(self.main_container)

    # 2. THE BOARD CANVAS
    self.canvas_1 = Canvas(width=580, height=650)
    self.main_container.add_component(self.canvas_1)
    self.canvas_1.set_event_handler('mouse_down', self.canvas_click)

    # 3. SCOREBOARD
    self.score_panel = FlowPanel(align='center', spacing_above='small')
    self.main_container.add_component(self.score_panel)

    self.score_label = Label(text="Player: 0 | AI: 0", 
                             font_size=18, 
                             bold=True, 
                             foreground="blue")
    self.score_panel.add_component(self.score_label)

    # 4. STATUS & RESTART
    self.status_panel = FlowPanel(align='center')
    self.main_container.add_component(self.status_panel)

    self.turn_label = Label(text="Your Turn 🔴", foreground="black", font_size=20)
    self.status_panel.add_component(self.turn_label)

    self.reset_button = Button(text="Restart Game", role='secondary-color')
    self.reset_button.set_event_handler('click', self.restart_click)
    self.status_panel.add_component(self.reset_button)

    # --- STATE ---
    self.board = [[0] * 7 for _ in range(6)]
    self.game_active = True
    self.canvas_1.set_event_handler('show', lambda **e: self.draw_board())

  def update_score_display(self):
    """Refreshes the win counter label"""
    self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"

  def play_sound(self, sound_file):
    """Plays audio from Theme Assets"""
    file_url = f"{anvil.server.get_app_origin()}/_/theme/{sound_file}"
    js_code = f"new Audio('{file_url}').play();"
    anvil.js.window.eval(js_code)

  def draw_board(self):
    """Renders the game board and arrows"""
    c = self.canvas_1
    c.clear_rect(0, 0, 580, 650)
    c.font = "30px Arial"
    c.fill_style = "red"
    for col in range(7):
      x = col * (580//7) + (580//14) - 10 
      c.fill_text("⬇", x, 40)

    c.fill_style = "#0000FF"
    c.fill_rect(0, 70, 580, 580)

    colors = {0: "white", 1: "red", 2: "yellow"} 
    for r in range(6):
      for col in range(7):
        x = col * (580//7) + (580//14)
        y = r * (580//6) + (580//12) + 70
        c.fill_style = colors[self.board[r][col]]
        c.begin_path()
        c.arc(x, y, 35, 0, 2 * 3.14159)
        c.fill()

  def canvas_click(self, x, y, **event_args):
    if not self.game_active: return

    col = int(x // (580/7))
    if col < 0 or col > 6: return

    self.game_active = False 
    row = self.drop_piece(col, 1)

    if row is not None:
      self.draw_board()

      # Check for Player Win
      if anvil.server.call('check_winner_server', self.board, 1):
        self.play_sound("win.mp3")
        self.player_wins += 1
        self.update_score_display()
        alert("Red Wins!")
        self.restart_click()
        return

        # AI Move Phase
      self.turn_label.text = "AI Thinking... 🟡"

      # Using silent call to avoid default loading indicator
      ai_col = anvil.server.call_s('get_ai_move', self.board)

      if ai_col is not None:
        self.drop_piece(ai_col, 2)
        self.draw_board()

        # Check for AI Win
        if anvil.server.call('check_winner_server', self.board, 2):
          self.play_sound("win.mp3")
          self.ai_wins += 1
          self.update_score_display()
          alert("AI Wins!") 
          self.restart_click()
          return

      self.turn_label.text = "Your Turn 🔴"
      self.game_active = True

  def drop_piece(self, col, piece):
    for r in range(5, -1, -1):
      if self.board[r][col] == 0:
        self.board[r][col] = piece
        return r
    return None

  def restart_click(self, **event_args):
    """Clears board but keeps win history"""
    self.board = [[0] * 7 for _ in range(6)]
    self.game_active = True
    self.draw_board()
    self.turn_label.text = "Your Turn 🔴"