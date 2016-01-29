from pandac.PandaModules import NodePath

from toontown.modpanel.ModPanelFile import ModPanelFile
from toontown.modpanel.ModPanelButton import ModPanelButton

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *

import os


class ModPanel(NodePath, DirectObject):
    def __init__(self):
        NodePath.__init__(self, aspect2d.attach_new_node('ModMenu'))
        DirectObject.__init__(self)
        
        self.panel_file = None
        self.buttons = []
        
        self.hide()
        
        self.current_fill_name = None
        self.current_fill_exec = None
        self.current_accept_button = None
        
        button = self.create_button('Create A Button', self.load_create_button_dialog)
        button.set_pos(-0.72, 0, 0.95)
        
        self.accept('f10', self.toggle_menu)
        self.accept('f11', self.load_file_dialog)
        self.accept('save-file', self.save_file)
        
    def toggle_menu(self):
        if self.visible:
            self.hide()
        else:
            self.show()
            
            if self.panel_file is None:
                self.load_file_dialog()
        
    def hide(self):
        self.visible = False
        
        NodePath.hide(self)
        
    def show(self):
        self.visible = True
        
        NodePath.show(self)
        
    def load_file_dialog(self):
        # Unload the previous buttons
        for button in self.buttons:
            button.destroy()
        self.buttons = []

        # Load in the new panel_save.mp
        self.load_file('panel_save.mp')
    
    def load_file(self, filepath):
        needs_init = not os.path.exists(filepath)
        self.panel_file = ModPanelFile(self, filepath, needs_init)
        
    def load_create_button_dialog(self):
        self.current_fill_name = DirectEntry(initialText='Button Name', 
            numLines=1, focus=1
        )
        self.current_fill_name.reparent_to(self)
        self.current_fill_name.set_pos(-0.34, 0, 0.78)
        self.current_fill_name.set_scale(0.07)
        
        self.current_fill_exec = DirectEntry(initialText='Magic Word',
            numLines=20, focus=0, width=30
        )
        self.current_fill_exec.reparent_to(self)
        self.current_fill_exec.set_pos(-1.05, 0, 0.57)
        self.current_fill_exec.set_scale(0.07)
    
        self.current_accept_button = self.create_button('Accept', self.create_button_complete)
        self.current_accept_button.set_pos(0, 0, -0.9)
        
    def create_button_complete(self):
        name = self.current_fill_name.get(plain=True)
        command = self.current_fill_exec.get(plain=True)
        
        self.current_fill_name.destroy()
        self.current_fill_name = None
        
        self.current_fill_exec.destroy()
        self.current_fill_exec = None
    
        self.current_accept_button.destroy()
        self.current_accept_button = None
        
        self.create_button(name, command, True)
        
    def create_button(self, name, command, register=False):
        return ModPanelButton(self, name, command, register)
        
    def save_file(self):
        if self.panel_file:
            self.panel_file.save_file()