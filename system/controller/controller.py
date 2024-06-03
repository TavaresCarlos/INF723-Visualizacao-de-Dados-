#Management of the model and view classes

class user_controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def set_user_name(self, name):
        self.model.name = name
    
