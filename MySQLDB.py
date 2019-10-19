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
        answer = "user already exist!"
    else:
        _SQL = f'INSERT INTO users(name, id) VALUES("{str(name)}", {str(id)});'
        cur.execute(_SQL)
        conn.commit()
        answer = "user added!"
    cur.close()
    conn.close()
    return answer


def registration(id, match_id):
    conn = mysql.connector.connect(**dbconfig)
    cur = conn.cursor()
    _SQL = f'SELECT * FROM status WHERE user_id = {str(id)}
    cur.execute(_SQL)
    res = cur.fetchall()
    if len(res) == 0:
        _SQL = f'SELECT start FROM match_status WHERE match_id = {str(match_id)}'
        cur.execute(_SQL)
        res = cur.fetchone()
        if res[0] == 1:
            cur.close()
            conn.close()
            return False
        else:
            _SQL = f'INSERT INTO status (match_id, user_id) VALUES ({str(match_id)}, {str(id)})'
            cur.execute(_SQL)
            conn.commit()
            cur.close()
            conn.close()
            return True
    else:
        return "Вы уже в игре! Сдайте отчёт с предыдущей игры!"


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
    _SQL = f'UPDATE match_status SET average_points={str(avg)}'
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
    _SQL = f'SELECT host_id WHERE match_id={str(id)}'
    cur.execute(_SQL)
    res = cur.fetchone()
    if res[0] != host:
        return False
    else:
        
