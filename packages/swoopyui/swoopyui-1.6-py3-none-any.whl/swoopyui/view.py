import os
import urllib.parse



class View (object):
    def __init__(self, app) -> None:
        self.__app = app
        self.__next_id = 0 #? The next viewID.

        # View props
        self.sub_views_history = [] # This will store all sub_views even from the another subviews.
        self.sub_views = []
    
    def update (self, sub_view=None):
        if sub_view != None:
            action_content = {
                "new_view_content" : sub_view.get_dict_content()
            }
            self.__app.set_for_the_next_update_get (action_name="update_view", action_content=action_content)

    def add (self, view):
        view.respown (new_id=self.get_new_view_id(), mother_view=self, parent=self)
        action_content = {
            "new_view_content" : view.get_dict_content()
        }
        self.__app.set_for_the_next_update_get (action_name="add_view", action_content=action_content)
        self.sub_views_history.append(view)
        self.sub_views.append(view)
    
    def clear (self):
        for sbv in self.sub_views:
            action_content = {
                "view_id" : sbv.id
            }
            self.__app.set_for_the_next_update_get (action_name="delete_view", action_content=action_content)
    
    def delete (self, view):
        """Delete a sub-view from the view"""
        action_content = {
            "view_id" : view.id
        }
        self.__app.set_for_the_next_update_get (action_name="delete_view", action_content=action_content)
        
        num = 0
        for v in self.sub_views_history:
            if v.id == view.id:
                del self.sub_views_history[num]
                break
            num = num + 1
    
    def asset_path (self, path:str):
        """
        Use this to load a local file such as images, text files etc..

        But make sure that the `app` class is taking the `base_name` as the main file `__name__`,
        such as:

        ```python
        app (base_name=__name__)
        ```
        """
        if not os.path.isfile (path):
            raise FileNotFoundError ("The 'asset_path' must take a valid path.")
        
        original_string = path
        encoded_string = urllib.parse.quote(original_string)
        url_of_asset = f"http://127.0.0.1:{self.__app.app_port}/get_assets?path={encoded_string}"
        return url_of_asset


    def get_new_view_id (self):
        """This will generate new viewID for the current and next view"""
        self.__next_id = self.__next_id + 1
        current = self.__next_id
        self.__next_id = self.__next_id + 1
        return current
    
    def manage_on_view_action (self, action_content:dict):
        view_id = action_content['view_id']
        for v in self.sub_views_history:
            if v.id == view_id:
                v.view_action(action_content)
                break