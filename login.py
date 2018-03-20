#!/usr/bin/python3

import requests
import subprocess
import sys
import os
import csv

global list_dir 

##############  Login ####################
c = requests.Session()
#p = c.get('https://gslab.kpoint.com/user/login')
p = c.get('https://gslab.kpoint.com/user/login#')
from_id = p.text
for line in from_id.splitlines():
	if 'form_build_id' in line :
		form = line
abc  = form.split()[3]
form1=abc.replace('id=','')
id_form = form1.replace('"','')
#c.post('http://test.kpoint.com/user/login',data={'kpointemail':'siteadmin', 'pass':'kPoint@123','name':' ','form_build_id':id_form,'form_id':'user_login','op':'Sign in'})
try:
	c.post('https://gslab.kpoint.com/user/login#',data={'kpointuserid':'USER_NAME', 'pass':'PASS','name':' ','form_build_id':id_form,'form_id':'user_login','op':'Sign in'})
except Exception as e:
	print("Unexpected error:", e)


##############        #############
def teleport(li,id1):
	for i in li :
		if i != "teleport-bundle.properties" :
			file1 = open(list_dir+"/"+gcc[0]+"/"+i,'rb')
			kp_size=subprocess.getoutput("du "+list_dir+"/"+gcc[0]+"/"+ i).split("\t")[0]
			print ("Uploading kap file : %s    Size : %s " %(i,kp_size))
			try :
				kap=c.post("https://gslab.kpoint.com/doc/uploadteleport",files={'qqfile':file1}, data={'teleportid':id1,'qqqtotalfilesize':kp_size,'qqquuid':'bb05c024-7c0d-434d-a804-226dda0323d6'})
			except Exception as e:
                                print ("Error : ", e)
			file1.close()


########  Unzip And teleport File ###############
def extract(gconfid, date, user, user_id):
	#zip1 = "/tmp/" + gconfid
	zip1 = gconfid
	cmd = 'unzip', zip1, '-d','/tmp/'+ zip1.split("-")[1]
	subprocess.call(cmd, stdout=subprocess.PIPE)
	#subprocess.call(cmd)
	global list_dir 
	list_dir = "/tmp/"+ zip1.split("-")[1]
	global gcc 
	gcc = os.listdir(list_dir)
	global li
	li = os.listdir( list_dir + "/" + gcc[0])
	print ("li : ", li)
	for i in li :
		if i == "teleport-bundle.properties" :
			file = open(list_dir+"/"+gcc[0]+"/"+i,'rb')
			print ("*** Uploding Properties File ***")
			try:
				p=c.post("https://gslab.kpoint.com/upload_teleport",files={'file_upload':file}, data={'invitee_dn':user,'invitee':user_id, 'startdate':date, 'op':'Start Teleport'})
			except Exception as e:
				print ("Error : ", e)	
				
			print ("Status Uploading : ", p)
			id = p.text
			for line in id.splitlines():
				if "teleportid" in line:
					t_ip=line
			temp=t_ip.split()[1]
			global id1
			id1=temp.replace('"','')
			file.close()	
	teleport(li,id1)


############### Read CSV Containt ###########

def un(gconfid):
	zip1 = gconfid
	cmd = 'unzip', zip1, '-d','/tmp/'+ zip1.split("-")[1]
	print(cmd)
	subprocess.call(cmd, stdout=subprocess.PIPE)


def read():
	try:
		f_name = sys.argv[1]	
		print (f_name)
		open_file = open(f_name)
		csv_file = csv.reader(open_file, delimiter=",")
		count =  1
		for i in csv_file:
			gconfid = i[0]
			date = i[1]
			user = i[2]
			user_id = i[3]
			print ("----------------- %d Teleport Started  ---------------------" %(count))
			count =  count + 1
			print ("Name = ", gconfid)
			extract(gconfid, date, user, user_id)
			remove = ['rm','-rf','/tmp/'+ gconfid.split("-")[1]]
			subprocess.call(remove, stdout=subprocess.PIPE)
			print ("Removed file %s" %(remove))
			print ("------------------------------  END  ------------------------------------")
	except Exception as e:
		print("Unexpected error:", e)

read()
