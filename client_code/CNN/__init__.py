from ._anvil_designer import CNNTemplate
from anvil import *
import anvil.server
import anvil.js
import random
import time

class CNN(CNNTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # --- UI SETUP ---
    self.content_panel.clear() 
    self.content_panel.background = "#1a1a1a" 

    self.player_wins = 0
    self.ai_wins = 0

    self.main_container = ColumnPanel(width=580)
    self.content_panel.add_component(self.main_container)

    # --- IMAGE ASSET CHECK ---
    # Make sure the filename below matches your Assets folder EXACTLY
    try:
      self.hero = Image(source="_/theme/Connect 4 Image.jpg", height=220, display_mode='shrink_to_fit')
      self.main_container.add_component(self.hero)
    except:
      print("Image filename mismatch in Assets folder.")

    self.score_label = Label(text="Player: 0 | AI: 0", 
                             align='center', 
                             font_size=18, 
                             bold=True, 
                             foreground="#00d4ff")
    self.main_container.add_component(self.score_label)

    self.settings_panel = FlowPanel(align='center', spacing_above='small')
    self.main_container.add_component(self.settings_panel)

    self.settings_panel.add_component(Label(text="First Move:", foreground="#aaa"))
    self.first_move_dd = DropDown(items=[("Player", "Player"), ("AI", "AI"), ("Random", "Random")],
                                  selected_value="Random", 
                                  foreground="white")
    self.settings_panel.add_component(self.first_move_dd)

    self.canvas_1 = Canvas(width=580, height=650)
    self.main_container.add_component(self.canvas_1)
    self.canvas_1.set_event_handler('mouse_down', self.canvas_click)

    self.status_panel = FlowPanel(align='center')
    self.main_container.add_component(self.status_panel)

    self.turn_label = Label(text="Press Restart to Begin", foreground="white", font_size=20)
    self.status_panel.add_component(self.turn_label)

    self.reset_button = Button(text="RESTART GAME", role='raised', background='#ff4b2b', foreground='white')
    self.reset_button.set_event_handler('click', self.restart_click)
    self.status_panel.add_component(self.reset_button)

    self.board = [[0] * 7 for _ in range(6)]
    self.game_active = False 
    self.canvas_1.set_event_handler('show', lambda **e: self.draw_board())

  def update_score_display(self):
    self.score_label.text = f"Player: {self.player_wins} | AI: {self.ai_wins}"

  def draw_board(self):
    c = self.canvas_1
    c.clear_rect(0, 0, 580, 650)
    c.font = "30px Arial"
    c.fill_style = "#ff4b2b" 
    for col in range(7):
      x = col * (580//7) + (580//14) - 10 
      c.fill_text("⬇", x, 40)

    c.fill_style = "#0055ff" 
    c.fill_rect(0, 70, 580, 580)

    colors = {0: "#222", 1: "#ff4b2b", 2: "#ffee00"} 
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
      if anvil.server.call('check_winner_server', self.board, 1):
        self.player_wins += 1
        self.update_score_display()
        alert("Red Wins!")
        self.game_active = False
        return

      self.ai_turn() # Centralized AI logic call

  def ai_turn(self):
    """Standardized AI move logic"""
    self.turn_label.text = "AI Thinking... 🟡"
    ai_col = anvil.server.call_s('get_ai_move', self.board)
    if ai_col is not None:
      self.drop_piece(ai_col, 2)
      self.draw_board()
      if anvil.server.call('check_winner_server', self.board, 2):
        self.ai_wins += 1
        self.update_score_display()
        alert("AI Wins!") 
        self.game_active = False
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
    """Triggers the AI start immediately if required"""
    self.board = [[0] * 7 for _ in range(6)]
    self.draw_board()

    choice = self.first_move_dd.selected_value
    if choice == "Random":
      choice = random.choice(["Player", "AI"])
      Notification(f"Randomized Start: {choice} begins!").show()

    if choice == "AI":
      self.game_active = False 
      self.ai_turn()
    else:
      self.turn_label.text = "Your Turn 🔴"
      self.game_active = True