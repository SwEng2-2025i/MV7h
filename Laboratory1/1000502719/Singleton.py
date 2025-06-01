class Singleton:
    '''Esta clase simula el comportamiento de Singleton que se usara en Data.py'''
    _instance=None 
    def __new__(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    