from Data import Data
from User import User

class ManejadorDB:
    dataBase:Data
    def __init__(self):
        self.dataBase=Data()

    def getAllUsers(self):
        return self.dataBase.users

    def getUserById(self,id):
        returnUser=None
        for user in self.dataBase.users:
            if(user.id==id):
                returnUser=user
        return returnUser
        
    def registerUser(self,jsonfile):
        newUser=User(
            name=jsonfile["name"],
            preferred_channel=jsonfile["preferred_channel"],
            available_channels=jsonfile["available_channels"],
            notifAttempts=[]
            )
        self.dataBase.users.append(newUser)
    
    def updateUser(self,id,attempt):
        user=self.getUserById(id)
        attempts=user.notifAttempts
        attempts.append(attempt)
        user.notifAttempts=attempts
        self.dataBase.users.remove(user)
        self.dataBase.users.append(user)
        

