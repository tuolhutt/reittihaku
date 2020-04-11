#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Solidabis koodihaaste (3.5.20) - https://koodihaaste.solidabis.com/
#
# Author: Tuomo Huttu
# Date:   11.4.2020


import time
import json


roadtable_file="static/reittiopas.json"
coordinates_file="static/coordinates.json"
colors_file="static/colors.json"

roadtable,coordinates,shortest="","",""


def main():
    global roadtable_file,coordinates_file
    global roadtable,coordinates,shortest

    roadtable=read_json(roadtable_file)
    coordinates=read_json(coordinates_file)
    colors=read_json(colors_file)

    shortest=calculate_shortest_routes(roadtable)
    #print(shortest["A"]["B"])
    
    return "done"



def calculate_shortest_routes(roadtable):
    stops=roadtable["pysakit"]
    routes=roadtable["linjastot"]
    roads=roadtable["tiet"]

    ret=dict() #dict to return
    for stop in stops:
        aa=dict()
        aa["neighbors"]=[]
        aa[stop]=dict(route=[],length=0)
        for stop2 in stops:
            if stop!=stop2:
                aa[stop2]=dict(route=[],length=999)
        ret[stop]=aa

    #solve neighbors and add neighbor-lengths
    for key in routes.keys():
        route=routes[key]
        for i in range(len(route)-1):
            for road in roads:
                road_pair=[road["mista"],road["mihin"]]
                if (route[i] in road_pair) and (route[i+1] in road_pair):
                    if route[i] not in ret[route[i+1]]["neighbors"]:
                        ret[route[i+1]]["neighbors"].append(route[i])
                        ret[route[i+1]][route[i]]["length"]=road["kesto"]
                        ret[route[i+1]][route[i]]["route"].append([route[i+1],route[i]])
                    if route[i+1] not in ret[route[i]]["neighbors"]:
                        ret[route[i]]["neighbors"].append(route[i+1])
                        ret[route[i]][route[i+1]]["length"]=road["kesto"]
                        ret[route[i]][route[i+1]]["route"].append([route[i],route[i+1]])
                    break
    
    #iteration to solve shortest routes
    last_iteration=""
    while True:
        for stop in stops:
            for stop2 in stops:
                if stop!=stop2:
                    for n in ret[stop]["neighbors"]:
                        #length: start--neighbor + neighbor--end
                        le=ret[stop][n]["length"]+ret[n][stop2]["length"]
                        #update if shorter route found
                        if le<ret[stop][stop2]["length"]:
                            ret[stop][stop2]["length"]=le
                            ret[stop][stop2]["route"]=[]
                            for r in ret[n][stop2]["route"]:
                                ret[stop][stop2]["route"].append([stop]+r)
                        elif le==ret[stop][stop2]["length"]:
                            for r in ret[n][stop2]["route"]:
                                new_r=[stop]+r
                                if new_r not in ret[stop][stop2]["route"]:
                                    ret[stop][stop2]["route"].append(new_r)
        
        new_iteration=""
        for stop in stops:
            for stop2 in stops:
                for r in ret[stop][stop2]["route"]:
                    new_iteration+=str(r)
        if new_iteration==last_iteration:
            break
        last_iteration=new_iteration
    
    #calculate routes recursively to choose route combination with minimum shifts
    betweens=colors_between_stops(roadtable)
    for stop in stops:
        for stop2 in stops:
            ret[stop][stop2]["colors"]=[]
            ret[stop][stop2]["shifts"]=[]
            if stop!=stop2:
                for s in ret[stop][stop2]["route"]:
                    shift_count,colors=colors_recursive(s,betweens)
                    ret[stop][stop2]["colors"].append(colors)
                    ret[stop][stop2]["shifts"].append(shift_count)

    return ret


def colors_between_stops(roadtable):
    stops=roadtable["pysakit"]
    routes=roadtable["linjastot"]

    ret=dict() #dict to return
    for stop in stops:
        aa=dict()
        for stop2 in stops:
            if stop!=stop2:
                aa[stop2]=dict(routes=[])
        ret[stop]=aa
    
    for key in routes.keys():
        route=routes[key]
        for i in range(len(route)-1):
            if key not in ret[route[i]][route[i+1]]["routes"]:
                ret[route[i]][route[i+1]]["routes"].append(key)
            if key not in ret[route[i+1]][route[i]]["routes"]:
                ret[route[i+1]][route[i]]["routes"].append(key)
    
    return ret


def colors_recursive(stops,betweens,last_route=""):
    routes=betweens[stops[0]][stops[1]]["routes"]

    if len(stops)>2:
        if last_route in routes:
            shift_count,ret_routes=colors_recursive(stops[1:],betweens,last_route)
            return shift_count,[last_route]+ret_routes
        else:
            shift_count,ret_routes,ret_route=999,"",""
            for r in routes:
                sc,rr=colors_recursive(stops[1:],betweens,r)
                if sc<shift_count:
                    shift_count=sc
                    ret_routes=rr
                    ret_route=r
            if last_route:
                return shift_count+1,[ret_route]+ret_routes
            else:
                return shift_count,[ret_route]+ret_routes
    else:
        if last_route in routes:
            return 0,[last_route]
        elif not last_route:
            return 0,[routes[0]]
        else:
            return 1,[routes[0]]

    return 0,"" #return shift_count,ret_routes


def get_modded_stop_coordinates(coordinates,scale):
    ret="["
    first=True
    for key in coordinates["stops"].keys():
        if first:
            first=False
        else:
            ret+=","
        stop=coordinates["stops"][key]
        ret+=str(dict(name=str(key),x=(stop["x"]+1)*scale,y=(stop["y"]+1)*scale)).replace("'",'"')
    ret+="]"
    return ret


def get_modded_line_coordinates(coordinates,roadtable,scale):
    roads=roadtable["tiet"]
    ret="["
    first=True
    for road in roads:
        if first:
            first=False
        else:
            ret+=","
        stop=coordinates["stops"][road["mista"]]
        stop2=coordinates["stops"][road["mihin"]]
        ret+=str(dict(x1=(stop["x"]+1)*scale,y1=(stop["y"]+1)*scale,x2=(stop2["x"]+1)*scale,y2=(stop2["y"]+1)*scale)).replace("'",'"')
    ret+="]"
    return ret


def get_modded_route_coordinates(coordinates,shortest,colors,scale):
    ret="["
    first=True
    for i in range(len(shortest["shifts"])):
        if first:
            first=False
        else:
            ret+=","
        ret+="["
        first2=True
        for j in range(len(shortest["route"][i])-1):
            if first2:
                first2=False
            else:
                ret+=","
            stop=coordinates["stops"][shortest["route"][i][j]]
            stop2=coordinates["stops"][shortest["route"][i][j+1]]
            c=str(colors[shortest["colors"][i][j]])
            ret+=str(dict(color=c,x1=(stop["x"]+1)*scale,y1=(stop["y"]+1)*scale,x2=(stop2["x"]+1)*scale,y2=(stop2["y"]+1)*scale)).replace("'",'"')
        ret+="]"
    ret+="]"
    return ret


def get_routes_info(shortest):
    ret=[]
    for i in range(len(shortest["shifts"])):
        route="-".join(shortest["route"][i])
        ret.append(dict(shifts=shortest["shifts"][i],route=route,length=shortest["length"]))
    return ret


def read_json(file):
    data={}
    with open(file) as f:
        data = json.load(f)
    return data



if __name__ == "__main__":
    start_time=time.time()
    print(str(main()))
    print("time: "+str(round(time.time()-start_time,3))+"s")

