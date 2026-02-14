from ._anvil_designer import HomeTemplate
from anvil import *

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # 1. Background to cover the whole window
    self.background = "#1a1a1a"
    self.clear() 

    # 2. Create a wrapper to keep the content in the middle
    self.center_wrapper = FlowPanel(align='center')
    self.add_component(self.center_wrapper)

    # 3. Standardized 600px container for consistency with the CNN page
    self.main_container = ColumnPanel(width=1000)
    self.center_wrapper.add_component(self.main_container)

    # 4. IMAGE (From Assets)
    self.logo = Image(source="_/theme/Connect 4 Image.png", height=550, display_mode='shrink_to_fit')
    self.main_container.add_component(self.logo)

    # 5. TITLE
    self.title = Label(text="CONNECT 4", align='center', font_size=32, bold=True, foreground="#00d4ff")
    self.main_container.add_component(self.title)

    # 6. ACTION BUTTONS
    # Main Play Button
    self.play_btn = Button(text="PLAY NOW", background='#ff4b2b', foreground='white', font_size=24, bold=True)
    self.play_btn.set_event_handler('click', lambda **e: open_form('CNN'))
    self.main_container.add_component(self.play_btn)

    # How to Play Button
    self.help_btn = Button(text="HOW TO PLAY", role='secondary-color', foreground="white", spacing_above='small')
    self.help_btn.set_event_handler('click', self.how_to_play_click)
    self.main_container.add_component(self.help_btn)

    # 7. FOOTER ROW: About Us & Exit
    self.footer_row = FlowPanel(align='center', spacing_above='medium')
    self.main_container.add_component(self.footer_row)

    self.about_btn = Button(text="ABOUT US", role='link', foreground="#aaa")
    self.about_btn.set_event_handler('click', lambda **e: alert("Connect 4 AI Project v1.0", title="About Us"))
    self.footer_row.add_component(self.about_btn)

    self.exit_btn = Button(text="EXIT GAME", foreground='#ff4b2b', role='link')
    self.exit_btn.set_event_handler('click', self.exit_click)
    self.footer_row.add_component(self.exit_btn)

  def how_to_play_click(self, **event_args):
    """Displays game instructions."""
    alert("1. Click ⬇ to drop a Red piece.\n2. AI responds with Yellow.\n3. Get 4 in a row to win!", title="How to Play")

  def exit_click(self, **event_args):
    """Confirms and exits the game view."""
    if confirm("Are you sure you want to exit?"):
      self.main_container.clear()
      self.add_component(Label(text="Thanks for playing!", foreground="white", align="center", font_size=20))