from ._anvil_designer import CNNTemplate
from anvil import *
import anvil.server
import anvil.js
import random

class CNN(CNNTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # 1. SETUP THEME AND CENTERING
    self.background = "#1a1a1a"
    self.clear() 

    # Shift everything down significantly to clear the top bar
    self.center_wrapper = FlowPanel(align='center', spacing_above='large')
    self.add_component(self.center_wrapper)

    self.main_container = ColumnPanel(width=600)
    self.main_container.spacing_above = 'large'
    self.center_wrapper.add_component(self.main_container)

    # 2. SCOREBOARD
    self.player_wins = 0
    self.ai_wins = 0
    self.score_label = Label(text="Player: 0 | AI: 0", align='center', font_size=20, bold=True, foreground="#00d4ff")
    self.main_container.add_component(self.score_label)

    # 3. SETTINGS - AUTO-START LOGIC
    self.settings_panel = FlowPanel(align='center')
    self.main_container.add_component(self.settings_panel)

    self.first_move_dd = DropDown(items=[("Select Who Starts...", None), ("Player First", "Player"), ("AI First", "AI"), ("Random", "Random")], 
                                  selected_value=None)
    self.first_move_dd.set_event_handler('change', self.start_game_from_dropdown)

    self.settings_panel.add_component(Label(text="First Move:", foreground="#aaa"))
    self.settings_panel.add_component(self.first_move_dd)

    # 4. THE GAME BOARD (CANVAS)
    self.canvas_1 = Canvas(width=580, height=650)
    self.main_container.add_component(self.canvas_1)
    self.canvas_1.set_event_handler('mouse_down', self.canvas_click)

    self.turn_label = Label(text="Select 'First Move' to Begin", foreground="white", align='center', font_size=18)
    self.main_container.add_component(self.turn_label)

    # 5. NAVIGATION BUTTONS
    self.btn_panel = FlowPanel(align='center')
    self.main_container.add_component(self.btn_panel)
    self.reset_btn = Button(text="RESTART", background='#ff4b2b', foreground='white', width=120)
    self.reset_btn.set_event_handler('click', self.restart_click)
    self.home_btn = Button(text="HOME", background='#555', foreground='white', width=120)
    self.home_btn.set_event_handler('click', lambda **e: open_form('Home'))
    self.btn_panel.add_component(self.reset_btn)
    self.btn_panel.add_component(self.home_btn)

    self.board = [[0] * 7 for _ in range(6)]
    self.last_move = None 
    self.game_active = False
    self.canvas_1.set_event_handler('show', lambda **e: self.draw_board())

  def start_game_from_dropdown(self, **event_args):
    if self.first_move_dd.selected_value is None: return
    self.restart_click()

  def play_sound(self):
    js_code = "new Audio('_/theme/win.mp3').play().catch(e => console.log('Audio blocked'));"
    anvil.js.window.eval(js_code)

  def draw_board(self):
    """Renders grid with Last Move highlight."""
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
    c.shadow_blur = 0 

  def canvas_click(self, x, y, **event_args):
    if not self.game_active: return
    col = int(x // (580/7))
    if col < 0 or col > 6 or self.board[0][col] != 0: return

    self.game_active = False 
    for r in range(5, -1, -1):
      if self.board[r][col] == 0:
        self.board[r][col] = 1
        self.last_move = (r, col) # Fixed: Correctly using 'col' for Player
        break
    self.draw_board()
    if anvil.server.call_s('check_winner_server', self.board, 1):
      self.player_wins += 1
      self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"
      self.play_sound()
      alert("Red Wins!")
      return
    self.ai_turn()

  def ai_turn(self):
    self.turn_label.text = "AI Thinking... 🟡"
    ai_col = anvil.server.call_s('get_ai_move', self.board)
    if ai_col is not None:
      for r in range(5, -1, -1):
        if self.board[r][ai_col] == 0:
          self.board[r][ai_col] = 2
          self.last_move = (r, ai_col) # Fixed: Used 'ai_col' instead of 'col'
          break
      self.draw_board()
      if anvil.server.call_s('check_winner_server', self.board, 2):
        self.ai_wins += 1
        self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"
        self.play_sound()
        alert("AI Wins!")
        return
    self.turn_label.text = "Your Turn 🔴"
    self.game_active = True

  def restart_click(self, **event_args):
    self.board = [[0] * 7 for _ in range(6)]
    self.last_move = None
    self.draw_board()
    choice = self.first_move_dd.selected_value
    if choice == "Random": choice = random.choice(["Player", "AI"])
    if choice == "AI": self.ai_turn()
    else:
      self.turn_label.text = "Your Turn 🔴"
      self.game_active = True