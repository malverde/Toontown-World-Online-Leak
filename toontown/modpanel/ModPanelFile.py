from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram


class ModPanelFile:
    def __init__(self, menu, filepath, needs_init):
        self.menu = menu
        self.filepath = filepath
        
        self.is_loading = False
        
        if needs_init:
            self.init_file()
            
        self.load_file()
        
    def init_file(self):
        with open(self.filepath, 'wb') as file:
    
            data = PyDatagram()
            data.add_uint8(0)
            
            file.write(PyDatagramIterator(data).get_remaining_bytes())
        
    def load_file(self):
        self.is_loading = True
    
        file = open(self.filepath, 'rb')
        data = file.read()
        file.close()
        
        dg = PyDatagram(data)
        data = PyDatagramIterator(dg)
        
        for _ in xrange(data.get_uint8()):
            self.load_button(data)
            
        self.is_loading = False
    
    def load_button(self, dgi):
        name = dgi.get_string()
        word_data = dgi.get_string()
        x = dgi.get_float64()
        y = dgi.get_float64()
        z = dgi.get_float64()
        
        button = self.menu.create_button(name, word_data, True)
        button.set_pos(x, y, z)

    def save_file(self):
        if self.is_loading:
            return
    
        with open(self.filepath, 'wb') as file:
            
            dg = PyDatagram()
            
            dg.add_uint8(len(self.menu.buttons))
            for button in self.menu.buttons:
                self.save_button(button.get_data(), dg)
                
            file.write(PyDatagramIterator(dg).getRemainingBytes())
    
    def save_button(self, data, dg):
        dg.add_string(data[0])
        dg.add_string(data[1])
        dg.add_float64(data[2][0])
        dg.add_float64(data[2][1])
        dg.add_float64(data[2][2])