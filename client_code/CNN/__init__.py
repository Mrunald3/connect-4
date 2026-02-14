from ._anvil_designer import CNNTemplate
from anvil import *
import anvil.server
import anvil.js
import random

class CNN(CNNTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # 1. THEME & FULL SCREEN SETUP
    self.background = "#1a1a1a"
    self.clear() 

    # Preload audio into memory to remove the delay
    self.win_sound = anvil.js.window.Audio('_/theme/win.mp3')

    # 2. SHIFT DOWN & CENTERING
    self.center_wrapper = FlowPanel(align='center', spacing_above='large')
    self.add_component(self.center_wrapper)

    self.main_container = ColumnPanel(width=600)
    self.main_container.spacing_above = 'large'
    self.center_wrapper.add_component(self.main_container)

    # 3. SCOREBOARD
    self.player_wins = 0
    self.ai_wins = 0
    self.score_label = Label(text="Player: 0 | AI: 0", align='center', font_size=20, bold=True, foreground="#00d4ff")
    self.main_container.add_component(self.score_label)

    # 4. SETTINGS - MODEL SELECTION & AUTO-START
    self.settings_panel = FlowPanel(align='center')
    self.main_container.add_component(self.settings_panel)

    self.model_dd = DropDown(items=[("Select Model...", None), ("CNN", "cnn"), ("Transformer", "transformer")], 
                             selected_value=None)
    self.model_dd.set_event_handler('change', self.check_start_conditions)

    self.first_move_dd = DropDown(items=[("Select Who Starts...", None), ("Player First", "Player"), ("AI First", "AI"), ("Random", "Random")], 
                                  selected_value=None)
    self.first_move_dd.set_event_handler('change', self.check_start_conditions)

    self.settings_panel.add_component(Label(text="Model:", foreground="#aaa"))
    self.settings_panel.add_component(self.model_dd)
    self.settings_panel.add_component(Label(text="First Move:", foreground="#aaa"))
    self.settings_panel.add_component(self.first_move_dd)

    # 5. THE GAME BOARD (CANVAS)
    self.canvas_1 = Canvas(width=580, height=650)
    self.main_container.add_component(self.canvas_1)
    self.canvas_1.set_event_handler('mouse_down', self.canvas_click)

    self.turn_label = Label(text="Configure settings to begin", foreground="white", align='center', font_size=18)
    self.main_container.add_component(self.turn_label)

    # 6. NAVIGATION
    self.btn_panel = FlowPanel(align='center')
    self.main_container.add_component(self.btn_panel)
    self.reset_btn = Button(text="RESTART", background='#ff4b2b', foreground='white', width=120)
    self.reset_btn.set_event_handler('click', self.restart_click)
    self.home_btn = Button(text="HOME", background='#555', foreground='white', width=120)
    self.home_btn.set_event_handler('click', lambda **e: open_form('Home'))
    self.btn_panel.add_component(self.reset_btn)
    self.btn_panel.add_component(self.home_btn)

    # 7. GAME STATE VARIABLES
    self.board = [[0] * 7 for _ in range(6)]
    self.last_move = None 
    self.game_active = False
    self.game_over_message = None # Tracks the centered text
    self.canvas_1.set_event_handler('show', lambda **e: self.draw_board())

  def check_start_conditions(self, **event_args):
    if self.model_dd.selected_value and self.first_move_dd.selected_value:
      self.restart_click()

  def play_sound(self):
    try:
      self.win_sound.currentTime = 0 
      self.win_sound.play()
    except:
      pass

  def show_winner(self, message, color):
    """Prepares message and draws it centered on board."""
    # Translation logic: RED -> PLAYER
    if "RED" in message.upper() or "PLAYER" in message.upper():
      message = "PLAYER WINS!"
    elif "AI" in message.upper():
      message = "AI WINS!"

    self.game_over_message = (message, color)
    self.game_active = False
    self.play_sound()
    self.draw_board()

  def draw_board(self):
    """Renders grid and centered text overlay."""
    c = self.canvas_1
    c.clear_rect(0, 0, 580, 650)
    c.font = "30px Arial"
    c.fill_style = "#ff4b2b" 
    for col_idx in range(7):
      c.fill_text("⬇", col_idx * (580//7) + 30, 40)

    c.fill_style = "#0055ff" 
    c.fill_rect(0, 70, 580, 580)

    colors = {0: "#222", 1: "#ff4b2b", 2: "#ffee00"} 
    for r in range(6):
      for col in range(7):
        if self.last_move == (r, col):
          c.shadow_blur = 15
          c.shadow_color = "white"
        else:
          c.shadow_blur = 0

        c.fill_style = colors[self.board[r][col]]
        c.begin_path()
        c.arc(col * (580//7) + 41, r * (580//6) + 118, 35, 0, 2 * 3.14159)
        c.fill()

        # Draw centered winner text over the board
    if self.game_over_message:
      msg, color = self.game_over_message
      c.shadow_blur = 20
      c.shadow_color = "black"
      c.font = "bold 55px Arial"
      c.fill_style = color
      c.text_align = "center"
      c.fill_text(msg, 290, 360) # Perfectly centered in the board area

    c.shadow_blur = 0 

  def canvas_click(self, x, y, **event_args):
    if not self.game_active: return
    col = int(x // (580/7))
    if col < 0 or col > 6 or self.board[0][col] != 0: 
      if 0 <= col <= 6 and self.board[0][col] != 0:
        Notification("Column Full!", style="warning").show()
      return

    self.game_active = False 
    for r in range(5, -1, -1):
      if self.board[r][col] == 0:
        self.board[r][col] = 1
        self.last_move = (r, col)
        break
    self.draw_board()

    if anvil.server.call_s('check_winner_server', self.board, 1):
      self.player_wins += 1
      self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"
      self.show_winner("PLAYER WINS!", "#ff4b2b")
      return

    if all(self.board[0][c] != 0 for c in range(7)):
      self.show_winner("IT'S A TIE!", "white")
      return

    self.ai_turn()

  def ai_turn(self):
    model = self.model_dd.selected_value
    self.turn_label.text = f"AI Thinking ({model.upper()})... 🟡"

    ai_col = anvil.server.call_s('get_ai_move', self.board, model_type=model)

    if ai_col is not None:
      for r in range(5, -1, -1):
        if self.board[r][ai_col] == 0:
          self.board[r][ai_col] = 2
          self.last_move = (r, ai_col) 
          break
      self.draw_board()
      if anvil.server.call_s('check_winner_server', self.board, 2):
        self.ai_wins += 1
        self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"
        self.show_winner("AI WINS!", "#ffee00")
        return

    if all(self.board[0][c] != 0 for c in range(7)):
      self.show_winner("IT'S A TIE!", "white")
      return

    self.turn_label.text = "Your Turn 🔴"
    self.game_active = True

  def restart_click(self, **event_args):
    self.board = [[0] * 7 for _ in range(6)]
    self.last_move = None
    self.game_over_message = None
    self.draw_board()
    choice = self.first_move_dd.selected_value
    if choice == "Random": choice = random.choice(["Player", "AI"])
    if choice == "AI": self.ai_turn()
    else:
      self.turn_label.text = "Your Turn 🔴"
      self.game_active = True