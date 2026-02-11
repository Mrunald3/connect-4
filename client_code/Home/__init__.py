from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # 1. MATCH DARK THEME: Change white to the dark background
    self.background = "#1a1a1a" 

    # 2. Main container (Fixed 600px width for centering)
    self.main_container = ColumnPanel(width=600)
    self.add_component(self.main_container)

    # 3. FIX FILENAME: Use .jpg to match your actual file
    # Changed from .png to .jpg based on your successful upload
    self.logo = Image(source="_/theme/Connect 4 Image.jpg", 
                      height=400, 
                      display_mode='shrink_to_fit')
    self.main_container.add_component(self.logo)

    # 4. TITLE: Neon blue for better contrast on dark
    self.title = Label(text="CONNECT 4 OPTIMIZED", 
                       align='center', 
                       font_size=32, 
                       bold=True, 
                       foreground="#00d4ff")
    self.main_container.add_component(self.title)

    # 5. BUTTONS: Updated colors for high visibility
    self.play_button = Button(text="PLAY NOW", role='raised', 
                              background='#ff4b2b', foreground='white', 
                              font_size=24, bold=True)
    self.play_button.set_event_handler('click', self.play_now_click)
    self.main_container.add_component(self.play_button)

    self.help_button = Button(text="HOW TO PLAY", role='secondary-color', foreground="white")
    self.help_button.set_event_handler('click', self.how_to_play_click)
    self.main_container.add_component(self.help_button)

    # 6. Bottom Row
    self.bottom_row = FlowPanel(align='center')
    self.main_container.add_component(self.bottom_row)

    self.about_button = Button(text="ABOUT US", role='link', foreground="#aaa")
    self.about_button.set_event_handler('click', self.about_us_click)
    self.bottom_row.add_component(self.about_button)

    self.exit_button = Button(text="EXIT", role='link', foreground='#ff4b2b')
    self.exit_button.set_event_handler('click', self.exit_click)
    self.bottom_row.add_component(self.exit_button)

    # --- Event Handlers (Preserved) ---
  def play_now_click(self, **event_args):
    open_form('CNN')

  def how_to_play_click(self, **event_args):
    alert("1. Select a column (⬇) to drop your red piece.\n"
          "2. AI responds with a yellow piece.\n"
          "3. Get 4 in a row to win!", title="How to Play")

  def about_us_click(self, **event_args):
    alert("Connect 4 Optimized\nAI Optimization Project v1.0", title="About Us")

  def exit_click(self, **event_args):
    if confirm("Are you sure you want to exit?"):
      self.main_container.clear()
      self.add_component(Label(text="Thanks for playing!", align='center', font_size=20, foreground="white"))