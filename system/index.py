from controller.controller import *
from model.model import *
from view.view import *

if __name__ == "__main__":
    user_m = user_model("Carlos Henrique")
    user_v = user_view()
    user_c = user_controller(user_m, user_v)

    user_c.set_user_name("Carlos")
