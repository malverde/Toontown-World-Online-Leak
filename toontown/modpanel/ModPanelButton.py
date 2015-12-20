from toontown.modpanel import ModPanelGlobals

from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import DirectButton

import types


class ModPanelButton:
    def __init__(self, menu, name, command, register):
        self.menu = menu
        self.name = name
        
        self.command = command
        if type(command) == types.StringType:
            command = self.call_word

        self.button = DirectButton(frameSize=None, text=name, 
            image=(ModPanelGlobals.Button.find('**/QuitBtn_UP'),
            ModPanelGlobals.Button.find('**/QuitBtn_DN'),
            ModPanelGlobals.Button.find('**/QuitBtn_RLVR')),
            relief=None, command=command, text_pos=(0, -0.015),
            geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(0, 0, 0), 
            text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7
        )
        
        self.button.reparent_to(menu)
        
        if register:
            self.button.bind(DirectGuiGlobals.B2PRESS, self.delete_button)
            self.button.bind(DirectGuiGlobals.B3PRESS, self.button.editStart)
            self.button.bind(DirectGuiGlobals.B3RELEASE, self.edit_stop)
            self.menu.buttons.append(self)
            messenger.send('save-file')
        
    def call_word(self):
        messenger.send('magicWord', [self.command])
        
    def hide(self):
        self.button.hide()
        
    def show(self):
        self.button.show()
        
    def place(self):
        self.button.place()
        
    def set_pos(self, x, y, z):
        self.button.set_pos(x, y, z)
        
    def destroy(self):
        self.button.destroy()
        
    def edit_stop(self, dispatch):
        self.button.editStop(dispatch)
        
        messenger.send('save-file')

    def delete_button(self, dispatch):
        self.button.destroy()
        if self in self.menu.buttons:
            self.menu.buttons.remove(self)
            
        messenger.send('save-file')
        
    def get_data(self):
        return (self.name, self.command, self.button.get_pos())