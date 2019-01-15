#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import MySQLdb


app = Flask(__name__)
api = Api(app)
try:
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "Elisey2011", "zrada", charset='utf8', use_unicode = True )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
except Exception as err:
    print(err)
    # disconnect from server
    db.close()

@app.route('/db_api/deputats/names', methods=['GET'])
@cross_origin()
def get_deputats_names():
    try:
        sql = "SELECT * FROM deputats"
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the deputats
        deputats = cursor.fetchall()
        list_deputats =  []
    except Exception as err:
        print(err)
        return None

    for deputat in deputats:
        list_deputats.append({'url': deputat[0], 'name': deputat[1]})

    return jsonify({'deputats': list_deputats})
        
@app.route('/db_api/deputats/url/<name>', methods=['get'])
@cross_origin()
def get_url_by_name(name):
    try:
        sql = "SELECT * FROM deputats WHERE name = '" + name.encode('utf-8') + "'"
        cursor.execute(sql)
        deputat = cursor.fetchone()
        return jsonify({deputat[1]: deputat[0]})
    except Exception as err:
        print(err)
        abort(404)       

@app.route('/db_api/enactments', methods=['get'])
@cross_origin()
def get_enactments():
    try:
        sql = "SELECT * FROM enactments"
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

@app.route('/db_api/votes/<name>')
@cross_origin()
def get_votes_by_name(name):
    try:
        sql = "SELECT * FROM deputats WHERE name = '" + name.encode('utf-8') + "'"
        cursor.execute(sql)
        deputat = cursor.fetchone()
        sql = "SELECT * FROM votes WHERE person = '" + deputat[0] + "'"
        cursor.execute(sql)
        votes = cursor.fetchall()
        list_votes = []
        for vote in votes:
            list_votes.append({"enactment": vote[1], "vote": vote[2]})

        return jsonify({"votes": list_votes})
    except Exception as err:
        print(err)
        abort(404) 


if __name__ == '__main__':
    app.run(debug=True)


db.close()
