from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.background = "white" #

    # 1. Main container (Fixed 600px width for centering)
    self.main_container = ColumnPanel(width=600)
    self.add_component(self.main_container)

    # 2. Logo
    # Use 'shrink_to_fit' to maintain the 1:1 aspect ratio of your image
    self.logo = Image(source="_/theme/Connect 4 Image.png", 
                      height=400, 
                      display_mode='shrink_to_fit')
    self.main_container.add_component(self.logo)

    # 3. Title
    self.title = Label(text="CONNECT 4 OPTIMIZED", align='center', font_size=32, bold=True, foreground="blue")
    self.main_container.add_component(self.title)

    # 4. PLAY NOW Button (FIXED: Removed margin_top)
    self.play_button = Button(text="PLAY NOW", role='raised', background='red', foreground='white', 
                              font_size=24, bold=True)
    self.play_button.set_event_handler('click', self.play_now_click)
    self.main_container.add_component(self.play_button)

    # 5. HOW TO PLAY Button
    self.help_button = Button(text="HOW TO PLAY", role='secondary-color')
    self.help_button.set_event_handler('click', self.how_to_play_click)
    self.main_container.add_component(self.help_button)

    # 6. Bottom Row for About Us & Exit
    self.bottom_row = FlowPanel(align='center')
    self.main_container.add_component(self.bottom_row)

    self.about_button = Button(text="ABOUT US", role='link')
    self.about_button.set_event_handler('click', self.about_us_click)
    self.bottom_row.add_component(self.about_button)

    self.exit_button = Button(text="EXIT", role='link', foreground='red')
    self.exit_button.set_event_handler('click', self.exit_click)
    self.bottom_row.add_component(self.exit_button)

  # --- Event Handlers ---
  def play_now_click(self, **event_args):
    open_form('CNN')

  def how_to_play_click(self, **event_args):
    alert("1. Select a column (1-7) to drop your red piece.\n"
          "2. AI responds with a yellow piece.\n"
          "3. Get 4 in a row to win!", title="How to Play")

  def about_us_click(self, **event_args):
    alert("Connect 4 Optimized\nAI Optimization Project v1.0", title="About Us")

  def exit_click(self, **event_args):
    if confirm("Are you sure you want to exit?"):
      self.main_container.clear()
      self.add_component(Label(text="Thanks for playing!", align='center', font_size=20))