from pymongo import MongoClient
from pprint import pprint
from typing import List, Dict, Any
import random


client = MongoClient('mongodb+srv://PyScr:Sorodich666@civbotdatabase-ltzn0.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client.CivBot



class User:
    def __init__(self, discordId: str, name: str, avatar_url: str) -> None:
        self.id = discordId
        self.name = name
        self.url = avatar_url
        self.coll = db.Users
        if self.coll.find_one({"id": self.id}) == None: #Если пользователя нет в базе данных - мы тупо создаём его
            self.ingame = False
            self.create()
        else:
            self.ingame = self.coll.find_one({"id": self.id})["in_game"]

    def __str__(self) -> str:
        return f"I'm {self.name}, My id is {self.id}, I'm in game: {self.ingame}" #Это мне надо для тестов!

    def create(self) -> None:
        user: Dict[str, Any] = {
            "id": str(self.id),
            "name": self.name,
            "matches": 0,
            "wins": 0,
            "loses": 0,
            "survives": 0,
            "avatar_URL": self.url,
            "points": 0,
            "in_game": False,
        } #Шаблон пользователя в базе данных.


        self.coll.insert_one(user)

    def join(self) -> bool:
        if self.ingame:
            return False #Блокируем вход в матч, если пользователь уже в игре
        else:
            self.coll.update_one({"id": self.id}, {"$set": {"in_game": True}})
            return True #Пускаем его в матч, если он не в игре

    def statistic(self) -> Dict[str, Any]:
        mediator = self.coll.find_one({"id": self.id})
        stat: Dict[str, Any] = {
            "id": mediator["id"],
            "name": mediator["name"],
            "matches": mediator["matches"],
            "wins": mediator["wins"],
            "loses": mediator["loses"],
            "survives": mediator["survives"],
            "avatar": mediator["avatar_URL"],
            "points": mediator["points"],
            "in_game": mediator["in_game"],
        }
        return stat #Статистика игрока. В виде словаря, да
    
    


class Match:
    def __init__(self, match_id: int) -> None:
        self.coll = db.Matches
        self.players: List[str] = []
        self.id: int = match_id

    def not_exist_check(self, match_id: int) -> bool: #Проверка на уже созданный матч
        if self.coll.find_one({"id": match_id}) == None:
            return True
        else:
            return False

    def create(self, match_id: int) -> bool:
        self.match_id: int = match_id
        match: Dict[str, Any] = {
            "id": match_id,
            "players": [],
            "host": "",
            "avg_rating": 0,
            "status": False,
            "winer": "",
            "looser": [],
            "survival": [],
        }

        if self.not_exist_check(match_id):
            self.coll.insert_one(match)
            return True #Если не существует матча, мы его создаём!
        else:
            return False #Матч уже существует

    def join(self, player: User, match_id: int) -> bool:
        if player.ingame:
            return False #Если игрок уже в игре - он идёт нахуй!
        else: #Иначе проверяем матч на то, существует он или нет!
            if self.not_exist_check(match_id):
                self.create(match_id) #Если не существует - создаём и добавляем игрока в список играющих!
                self.players.append(player.id)
                return True
            else: #Если существует, мы проверяем его статус.
                if self.coll.find_one({"id": match_id})["status"] == False:
                    self.players.append(player.id) #Если регистрация открыта - пускаем игрока
                    return True
                else: #А иначе он идёт нахуй!
                    return False

    def start(self, match_id: int) -> List[str]:
        host: List[str] = []
        self.coll.update({"id": match_id}, {"$addToSet": {"players": {"$each": self.players}}})
        self.coll.update({"id": match_id}, {"$set": {"status": True}})
        if "371291041640218647" in self.players:
            host.append("371291041640218647")
        else:
            host.append(random.choice(self.players))
        self.coll.update({"id": match_id}, {"$addToSet": {"hosts": {"$each": hosts}}})
        return host

    def remake(self, player: User, match_id: int) -> bool:
        if player.id == self.coll.find_one({"id": match_id})["host"]:
            for user in self.coll.find_one({"id": match_id}):
                db.Users.update({"id": user}, {"$set": {"in_game": False}})
            self.coll.delete_one({"id": match_id})
            return True
        else:
            return False

    def result(self, player: User, match_id: int, *args) -> bool:
        if player.id == self.coll.find_one({"id": match_id})["host"]:
            for arg in enumerate(args):
                usr = db.Users.find_one({"name": arg[1]})["id"]
                if arg[0] == 0:
                    self.coll.update({"id": match_id}, {"$pull": {"players": usr}})
                    self.coll.update({"id": match_id}, {"$set": {"winer": usr}})
                    db.Users.update({"id": usr}, {"$inc": {{"wins": 1}, {"matches": 1}, {"points": self.coll.find_one({"id": match_id})["avg_rating"]*0.25}}})
                else:
                    db.Users.update({"id": usr}, {"$inc": {{"loses": 1}, {"matches": 1}, {"points": -self.coll.find_one({"id": match_id})["avg_rating"]*0.1}}})
                    self.coll.update({"id": match_id}, {"$pull": {"players": usr}})
                    self.coll.update({"id": match_id}, {"$addToSet": {"looser": usr}})
            for user in self.coll.find_one({"id": match_id})["players"]:
                self.coll.update({"id": match_id}, {"$pull": {"players": user}})
                self.coll.update({"id": match_id}, {"$addToSet": {"survival": user}})
                db.Users.update({"id": usr}, {"$inc": {{"survives": 1}, {"matches": 1}, {"points": self.coll.find_one({"id": match_id})["avg_rating"]*0.15}}})
            return True
        else:
            return False





def join(player: User, match: Match, match_id: str) -> str:
    ans_from_player: bool = player.join()
    ans_from_match: bool = match.join(player, int(match.id))
    if ans_from_player == False:
        return "В игре!"
    else:
        if ans_from_match == False:
            return "Матч уже идёт!"
        else:
            return "Добро пожаловать!"

def remake(player: User, match: Match, match_id: str) -> bool:
    if match.remake(player, int(match_id)):
        match.remake(player, int(match_id))
        return True
    else:
        return False


print(user.statistic())
#TODO: results from match, write mediator of two functions
