import re
import requests
import time
import json
import urllib
import string
from subprocess import check_call,CalledProcessError      
import hashlib
from subprocess import DEVNULL, STDOUT, check_call

import random
import os
import subprocess
import time
import re
import ntpath
from multiprocessing.managers import BaseManager
import time
import multiprocessing
import signal
# from JAW.analyses.fingerprinting import find_invocation
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
datapath="/storage/miniapp/wechat/packages/"
targetdir="./output/"

 

class detectedresult:
    appid=""
    path=""
    name=""
    
    similarityhit=False
    def __init__(self,appid,path):
        self.appid=appid
        self.path=path  
        self.similarityhit=False
    
    def getresult(self):
        return json.dumps(self.__dict__)
        # return "{}, name={}, path={}, hiddenapis={}, boxgame={}, locationbypass={}, suanming={}, bypass={}, shareabuse={}, fakeapp={}, fakechat={}, redpocket={}, timebased={}, collusion={}, eval5={}, vm={}, hotupdate={}, pyramidselling={}, locids={}, userinfo={}, crossinfo={}, apis={}".format(self.appid, self.name, self.path, self.hiddenapis, self.boxgame, self.locationbypass, self.suanming, self.bypass, self.shareabuse, self.fakeapp, self.fakechat, self.redpocket, self.timebased, self.collusion, self.eval5, self.vm, self.hotupdate, self.pyramidselling, self.locids, self.userinfo, self.crossinfo, self.apis)

publicapis=[]
 

# def loadnameDB():
#     global names
#     namefile=open("names.csv","r")
#     for line in namefile:
#         line=line.strip()
#         objs=line.split()
#         names[objs[0]]=objs[2]
#     print("NameDB loaded:", len(names))
 
def get_first_page(path):
    jsonfile=open(path+"/app.json","r")
    print(jsonfile)
    index=0
    fp=""
    try:
      for l in jsonfile:
        index=index+1
        if(index<3):
            continue
        print(l)
        fp=l.strip().split('"')[1]+".wxml"
 
        return fp
    except:
        print('get first page error')
        pass
    return "None"

 



def loadpublicapis():
    # global publicapis
    # apis=open("publicAPIs.csv","r")
    # for api in apis:
    #     publicapis.append(api.strip())
        
    # appendlist=['wx.rprm', 'wx.storeId', 'wx.min', 'wx.vue', 'wx.bncxw','wx.qy', 'wx.getStyle', 'wx.length', 'wx.key', 'wx.test', 'wx.getSavedFileInfo','wx.bncxw', 'wx.bjcxdf', 'wx.requestpayment', 'wx.createContext', 'wx.drawCanvas', 'wx.hloop']    
    # publicapis.extend(appendlist)
    # print("public API loaded:", len(publicapis))
    print("not loading public APIs")
  
def scan(appid,name, path):
    global publicapis
 
 
    res = detectedresult(appid,path)
    hashlists={}
    res.name=name
    pubapis=[]
    # firstpage = get_first_page(path)
 
    
    isapphit=False
    reportmatch=False  
    contentmatch=False
    subjectmatch=False
    evidencematch=False
    usematch=False
    descriptionmatch=False
    submitmatch=False
    selectmatch=False
    selectmatchlist=[]
    pages=[]
    choosetypematch=False
    for root, dirs, files in os.walk(path):
        # for file in files:
        
        for file in files:
                filehit=False
                if not (file.endswith(".js") or file.endswith(".wxml")  or file.endswith(".wxss") or file.endswith(".json")):
                    continue

                jsfile=open(os.path.join(root, file),'r')
                print(os.path.join(root, file))
                # exit()
                p=re.compile(r"wx\.[A-Za-z]+")
                
               
                
                
                lines=""
                lines= jsfile.read()
                    
   
                # fake report
                if '投诉' in lines:
                    reportmatch=True
                    isapphit=True
                    filehit=True
                if "投诉对象" in lines:
                    subjectmatch = True
                if "请输入投诉内容" in lines:
                    contentmatch = True
                if "证据截图" in lines:
                    evidencematch = True
                if "允许微信使用小程序当前页面的数据和截图作为投诉证据" in lines:
                    usematch=True
                if '相关说明' in lines:
                    descriptionmatch=True
                if '提交' in lines:
                    submitmatch=True
                selectkeywords=['欺诈','色情低俗','诱导','传播不实信息','违法犯罪','骚扰','侵权（诽谤、抄袭）','混淆他人投诉','恶意营销','与服务类目不符','隐私数据收集','其他']
                if '请选择投诉原因' in lines:
                    for i in range(0,len(selectkeywords)):
                        if selectkeywords[i] in lines:
                            selectmatchlist.append(i)
                

                
                
                digeststr=hashlib.md5(lines.encode()).hexdigest()
                # if reportmatch:
                if digeststr not in hashlists:
                    hashlists[digeststr]=[]
                res.similarityhit=True
                if filehit:
                    pages.append(os.path.join(root, file))
                # hashlists[digeststr].append({
                #     'path':os.path.join(root, file),
                #     'reportmatch':reportmatch,
                #     'contentmatch':contentmatch,
                #     'subjectmatch':subjectmatch,
                #     'evidencematch':evidencematch,
                #     'usematch':usematch,
                #     'descriptionmatch':descriptionmatch,
                #     'submitmatch':submitmatch,
                #     'selectmatch':selectmatch,
                #     'selectmatchlist':selectmatchlist,
                #     'choosetypematch':choosetypematch
                # })
                
                    
                    
    #WARNING: PATH IS NOT USEFUL
    resobj={
        # 'path':os.path.join(root, file),
        'appid':appid,
        'reportmatch':reportmatch,
        'contentmatch':contentmatch,
        'subjectmatch':subjectmatch,
        'evidencematch':evidencematch,
        'usematch':usematch,
        'descriptionmatch':descriptionmatch,
        'submitmatch':submitmatch,
        'selectmatch':selectmatch,
        'selectmatchlist':selectmatchlist,
        'choosetypematch':choosetypematch,
        'pages':pages
    }
    # resobj=json.loads(res.getresult())
    # resobj['reportmatch']=reportmatch
    # resobj['hashlists']=hashlists
    # resobj['appid']=appid
    resobj['isapphit']=isapphit
    resobj=json.dumps(resobj)
    # print("RESULT:",resobj)

    
    
    return resobj
 

def scan_keyword(appid,name, path):
    global publicapis
 
 
    priv_collect_api=['getLocation', 'getFuzzyLocation', 'getUserProfile', 'getUserInfo']
    non_priv_collection_api=['getWindowInfo', 'getSystemSetting', 'getSystemInfoSync', 'getSystemInfoAsync', 'getSystemInfo','getDeviceInfo', 'getAppBaseInfo', 'getAppAuthorizeSetting', 'getPerformance','getAvailableAudioSources', 'getSetting','getGroupEnterInfo', 'getPrivacySetting','getBluetoothDevices', 'getBeacons', 'getConnectedWifi','getBatteryInfoSync', 'getBatteryInfo', 'getClipboardData', 'getScreenBrightness']
    res={}


    for root, dirs, files in os.walk(path):
        for file in files:
                
                filehit=False
                if not (file.endswith(".js") or file.endswith(".wxml")  or file.endswith(".wxss") or file.endswith(".json")):
                    continue
                
                jsfile=open(os.path.join(root, file),'r')
                fullpath=os.path.join(root, file)
                pagepath=fullpath.split(appid+'/')[1]
                res[pagepath]={
                    'priv-apis':set(),
                    'non-priv-apis':set(),
                }
                text=jsfile.read()
                # print(text)
                
                # pagepath=fullpath.split()
                # exit()
                for API in priv_collect_api:

                    if API in text:
                        res[pagepath]['priv-apis'].add(API)
                for API in non_priv_collection_api:
                    if API in text:
                        res[pagepath]['non-priv-apis'].add(API)
                    
                

    
    print(res)
    return res
 
def check_gamejs(appid):
    apppath=datapath+'wx'+appid[2:4]+'/'+appid[4:6]+"/"+appid+'.wxapkg'
    process_strings = subprocess.Popen(
            ["strings", apppath],  # First command
            stdout=subprocess.PIPE,  # Pipe its output
            text=True  # Decode the output as text
        )

    process_grep = subprocess.Popen(
        ["grep", 'require("game.js")'],  # Second command
        stdin=process_strings.stdout,  # Take input from the previous process
        stdout=subprocess.PIPE,  # Capture output
        text=True  # Decode the output as text
    )
    # Ensure proper closing of pipes
    process_strings.stdout.close()

    # Get the final output
    output, _ = process_grep.communicate()

    # Print the matched lines
    if len(output)>0:
        return True
    else:
        return False

def analyze_mini_program(path):
    # apppath=datapath+'wx'+appid[2:4]+'/'+appid[4:6]+"/"+appid+'.wxapkg'
    
    process_analyze = subprocess.Popen(
            ["python3", "-m", "analyses.fingerprinting.find_invocation","--input="+path],  # First command
            stdout=subprocess.PIPE,  # Pipe its output
            text=True,  # Decode the output as text
            cwd="./JAW/"
        )

    
    print(' '.join(["python3", "-m", "analyses.fingerprinting.find_invocation","--input="+path]))
    

    # Get the final output
    output, _ = process_analyze.communicate()
    # Ensure proper closing of pipes
    process_analyze.stdout.close()
    print(output)
    return output

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def remove_miniapp(appid):
    # apppath=targetdir+appid
    # os.system("./clean.sh "+apppath)
    a=1
    os.system("./clean.sh "+appid)
    # print("SSSSSSREMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOVE!")
    # exit()


    
def scan_miniapp(appid):
    res={}
    is_gamejs=check_gamejs(appid)
    if not is_gamejs:
        res={
            "appid":appid,
            "type":'app',
            "error":None,
            'result':None
        }
        return res
    else:
        unpackstatus,msg=unpack_miniapp(appid)
        res={
            "appid":appid,
            "type":'game',
            "error":None,
            'result':None
        }
    
    if unpackstatus:
        print('unpacked!')
        analyze_res=analyze_mini_program('../output/'+appid)
        # try:
        res['result']=analyze_res
    else:
        res['error']=msg
    remove_miniapp(appid)
    if 'appid' not in res:
        res['appid']=appid
    
    
    # exit()
    return res


def unpack_miniapp(appid):
    apppath=datapath+'wx'+appid[2:4]+'/'+appid[4:6]+"/"+appid+'.wxapkg'
    targetpath=targetdir+appid
    print(apppath,targetpath)
    print("./decrypt.sh "+appid)
    try:
        with NamedTemporaryFile() as f:
            check_call(["./decrypt.sh", appid],stdout=f, stderr=STDOUT)
    except CalledProcessError as e:
       print('unpack error')
       print(e)
       return False,'unpackerror'
   
    return True,''



def run():
    print("Miniapp Scanner Slave")


    class QueueManager(BaseManager):
        pass

    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    server_addr = '127.0.0.1'
    print('Connect to server %s...' % server_addr)

    m = QueueManager(address=(server_addr, 8989), authkey=b'abc')
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()
    loadpublicapis()
 
    while True:
        try:
            scanstr = task.get(timeout=10)
            #print(res)
            start_time = time.time()
            appid=scanstr
            # name=scanstr[1]
 
            scanres = scan_miniapp(appid)
            end_time = time.time()
            
            # writeres(res.getresult())
            # print(res.getresult())
            # res['process_time']=int((end_time-start_time)/0.01)/100
            # res=json.dumps(res)
            # print((appid,json.dumps(respage),json.dumps(resurl)))
            # print((appid,scanres))
            print("SUCCESS",appid,scanres)
            result.put((appid,str(scanres)))
            # print(appid,res)
            # exit()    
        except BrokenPipeError:
            print("finished")
            break
        # except Exception as e:
        #     print('miniapp scan error')
        #     print(e)

        #     continue
        # exit()
run()
# scan_miniapp('wx4d6c35387959cd7d')