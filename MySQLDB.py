import mysql.connector

dbconfig = { 'host': 'eu-cdbr-west-02.cleardb.net',
             'user': 'bca611917ce10f',
             'password': '6f307489',
             'database': 'heroku_4e4d24d83d2a5ae', }

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
        _SQL = f'INSERT INTO users(name, id) VALUES("{name}", {str(id)});'
        cur.execute(_SQL)
        conn.commit()
        answer = "user added!"
    cur.close()
    conn.close()
    return answer
