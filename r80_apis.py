#!/bin/python

import requests
import json
import pprint


#remove https warning
requests.packages.urllib3.disable_warnings()


def login(url,user,pw):

    payload_list={}
    payload_list['user']=user
    payload_list['password']=pw
    headers = {
        'content-type': "application/json",
        'Accept': "*/*",
    }
    response = requests.post(url+"login", json=payload_list, headers=headers, verify=False)
    return response    



def add_host(sid,url,name,ip_address,comments,groups,nat_settings):
        payload_list={}
        payload_list['name']=name
        payload_list['ipv4-address']= ip_address
        if nat_settings != "":
            payload_list['nat-settings']=nat_settings         
        if groups != "" :
            payload_list['groups']= groups 
        if comments != "":
            payload_list['comments']= comments 
    
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
             #print payload_list
        response = requests.post(url+"add-host", json=payload_list, headers=headers, verify=False)
        return response.json()

def delete_host(sid,url,name):
        payload_list={}
        payload_list['name']=name
        payload_list['ignore-warnings']="true"
        
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-host", json=payload_list, headers=headers, verify=False)
        return response

def add_network(sid,url,name,subnet,mask_length):
        payload_list={}
        payload_list['name']=name
        payload_list['subnet']= subnet 
        payload_list['mask-length']=mask_length
   
        
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
         
      
        response = requests.post(url+"add-network", json=payload_list, headers=headers, verify=False)
        
        return response.json()

def add_appsite(sid,url,name,url_list):
        payload_list={}
        payload_list['name']=name
        payload_list['url-list']=url_list
        payload_list['urls-defined-as-regular-expression']=True
        payload_list['primary-category']="Custom_Application_Site"
   
        
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
         
      
        response = requests.post(url+"add-application-site", json=payload_list, headers=headers, verify=False)
        
        return response.json() 

def update_appsite(sid,url,name,url_list):
        payload_list={}
        payload_list['name']=name
        payload_list['url-list']=url_list
        payload_list['urls-defined-as-regular-expression']=True
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
         
      
        response = requests.post(url+"set-application-site", json=payload_list, headers=headers, verify=False)
        
        return response.json() 
        
def delete_network(sid,url,name):
        payload_list={}
        payload_list['name']=name

        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-network", json=payload_list, headers=headers, verify=False)
        return response


def show_network_groups(sid,url):
    payload_list={}
    payload_list['details-level']="standard"
    headers = {
            'content-type': "application/json",
            'Accept': "*/*",
        'x-chkp-sid': sid,
    }    
    response = requests.post(url+"show-groups", json=payload_list, headers=headers, verify=False)
    groups=json.loads(response.text)
    return groups

def add_network_group(sid,url,name):
        payload_list={}
        payload_list['name']=name
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-group", json=payload_list, headers=headers, verify=False)
        return response.json()

def add_members_to_network_group(sid,url,name,members):
        payload_list={}
        payload_list['name']=name
        payload_list['members']=members
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"set-group", json=payload_list, headers=headers, verify=False)
        return response.json()

def add_access_layer(sid,url,name):
        payload_list={}
        payload_list['name']=name
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-access-layer", json=payload_list, headers=headers, verify=False)    
        return response



def add_policy_package(sid,url,name,access_layer,threat_layer,comments):
        payload_list={}
        payload_list['name']=name
        payload_list['access']=access_layer
        payload_list['threat-prevention']=threat_layer
        payload_list['comments']=comments
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-package", json=payload_list, headers=headers, verify=False)
        return response

def add_access_section(sid,url,layer,position,name):
        payload_list={}
        payload_list['layer']=layer
        payload_list['position']=position
        payload_list['name']=name
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-access-section", json=payload_list, headers=headers, verify=False)
        return response.json()

def delete_access_section_by_name(sid,url,layer,name):
        payload_list={}
        payload_list['name']=name
        payload_list['layer']=layer
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-access-section", json=payload_list, headers=headers, verify=False)
        return response

def show_access_section(sid,url,layer,name):
        payload_list={}
        payload_list['layer']=layer
        payload_list['name']=name
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"show-access-section", json=payload_list, headers=headers, verify=False)
        return response
    
def add_access_rule(sid,url,layer,rule):
        payload_list={}
        payload_list['layer']=layer
        payload_list['position']=rule['position']
        payload_list['name']=rule['name'] 
        payload_list['source']=rule['source']
        payload_list['destination']=rule['destination']
        payload_list['service']=rule['service']
        payload_list['track']= 'Log' #track={'per-connection':True, 'accounting':False,}
        payload_list['action']=rule['action']
        headers = {
                'content-type': "application/json",
                'Accept': "*/*",
                'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-access-rule", json=payload_list, headers=headers, verify=False)
        return response.json()

def delete_access_rule_by_rule_number(sid,url,layer,number):
        payload_list={}
        payload_list['layer']=layer
        payload_list['rule-number']=number
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-access-rule", json=payload_list, headers=headers, verify=False)
        return response

def delete_access_rule_by_rule_name(sid,url,layer,name):
        payload_list={}
        payload_list['layer']=layer
        payload_list['name']=name
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-access-rule", json=payload_list, headers=headers, verify=False)
        return response
    

def publish(sid,url):
        payload_list={}
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"publish", json=payload_list, headers=headers, verify=False)
        return response

def add_range(sid,url,name,ip_address_first,ip_address_last,comments=""):
        payload_list={}
        payload_list['name']=name
        payload_list['ip-address-first']=ip_address_first
        payload_list['ip-address-last']= ip_address_last      
        payload_list['comments']= comments    
        
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"add-address-range", json=payload_list, headers=headers, verify=False)
        return response.json()
       
def delete_range(sid,url,name):
        payload_list={}
        payload_list['name']=name

        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"delete-address-range", json=payload_list, headers=headers, verify=False)
        return response

def show_task(sid,url,task):
        payload_list={}
        payload_list['task-id']=task
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"show-task", json=payload_list, headers=headers, verify=False)
        return response

def logout(sid,url):
        payload_list={}
        headers = {
            'content-type': "application/json",
            'Accept': "*/*",
            'x-chkp-sid': sid,
        }
        response = requests.post(url+"logout", json=payload_list, headers=headers, verify=False)
        return response


