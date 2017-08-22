#!/bin/python

import csv
import r80_apis
import json
import ConfigParser
import time
import re
import socket


#help method since in add_objects method is not handled adding objects into groups, in forst iteration is created just group and in second are added members
def add_members_togroup(sid,url):
     with open('hosts') as csvfile:
        reader=csv.DictReader(csvfile)
        members =[]# pomocny list pro API
        for row in reader:
            group_name = row['name']# jmeno grupy ktera se bude modifikovat
            if '|' in row['members']: # pokud najdes | v hodnote
                members=row['members'].split('|') # pridej nezavile objekty oddelene pomoci | do pomocneho listu members
                dic_temp={}# pomocny slovnik pro API
                for item in members: # projdi objekty na pridani
                    dic_temp['add'] = item # pridej kay, value hodnoty do slovniku
                    group=r80_apis.add_members_to_network_group(sid,url,group_name,dic_temp) # udelej update grupy
                    print group             
                
          #object method for adding objects from csv  
def add_objects(sid,url):
     with open('hosts') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:        
            
                if row['table'] == "ipaddr":
                 name=row['name'] 
                 ip_add=row['ipaddr']
                 description=row['description']
                 host=r80_apis.add_host(sid,url,name,ip_add,description,nat_settings="",groups="")
                 print host
                 
                 
                #handling network object 
                if row['table'] == "subnet":
                  name=row['name']
                  subnet=row['subnet']
                  mask=row['bits']
                  mask=int(mask)
                  description=row['description']
                  network=r80_apis.add_network(sid,url,name,subnet,mask)
                  print network
                    
                # handlinh ip range
                if row['table'] == "iprange":
                    name=row['name']
                    ip_address_first=row['begin']
                    ip_address_last=row['end']
                    description=row['description']
                    range=r80_apis.add_range(sid,url,name,ip_address_first,ip_address_last,description)
                    print range
                    
                # handling net group
                if row['table'] == "netgroup":
                    name= row['name']
                    group=r80_apis.add_network_group(sid,url,name)
                    print group
                #handlin app_site
                    
                if row['table'] == "host":
                    name=row['name']
                    url_list=row['host'] 
                    host=r80_apis.add_appsite(sid,url,name,url_list)
                    print host
                    
        

def add_rules(sid, url):
        layer="Network"
        with open('rules') as csvfile:
                reader=csv.DictReader(csvfile)
                position = 1
                for row in reader:
                        rule ={}  # dictionary with parameters
                        rule2 ={} # second dictionary for second rule
                        
                        list_service_temp=[] # temp list for storing services
                        list_destination_temp=[]
                        if '|' in row['source']: # if there is ; in string, split thiso
                            rule['source']=row['source'].split('|')
                            rule2['source']=row['source'].split('|') # add into rule, key source, values are items in list
                        else:
                            rule['source']=row['source']
                            rule2['source']=row['source'] # or add just one source
                        #service
                        if '|' in row['service']: # same as source
                            rule['service']=row['service'].split('|')
                            rule2['service']=row['service'].split('|') #same as source
                        else:
                            list_service_temp.append(row['service']) # one item services need to be added as list to be able add more items in the future
                            #rule['service']=list_service_temp
                            rule['service']=row['service']
                            rule2['service']=list_service_temp
                        #destination
                        if '|' in row['destination']: # same as source
                            help ={} # help dict for checking app sites in destination since forcepoint has hosts aka app sites in destination defone but checkpoint has it in service
                            help['destination']=row['destination'].split('|') # add items to help list to ceck app sites
                            for item in help['destination']: # check items
                                     if re.search(r"host:(.+).", item): # if item starts by host: it means it is app site object
                                       a=item.replace('host:','')# remove substrint host:
                                       list_service_temp.append(a)
                                       rule2['service']=list_service_temp
                                       rule2['destination']='any'
                                       rule2['action']=row['action']
                                       rule2['track']=row['track']
                                       rule2['name']=row['name']
                                       rule2['position']=position
                                       position = position+1
                                       rule_response=r80_apis.add_access_rule(sid,url,layer,rule2)
                                       print rule_response
                                     else:
                                         list_destination_temp.append(item)
                                         rule['destination']=list_destination_temp # if there is no host, add items             
                        else:
                            rule['destination']=row['destination']
                            rule2['destination']=row['destination']
                            #other field    
                        rule['action']=row['action']
                        rule['track']=row['track']
                        rule['name']=row['name']
                        rule['position']=position
                        position = position+1
                        rule_response=r80_apis.add_access_rule(sid,url,layer,rule)
                        print rule_response
                                              
def main():
    
    # config credentials
    config = ConfigParser.ConfigParser()
    config.read('cp.ini') #read from cp.ini file
    url=config.get('config','url',0)
    print url
    user=config.get('config','user',0)
    pw=config.get('config','password',0)
    
    
    #################
    #login to CP API
    #################
    sid_return=r80_apis.login(url,user,pw)
    print "status code"
    print sid_return.status_code
    if sid_return.status_code == 200:
            print "this"
            sid_text=json.loads(sid_return.text)
            sid = sid_text['sid']
            print "========="
            print "sid"
            print sid
            print "========="
    else:
            print "else"
            print json.loads(sid_return.text)
            exit

        
        
    # add objects only, no NAT no group members etc. will be done in next iteration
    
    # UNCOMENT THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    add_objects(sid, url)        
    add_members_togroup(sid,url)
    add_rules(sid,url)
    
    #update_appsites(sid,url)
    
 
    
     ################
    #publish
    ################
    publish=r80_apis.publish(sid,url)
    #print json.loads(publish.text)
    print "####"
    
    publish_text=json.loads(publish.text)
    show_task=r80_apis.show_task(sid,url,publish_text['task-id'])
    print json.loads(show_task.text)
    
    
    
    
    #####################
    # wait for publish to finish
    #u'tasks': [{u'task-id': u'01234567-89ab-cdef-a197-071c6ce706e3', u'task-name': u'Publish operation', u'status': u'in progress', u'progress-percentage': 0, u'suppressed': False}]}
    #####################
    
    
    show_task_text=json.loads(show_task.text)
    while show_task_text['tasks'][0]['status'] == "in progress":
        print " publish status = ", show_task_text['tasks'][0]['progress-percentage']
        time.sleep(3)
        show_task=r80_apis.show_task(sid,url,publish_text['task-id'])
        show_task_text=json.loads(show_task.text)
    print " publish status = ", show_task_text['tasks'][0]['progress-percentage'] , show_task_text['tasks'][0]['status']
    
    
    ################
    #logout
    ################
    logout=r80_apis.logout(sid,url)
    
    
if __name__ == "__main__":
    main()