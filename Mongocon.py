from pymongo import MongoClient
from typing import List, Dict, Any
import random


client = MongoClient('mongodb://DataUser:Sorodich666@ds211099.mlab.com:11099/heroku_w4jzwn4c')
db = client.CivBot



class User:
    def __init__(self, discordId: int, name: str, avatar_url: str) -> None:
        self.id = discordId
        self.name = name
        self.url = avatar_url
        self.coll = db.Users
        if self.coll.find_one({"id": self.id}) == None: #Если пользователя нет в базе данных - мы тупо создаём его
            self.ingame = False
            self.create()
        else:
            self.ingame = self.coll.find_one({"id": self.id})["in_game"]

    def create(self) -> None:
        user: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "matches": 0,
            "wins": 0,
            "loses": 0,
            "survives": 0,
            "avatar_URL": self.url,
            "points": 1200,
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
        } #Шаблон Матча в базе данных

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
                self.coll.update_one({"id": match_id}, {"$addToSet": {"players": player.id}})
                return True
            else: #Если существует, мы проверяем его статус.
                if self.coll.find_one({"id": match_id})["status"] == False: #Если регистрация открыта - пускаем игрока
                    self.coll.update_one({"id": match_id}, {"$addToSet": {"players": player.id}})
                    return True
                else: #А иначе он идёт нахуй!
                    return False

    def start(self, match_id: int,) -> str:
        point_sum: int = 0
        self.coll.update({"id": match_id}, {"$set": {"status": True}})
        if 371291041640218647 in self.coll.find_one({"id": match_id})["players"]:
            host = 371291041640218647 #Если в данном матче есть доверенное лицо, делаем его хостом!
        else:
            host = random.choice(self.coll.find_one({"id": match_id})["players"]) #Или выбираем хоста рандомно
        self.coll.update({"id": match_id}, {"$set": {"host": host}})
        for user in self.coll.find_one({"id": match_id})["players"]:
            point_sum += db.Users.find_one({"id": user})["points"]
        avg_point = point_sum/len(self.coll.find_one({"id": match_id})["players"]) #Средний рейтинг игроков
        self.coll.update({"id": match_id}, {"$set": {"avg_rating": avg_point}})
        str_host = db.Users.find_one({"id": host})["name"] #никнейм хоста
        return str_host, avg_point

    def remake(self, player: User, match_id: int) -> bool:
        if player.id == self.coll.find_one({"id": match_id})["host"]:
            for user in self.coll.find_one({"id": match_id})["players"]:
                db.Users.update({"id": user}, {"$set": {"in_game": False}})
            self.coll.delete_one({"id": match_id})
            return True
        else:
            return False

    def result(self, player: User, match_id: int, mention_list: List[Any]) -> bool:
        host = self.coll.find_one({"id": match_id})["host"]
        avg_point = self.coll.find_one({"id": match_id})["avg_rating"]
        if player.id == host: #Статистику отдаёт хост
            for arg in enumerate(mention_list): #Тактика следующая, всегда есть победитель. Проигравших может не быть
                if arg[0] == 0: #Победитель всегда передаётся первым среди всех аргументов
                    db.Users.update({"id": arg[1]}, {"$inc": {"wins": 1, "matches": 1, "points": avg_point*0.25}})
                    db.Users.update({"id": arg[1]}, {"$set": {"in_game": False}})
                    self.coll.update({"id": match_id}, {"$pull": {"players": arg[1]}})
                else: #После - идут проигравшие. Их может быть несколько
                    db.Users.update({"id": arg[1]}, {"$inc": {"loses": 1, "matches": 1, "points": -avg_point*0.1}})
                    db.Users.update({"id": arg[1]}, {"$set": {"in_game": False}})
                    self.coll.update({"id": match_id}, {"$pull": {"players": arg[1]}})
            for user in self.coll.find_one({"id": match_id})["players"]: #Остальные игроки, по которым не передали статистику считаются выжившими.
                db.Users.update({"id": user}, {"$inc": {"survives": 1, "matches": 1, "points": avg_point*0.15}})
                db.Users.update({"id": user}, {"$set": {"in_game": False}})
            self.coll.delete_one({"id": match_id})
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

