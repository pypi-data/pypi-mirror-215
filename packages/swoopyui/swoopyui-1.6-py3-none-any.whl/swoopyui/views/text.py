from ..tools.on_action import on_view_action


class Text (object):
    def __init__(self, text, foreground_color="primary", on_hover=None, bold:bool=False, size:float=18) -> None:
        self.__last_view_id = None # This is used becuase swiftUI will not know that this updated without it
        self.__id = None
        self.__mother_view = None
        self.__parent_view = None

        self.__text : str = text
        self.__foreground_color : str = foreground_color
        self.on_hover = on_hover
        self.__bold : bool = bold
        self.__size : str = size
    

    def get_dict_content (self):
        return {
            "last_view_id" : self.__last_view_id,
            "view_id" : self.__id,
            "vname" : "Text",
            "text" : self.__text,
            "fgcolor" : self.__foreground_color,
            "bold" : self.__bold,
            "size" : self.__size
        }

    def respown (self, new_id=None, mother_view=None, parent=None):
        if new_id == None: return
        if mother_view == None: return
        if parent == None: return

        if self.__id == None:
            self.__id = new_id
            self.__last_view_id = new_id
        
        if self.__mother_view == None:
            self.__mother_view = mother_view
        
        if self.__parent_view == None:
            self.__parent_view = parent
    
    def view_action (self, action_data):
        action_name = action_data['action_name']
        if action_name == "on_hover":
            hover_state = action_data['hover_state']
            on_view_action(self.on_hover, [self, {"state":hover_state}])
    
    @property
    def id (self):
        return self.__id

    @property
    def text (self): return self.__text

    @text.setter
    def text (self, value):
        if self.__mother_view == None:
            raise Exception("Cannot change the sub_view property while its not on the screen.")
        
        self.__text = value
        self.__id = self.__mother_view.get_new_view_id()
        self.__mother_view.update(self)
        self.__last_view_id = self.__id
    
    @property
    def foreground_color (self): return self.__foreground_color

    @foreground_color.setter
    def foreground_color (self, value):
        if self.__mother_view == None:
            raise Exception("Cannot change the sub_view property while its not on the screen.")
        
        self.__foreground_color = value
        self.__id = self.__mother_view.get_new_view_id()
        self.__mother_view.update(self)
        self.__last_view_id = self.__id
    

    @property
    def bold (self):
        return self.__bold
    
    @bold.setter
    def bold (self, value:bool):
        if self.__mother_view == None:
            raise Exception("Cannot change the sub_view property while its not on the screen.")
        
        self.__bold = value
        self.__id = self.__mother_view.get_new_view_id()
        self.__mother_view.update(self)
        self.__last_view_id = self.__id
    
    @property
    def size (self):
        return self.__size
    
    @size.setter
    def size (self, value:float):
        if self.__mother_view == None:
            raise Exception("Cannot change the sub_view property while its not on the screen.")
        
        self.__size = value
        self.__id = self.__mother_view.get_new_view_id()
        self.__mother_view.update(self)
        self.__last_view_id = self.__id