#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Solidabis koodihaaste (3.5.20) - https://koodihaaste.solidabis.com/
#
# Author: Tuomo Huttu
# Date:   11.4.2020


from flask import Flask, redirect, url_for, render_template,request
from sys import argv
from reitti import *


roadtable_file="reittiopas.json"
coordinates_file="coordinates.json"
colors_file="colors.json"

app=Flask(__name__)

scale=33

roadtable,coordinates,shortest="","",""
stops_coordinates,roads_coordinates=[],[]
stops,colors=[],[]


@app.route('/')
def tyhja():
    return redirect(url_for('reitti'))


@app.route('/reitti',methods=['POST','GET'])
def reitti():
    global coordinates,scale
    global stops_coordinates,roads_coordinates
    global stops

    try:
        stop1=request.form['stop1'].upper()
        stop2=request.form['stop2'].upper()
    except:
        stop1,stop2="",""
    
    error=""
    if not stop1 and not stop2:
        pass
    elif (stop1 not in stops) or (stop2 not in stops):
        error=u"Virheellinen syöte."
    elif stop1==stop2:
        error=u"Syötteet ovat samat."
    
    routes=[]
    if stop1!=stop2 and stop1 in stops and stop2 in stops:
        routes=get_modded_route_coordinates(coordinates,shortest[stop1][stop2],colors["colors"],scale)
    
    route_infos=[]
    if routes:
        route_infos=get_routes_info(shortest[stop1][stop2])
    
    return render_template('reitti.html',stop1=stop1,stop2=stop2,stops=stops_coordinates,roads=roads_coordinates,routes=routes,route_count=len(route_infos),route_infos=route_infos,error=error)



def start():
    global roadtable_file,coordinates_file,colors_file
    global roadtable,coordinates,shortest
    global stops_coordinates,roads_coordinates,scale
    global stops,colors

    roadtable=read_json(roadtable_file)
    coordinates=read_json(coordinates_file)
    colors=read_json(colors_file)

    shortest=calculate_shortest_routes(roadtable)

    stops_coordinates=get_modded_stop_coordinates(coordinates,scale)
    roads_coordinates=get_modded_line_coordinates(coordinates,roadtable,scale)

    stops=roadtable["pysakit"]


if __name__ == '__main__':
    start()

    use_local=False
    try:
        if argv[1]=="local":
            use_local=True
    except:
        pass
    
    if use_local:
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=80)
