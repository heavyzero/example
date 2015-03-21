#-*- coding:utf-8 -*-
import lxml.html
import requests
import os
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

#只有一定机率获得到 报名人数
def get_signup(text):
	html= lxml.html.document_fromstring(text)
	txpaths = [
			'//table[@class="t_table"]/tr/td/div/font/text()',
			'//table[@class="t_table"]/tr/td/div/text()',
			'//table[@class="t_table"]/tr/td/text()'
			]
	ret = []
	for p in txpaths:
		data = html.xpath(p)
		ret += data
	return ret

#可能找到正确的
def get_price(text):
	html= lxml.html.document_fromstring(text)
	txpaths = [
				'//font[@size=6]//font[@color="#ff0000"]/text()',
				'//font[@size=5]//font[@color="#ff0000"]/text()',
				'//font[@size=5]//font[@color="#ff0000"]/font/text()',
				'//font[@size=5 and @color="#ff0000"]/text()',
				'//font[@size=5]/b/span/text()',
				'//font[@color="#ff0000"]/font[@size=5]/b/text()'
			]
	for p in txpaths:
		ret = html.xpath(p)
		if len(ret) > 0:
			return ret[0]
def main():
	host ="http://www.uuhw.cn"
	url = 'http://www.uuhw.cn/api.php?mod=ad&adid=custom_3'
	r = requests.get(url)
	doc = lxml.html.document_fromstring(r.text)
	r.close()
	a = doc.xpath('//div[@id="wow"]')[0]
	titles = a.xpath('div[@class="we"]/div[@class="we-title"]/a/text()')
	hrefs = [ os.path.join(host,path) for path in  a.xpath('div[@class="we"]/div[@class="we-title"]/a/@href')]
	others = a.xpath('div[@class="we"]/div[@class="we-other"]/text()')
	#报名情况
	statuss = a.xpath('div[@class="we"]/div[@class="we-other"]/b/text()')
	peoples = []
	prices = []
	for url in hrefs:
		print "process init"
		#防止阻塞死掉
		r = None
		try:
			r =  requests.get(url,timeout=5)
			signups = get_signup(r.text)
			peoples.append(signups)
			price = get_price(r.text)
			prices.append(price)
		except Exception ,e:
			print e
		finally:
			if r != None:
				r.close()
	travel_data =  zip(titles,hrefs,others,statuss,prices,peoples)
	#更新数据库
	print "xdrerer"
	for item in travel_data:
		tid = int(item[1][item[1].rindex('=')+1:])
		exec_sql('''
				insert into travel_info(tid,title,href,date,status,price) 
				values(%d,"%s","%s","%s","%s","%s")
				''',tid,item[0],item[1],item[2],item[3],item[4])
		exec_sql('delete from travel_signup where tid = "%s"',tid)
		for p in item[5]:
			exec_sql('''
				insert into travel_signup(name,tid) values("%s",%d)
				''',p,tid)
if __name__  == '__main__':
	main()
