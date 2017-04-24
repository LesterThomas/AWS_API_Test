#!/usr/bin/env python

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobal,LocationGlobalRelative, Command, mavutil, APIException
import boto3    
import time
import json
import math
import os
import web
import logging

simulatorArray = [] 
MAX_SIMULATORS=5 #Maximum number of simulators allowed

 
logging.basicConfig(level=logging.DEBUG)
def applyHeadders():
    logging.debug('Applying HTTP headers')
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin',      '*')
    web.header('Access-Control-Allow-Credentials', 'true')        
    web.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')   
    web.header('Access-Control-Allow-Headers', 'Content-Type')      
    return

class index:        
    def GET(self):
        logging.info( "#####################################################################")
        logging.info( "Method GET of index")
        logging.info( "#####################################################################")
        applyHeadders()
        outputObj={}
        outputObj['_links']={
            'self':{"href": homeDomain},
            'simulator':{
                'operations':  [
                    {"method":"GET",
                    "description":"Return the collection of available drone simulators"},
                    {"method":"POST",
                    "description":"Create a new drone simulator. It will return the id of the simulator.",
                    "samplePayload":{}}],
                    "href": homeDomain+"/simulator" }}
        outputObj['id']="EntryPoint"
        output=json.dumps(outputObj)    
        return output

class simulatorIndex:        
    def GET(self):
        logging.info( "#####################################################################")
        logging.info( "Method GET of simulatorIndex")
        logging.info( "#####################################################################")
        applyHeadders()
        ec2client=boto3.client('ec2')
        response=ec2client.describe_instances()
        instances=[]
        outputObj=[]
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if ((instance["State"]["Name"]=="running") | (instance["State"]["Name"]=="pending") ):
                    outputObj.append( {"id":instance["InstanceId"],
                        "details":{"method":"GET","href":homeDomain+"/simulator/"+str(instance["InstanceId"])+"/","description":"Get status for drone simulator " + str(instance["InstanceId"]),"instanceType":str(instance["InstanceType"]),"simulatorHref":"http://"+str(instance["PublicDnsName"])+":1235","status":instance["State"]["Name"]}})
                    print(instance["InstanceId"],instance["InstanceType"],instance["State"]["Name"])  
                else :
                    print("Not included:",instance["InstanceId"],instance["InstanceType"],instance["State"]["Name"])  

                #print(instance)
        #print(outputObj)
        output=json.dumps(outputObj)    
        return output

    def POST(self):
        logging.info( "#####################################################################")
        logging.info( "Method POST of simulatorIndex")
        logging.info( "#####################################################################")
        applyHeadders()
        data = json.loads(web.data())
        connection = data["connection"]
        logging.debug( connection)
        simulatorArray.append(connection)
        connectionArray.append(None)
        authorizedZoneArray.append({})
        outputObj={}
        outputObj["connection"]=connection
        outputObj["id"]=len(simulatorArray)-1
        return json.dumps(outputObj)

    def OPTIONS(self, simulatorId):
        logging.info( "#####################################################################")
        logging.info( "Method OPTIONS of action - just here to suppor the CORS Cross-Origin security")
        logging.info( "#####################################################################")
        applyHeadders()

        outputObj={}
        output=json.dumps(outputObj)   
        return output

class catchAll:
    def GET(self, user):
        logging.info( "#####################################################################")
        logging.info( "Method GET of catchAll")
        logging.info( "#####################################################################")
        applyHeadders()
        logging.debug( homeDomain)
        outputObj={"Error":"No API endpoint found. Try navigating to "+homeDomain+"/simulator for list of drone simulators." }
        return json.dumps(outputObj)

    def POST(self, user):
        logging.info( "#####################################################################")
        logging.info( "Method POST of catchAll")
        logging.info( "#####################################################################")
        applyHeadders()
        outputObj={"Error":"No API endpoint found. Try navigating to "+homeDomain+"/simulator for list of drone simulators." }
        return json.dumps(outputObj)


urls = (
    '/', 'index',
    '/simulator/(.*)/action', 'action',
    '/simulator', 'simulatorIndex',
    '/simulator/(.*)/(.*)', 'simulatorStatus',
    '/(.*)', 'catchAll'
)

defaultHomeDomain='http://192.168.1.67:1235'
homeDomain = os.getenv('HOME_DOMAIN', defaultHomeDomain)
logging.debug( "Home Domain:"  + homeDomain)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()






