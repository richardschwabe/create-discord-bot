# You can skip the generation of Model/Controller/Converter and Tests by supplying --bare to createcog

from .model import *

class AdminController:
    def __init__(self):
        pass

    def foo(self):
        return "Bar"