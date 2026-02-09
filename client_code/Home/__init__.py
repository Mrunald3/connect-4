from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # FIX: Set background directly on the form
    self.background = "white" 

    # 1. Main container for centering
    self.main_container = ColumnPanel(width=600)
    self.add_component(self.main_container) # Added directly to 'self'

    # 2. Game Logo
    # Make sure 'Connect 4.jpg' exists in your Assets
    self.logo = Image(source="_/theme/Connect 4.jpg", height=250)
    self.main_container.add_component(self.logo)

    # 3. Game Title
    self.title = Label(text="CONNECT 4", 
                       align='center', 
                       font_size=40, 
                       bold=True, 
                       foreground="blue")
    self.main_container.add_component(self.title)

    # 4. Play Now Button
    self.play_button = Button(text="PLAY NOW", 
                              role='raised', 
                              background='red', 
                              foreground='white', 
                              font_size=24, 
                              bold=True)
    self.play_button.set_event_handler('click', self.play_now_click)
    self.main_container.add_component(self.play_button)

  def play_now_click(self, **event_args):
    # Switches to your game form
    open_form('CNN')