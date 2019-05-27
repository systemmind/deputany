#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import MySQLdb
from operator import itemgetter

app = Flask(__name__)
api = Api(app)
app.config.update(SERVER_NAME='casper.uk.to:5000')

@app.route('/db_api/topenactments', methods=['GET'])
@cross_origin()
def get_top_enactments():
    try:
        connection = MySQLdb.connect("localhost", "voter", "deputany", "zrada", charset='utf8', use_unicode = True)
        cursor = connection.cursor()
        sql = "SELECT * FROM enactments where reiting LIKE 1"
        cursor.execute(sql)
        enactments = cursor.fetchall()
        list_enactments = []
    except Exception as err:
        print(err)
        abort(404)

    for enactment in enactments:
        list_enactments.append({"url": enactment[0],
                                "date": enactment[1],
                                "time": enactment[2],
                                "description": enactment[3],
                                "result": enactment[4]})
    connection.close()
    return jsonify({"enactments": list_enactments}) 

@app.route('/db_api/process', methods=['POST'])
@cross_origin()
def process_user_votes():
    data = request.get_json()
    connection = MySQLdb.connect("localhost", "voter", "deputany", "zrada", charset='utf8', use_unicode = True)
    result  = process_voting(data, connection)
    connection.close()
    return result, 201

def process_voting(data, connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM deputats"
    cursor.execute(sql)
    deputats = cursor.fetchall()
    voting_matches = {}
    for element in data:
      sql = """SELECT * FROM voting WHERE enactment = "%s" AND vote = "'%s'";""" % (element['enactment'], element['vote'],)
      cursor.execute(sql)
      list_voting = list(cursor.fetchall())
      for deputat in deputats:
        for tupl in list_voting:
          if tupl[0] == "'"+deputat[0]+"'":

            if deputat[0] in voting_matches:
              voting_matches[deputat[0]]['matches']+=1

            else:
              voting_matches[deputat[0]]={'name': deputat[1], 'matches': 1}

    sorted_result = sorted(voting_matches.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_result)


if __name__ == '__main__':
    app.run(debug=True)


db.close()
