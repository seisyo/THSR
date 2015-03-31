from functools import wraps
from flask import Flask,request,current_app,json
from flask.ext import restful
from flask.ext.restful import Resource,Api
from datetime import datetime
from flask.ext.jsonpify import jsonify

import pymysql
import time


##import json ##as sys_json

app = Flask(__name__)
api = Api(app)

info = {} ##要存列車資訊的dictionary

def convertstation(dep,arr):
	depnum = int(dep.replace("taipei","1").replace("banqiao","2").replace("taoyuan","3").replace("hsinchu","4").replace("taichung","5").replace("chiayi","6").replace("tainan","7").replace("zuoying","8"))
	arrnum = int(arr.replace("taipei","1").replace("banqiao","2").replace("taoyuan","3").replace("hsinchu","4").replace("taichung","5").replace("chiayi","6").replace("tainan","7").replace("zuoying","8"))
	if depnum > arrnum:
		return '北上'
	elif depnum < arrnum:
		return '南下'
	else:
		print('error')

def convertdeltatostr(obj):
	if type(obj) == 'datetime.timedelta' or type(obj) == 'datetime.data':
		return str(obj)
	else:
		return obj

class searchtraintime(Resource):
	
	def get(self):

		info = {'depsta':request.values['depsta'],'arrsta':request.values['arrsta'],'date':request.values['date'],'time':request.values['time']}
		md = datetime.strptime(info['date'],'%m/%d')
		md = md.replace(year = 2015)
		
		if md >= datetime.strptime('2015-4-2','%Y-%m-%d') and md <= datetime.strptime('2015-4-7','%Y-%m-%d'):
			conn = pymysql.connect(host = '127.0.0.1',database = 'THSRstutimeSPtime',user = 'root',charset = 'utf8')
			cursor = conn.cursor()##連接資料庫的設定
			md = md

			result =("""
			select distinct `traindate`.`trainnum`,`traindate`.`traindate`,`traintime`.`{departure}`,`traintime`.`{arrive}`,`traindate`.`discount`
			from `traindate` 
			join `traintime` on `traindate`.`trainnum` = `traintime`.`trainnum` 
			where `traindate`.`traindate` = '{date}' and `traintime`.`{departure}` > '{deptime}' and traintime.direction = '{direction}' and `traintime`.`{departure}` is not null and `traintime`.`{arrive}` is not null ORDER BY `traintime`.`{departure}`"""
			.format(departure = info['depsta'],arrive = info['arrsta'],date = md,deptime = info['time'],direction = convertstation(info['depsta'],info['arrsta'])))
			
		else:
			conn = pymysql.connect(host = '127.0.0.1',database = 'THSRstutime2',user = 'root',charset = 'utf8')
			cursor = conn.cursor()##連接資料庫的設定

			if md == datetime.strptime('2015-4-1','%Y-%m-%d'):
				result =("""
				select distinct `traindate`.`trainnum`,`traindate`.`traindate`,`traintime`.`{departure}`,`traintime`.`{arrive}`,`traindate`.`discount`
				from `traindate` 
				join `traintime` on `traindate`.`trainnum` = `traintime`.`trainnum` 
				where `traindate`.`traindate` in('3','4/1') and `traintime`.`{departure}` > '{deptime}' and traintime.direction = '{direction}' and `traintime`.`{departure}` is not null and `traintime`.`{arrive}` is not null ORDER BY `traintime`.`{departure}`"""
				.format(departure = info['depsta'],arrive = info['arrsta'],deptime = info['time'],direction = convertstation(info['depsta'],info['arrsta'])))
			else:
				md = int(datetime.date(md).weekday())+ 1
				result =("""
				select distinct `traindate`.`trainnum`,`traindate`.`traindate`,`traintime`.`{departure}`,`traintime`.`{arrive}`,`traindate`.`discount`
				from `traindate` 
				join `traintime` on `traindate`.`trainnum` = `traintime`.`trainnum` 
				where `traindate`.`traindate` = '{date}' and `traintime`.`{departure}` > '{deptime}' and traintime.direction = '{direction}' and `traintime`.`{departure}` is not null and `traintime`.`{arrive}` is not null ORDER BY `traintime`.`{departure}`"""
				.format(departure = info['depsta'],arrive = info['arrsta'],date = md,deptime = info['time'],direction = convertstation(info['depsta'],info['arrsta'])))
		

		print(result)
		cursor.execute(result)
		data = list(cursor.fetchall())##將tuple換成list
		# print(data)
		
		dicdataout = {}##存進要jsonify的資料到dictionary中，方便輸出
		for a in enumerate(data):
			data[a[0]] = list(data[a[0]])
			dicdata = {}
			key = 0
			for index in enumerate(data[a[0]]):
				if index[0] == 1:
					data[a[0]][index[0]] = info['date']
				elif index[0] == 2 or index[0] == 3:
					data[a[0]][index[0]] = str(data[a[0]][index[0]])
				else:
					data[a[0]][index[0]] = data[a[0]][index[0]]
				dicdata[int(key)] = data[a[0]][index[0]]##每一筆各自存進去
				key += 1
			dicdataout[int(a[0])] = dicdata
		# print(dicdataout,type(dicdataout))
		
		# print(json.jsonify(dicdataout))
		
		# return jsonify(dicdataout)
		return jsonify(dicdataout)

api.add_resource(searchtraintime,'/searchtrain')
if __name__ == '__main__':
	app.run(debug = True)