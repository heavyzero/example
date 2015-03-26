import sqlite3

DB="uuhw.db"

def exec_sql(sql,*argv):
	con = None
	cur = None
	try:
		sql = sql %argv
		print sql
		con = sqlite3.connect(DB)
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		return cur.fetchall()
	except Exception ,e:
		print e
	finally:
		if cur != None:
			cur.close()
		if con != None:
			con.close()

def create_db():
	sqls = [
	'''
	create table travel_info
	( 
	tid INTEGER PRIMARY KEY,
	title VARCHAR(256),
	href VARCHAR(256),
	date VARCHAR(64),
	status VARCHAR(64),
	price VARCHAR(64)
	)
	'''
	,
	'''
	create table travel_signup
	( 
	id INTEGER PRIMARY KEY,
	name VARCHAR(256),
	tid INTEGER
	)
	''']

	for sql in sqls:
		exec_sql(sql)
def save_travel_info(tid=1,title="None",href="www.example.com",date="2015-3-26",status="ok",price=0):
    return exec_sql('''
				insert into travel_info(tid,title,href,date,status,price) 
				values(%d,"%s","%s","%s","%s","%s")
    ''',tid,title,href,date,status,price)
def del_travel_signup(tid):
    exec_sql('delete from travel_signup where tid = "%s"',tid)
def save_travel_signup(name,tid):
    exec_sql('''
				insert into travel_signup(name,tid) values("%s",%d)
    ''',name,tid)
