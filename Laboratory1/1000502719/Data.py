from User import User
from typing import List
from Singleton import Singleton

class Data(Singleton):
    '''Data hereda el comportamiento de Singleton'''
    '''Usamos Data como una forma de "Base de datos, solo permitimos crear
        una instancia de Data'''
    users: List[User]

    def __init__(self):
        if not hasattr(self,"users"):
            self.users=[]