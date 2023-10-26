from src.controllers.pix.pix_controller import PixController
from src.views.pix.pix_view import PixView


def pix_composer():
    controller = PixController()
    view = PixView(controller)
    return view
