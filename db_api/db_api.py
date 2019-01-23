#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import MySQLdb
from operator import itemgetter

app = Flask(__name__)
api = Api(app)
try:
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "zrada", "zrada", charset='utf8', use_unicode = True )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
except Exception as err:
    print(err)
    # disconnect from server
    db.close()

@app.route('/db_api/topenactments', methods=['get'])
@cross_origin()
def get_top_enactments():
    try:
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

    return jsonify({"enactments": list_enactments}) 

@app.route('/db_api/process', methods=['post'])
@cross_origin()
def process_user_votes():
    data = request.get_json()
    #print(data)
    result  = process_voting(data)
    return result, 201


def process_voting(data):

    sql = "SELECT * FROM deputats WHERE candidate <> 0"
    cursor.execute(sql)
    deputats = cursor.fetchall()
    voting_matches = {}
    print(len(deputats))
    for element in data:

        for deputat in deputats:
            sql = """SELECT * FROM voting WHERE person = "'%s'" AND enactment = "%s" AND vote = "'%s'";""" % (deputat[0], element['enactment'], element['vote'],)
            print(sql)
            cursor.execute(sql)
            match = cursor.fetchone()
            print(match)
            if(match):
                if deputat[0] in voting_matches:
                    voting_matches[deputat[0]]['matches']+=1

                else:
                    voting_matches[deputat[0]]={'name': deputat[1], 'matches': 1}


    sorted_result = sorted(voting_matches.items(), key=lambda x: x[1], reverse=True)
    print(sorted_result)
    return jsonify(sorted_result)



if __name__ == '__main__':
    app.run(debug=True)


db.close()
