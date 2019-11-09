import mysql.connector
import random

dbconfig = {'host': 'eu-cdbr-west-02.cleardb.net',
            'user': 'bca611917ce10f',
            'password': '6f307489',
            'database': 'heroku_4e4d24d83d2a5ae'}


def add_user(name, id):
    answer = ""
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT id FROM users WHERE id={str(id)}'
    cur.execute(_SQL)
    res = cur.fetchall()
    if len(res) > 0:
        answer = False
    else:
        _SQL = f'INSERT INTO users(name, id) VALUES("{str(name)}", {str(id)});'
        cur.execute(_SQL)
        conn.commit()
        answer = True
    cur.close()
    conn.close()
    return answer


def registration(id, match_id, civ1, civ2):
    """
    Регистрирует участника в матч
    """
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT id FROM users WHERE id={str(id)}' # Получаем юзера из БД
    cur.execute(_SQL)
    res = cur.fetchall()
    if len(res) == 0:
        cur.close()
        conn.close()
        return False, False, False #Есть в БД? Может участвовать в матче? Может присоединиться к ЭТОМУ матчу?
    _SQL = f'SELECT * FROM status WHERE user_id = {str(id)}' #Получаем информацию о нахождении в игре
    cur.execute(_SQL)
    res = cur.fetchall()
    if len(res) == 0: #Если не в игре, то идём дальше
        _SQL = f'SELECT start FROM match_status WHERE match_id = {str(match_id)}'
        cur.execute(_SQL)
        res = cur.fetchone()
        try:
            if res[0] == 1:
                cur.close()
                conn.close()
                return True, True, False #Пользователь не в игре, НО регистрация на текущий матч закрыта
            else:
                _SQL = f'INSERT INTO status(match_id, user_id) VALUES({str(match_id)}, {str(id)})'
                cur.execute(_SQL)
                _SQL = f'INSERT INTO banned(user_id, ban1, ban2) VALUES({str(id)}, "{str(civ1)}", "{str(civ2)}")'
                cur.execute(_SQL)
                conn.commit()
                cur.close()
                conn.close()
                return True, True, True #Пользователь присоединился к этой игре
        except TypeError:
            _SQL = f'INSERT INTO match_status(match_id) VALUES({str(match_id)})'
            cur.execute(_SQL)
            _SQL = f'INSERT INTO status(match_id, user_id) VALUES({str(match_id)}, {str(id)})'
            cur.execute(_SQL)
            _SQL = f'INSERT INTO banned(user_id, ban1, ban2) VALUES({str(id)}, "{str(civ1)}", "{str(civ2)}")'
            cur.execute(_SQL)
            conn.commit()
            cur.close()
            conn.close()
            return True, True, True #Пользователь создал новую игру.
    else:
        return True, False, False #В базе данных, но находится в игре.

def leave(id):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT id FROM users WHERE id={str(id)}' # Получаем юзера из БД
    cur.execute(_SQL)
    res = cur.fetchall()
    if len(res) == 0:
        cur.close()
        conn.close()
        return False, False, False #Нет в БД
    try:
        _SQL = f'SELECT match_id FROM status WHERE user_id = {str(id)}'
        cur.execute(_SQL)
        match_id = cur.fetchone()
        _SQL = f'SELECT start FROM match_status WHERE match_id = {str(match_id[0])}'
        cur.execute(_SQL)
        res2 = cur.fetchone()
    except TypeError:
        return True, False, False
    if res2[0] == 1:
        return True, True, False  #Матч уже начался
    else:
        _SQL = f'DELETE FROM status WHERE user_id = {str(id)}'
        cur.execute(_SQL)
        conn.commit()
        cur.close()
        conn.close()
        return True, True, True #Вышел из матча


def unbanned(id):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT ban1, ban2 FROM banned WHERE user_id={str(id)}'
    cur.execute(_SQL)
    _SQL = f'DELETE FROM banned WHERE user_id={str(id)}'
    cur.execute(_SQL)
    banned_civs = cur.fetchone()
    return banned_civs[0], banned_civs[1]


def host_rand(players):
    sum = 0
    host_index = random.randint(0, len(players))
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT match_id FROM status WHERE user_id={str(players[0])}'
    cur.execute(_SQL)
    res = cur.fetchone()
    for player in players:
        _SQL = f'SELECT point FROM users WHERE id={str(player)}'
        cur.execute(_SQL)
        points = cur.fetchone()
        sum += points[0]
    avg = sum/len(players)
    _SQL = f'UPDATE match_status SET average_points={str(avg)} WHERE match_id={str(res[0])}'
    cur.execute(_SQL)
    conn.commit()
    _SQL = f'UPDATE match_status SET host_id={str(players[host_index])} WHERE match_id={str(res[0])}'
    cur.execute(_SQL)
    conn.commit()
    cur.close()
    conn.close()


def start(id):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'UPDATE match_status SET start=1 WHERE match_id={str(id)}'
    cur.execute(_SQL)
    conn.commit()
    _SQL = f'SELECT host_id, average_points WHERE match_id={str(id)}'
    cur.execute(_SQL)
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res


def statistic(id):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT * FROM users WHERE id={str(id)}'
    cur.execute(_SQL)
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res


def result(host, id, *args):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT host_id from match_status WHERE match_id={str(id)}'
    cur.execute(_SQL)
    res = cur.fetchone()
    if res[0] != host:
        return False
    else:
        for player in enumerate(args):
            _SQL = f'SELECT id FROM users WHERE name={str(player[1])}'
            cur.execute(_SQL)
            res = cur.fetchone()
            _SQL = f'DELETE FROM status WHERE user_id={str(res[0])}'
            cur.execute(_SQL)
            conn.commit()
            _SQL = f'SELECT average_points FROM match_status WHERE host_id={str(host)}'
            cur.execute(_SQL)
            avg_points = cur.fetchone()[0]
            _SQL = f'UPDATE users SET games = games + 1 WHERE id={str(res[0])}'
            cur.execute(_SQL)
            conn.commit()
            if player[0] == 0:
                _SQL = f'UPDATE users SET wins = wins + 1 WHERE id={str(res[0])}'
                cur.execute(_SQL)
                conn.commit()
                _SQL = f'UPDATE users SET points = points + {int(avg_points*0.35)} WHERE id={str(res[0])}'
                cur.execute(_SQL)
                conn.commit()
            else:
                _SQL = f'UPDATE users SET loses = loses + 1 WHERE id={str(res[0])}'
                cur.execute(_SQL)
                conn.commit()
                _SQL = f'UPDATE users SET points = points - {int(avg_points*0.15)} WHERE id={str(res[0])}'
                cur.execute(_SQL)
                conn.commit()
        _SQL = f'SELECT user_id FROM status WHERE match_id={str(id)}'
        cur.execute(_SQL)
        res = cur.fetchall()
        for survivors in res:
            _SQL = f'DELETE FROM status WHERE user_id={str(survivors[0])}'
            cur.execute(_SQL)
            conn.commit()
            _SQL = f'UPDATE users SET games = games + 1 WHERE id={str(survivors[0])}'
            cur.execute(_SQL)
            conn.commit()
            _SQL = f'UPDATE users SET survives = survives + 1 WHERE id={str(survivors[0])}'
            cur.execute(_SQL)
            conn.commit()
            _SQL = f'UPDATE users SET points = points + {int(avg_points*0.2)} WHERE id={str(survivors[0])}'
        cur.close()
        conn.close()
        return True
