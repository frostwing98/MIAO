from minimalware import miniassigner as ma
import pandas as pd
import json

def post_process(alldata):
    # print(alldata)
    # if alldata['isapphit']:
    #     return alldata
    # else:
    #     return {}
    return alldata

result_file_path="scannedoverallres.csv"
scanned_appid_path="scannedallminiapps.csv"


appidlist=[]
# allminiappfile=open(all_package_path_list,'r')
# with open('template_id.csv','r') as f:
#     for line in f:
#         appidlist.append(line.split(",")[0])
readcnt=0

# with open('/storage/miniapp/wechat/index.list','r') as f:
# with open('allevasivevettingids_new.csv') as f:
# with open('takendown.csv') as f:
with open('/storage/miniapp//wechat/index.list') as f:
    for line in f:
        # appid=line.split('/')[-1].split('.')[0]
        # appid=line.replace('\n','')
        appid = line.strip().split('/')[-1].split('.')[0]
#        print("!!!",appid)
        appidlist.append(appid)
        readcnt+=1
        if readcnt%10000 ==0:
            print(readcnt)
        # if readcnt==36000:
        #     break
#        if readcnt==10:
#            break
        # print(appid)
        # break
# with open('../data/1-hit-anyone.csv') as f:
#     for lin in f:
#         data=json.loads(lin)
#         appidlist.append(data['appid'])
print(len(appidlist))

flag=False
# appidlist=[]
cnt=0

# for appid in templatelist:
#     print(cnt,4585587)
#     cnt+=1
#     appid=line.split('/')[7][:-1].split('.wxapkg')[0]
#     if appid in templatelist:

#         appidlist.append(appid)
        

ma.main(appidlist, result_file_path, scanned_appid_path, post_process)


# def writeres(res):
#     f=open(scanned_appid_path,"a")
#     f.write(json.dumps(res)+"\r\n")
# index = 0
# def loadscanned():
#     res=set()
#     finalres=open(scanned_appid_path,"r")
#     lastone=''
#     for l in finalres:
#         appid=json.loads(l)['appid']
#         res.add(appid)
#         lastone=json.loads(l)['appid']
#         # if not name in res:
#         #     res.add(name.strip())
        
#     print("scanned",len(res))
#     return res,lastone
# def loadTemplateMiniapps():
#     # fr=open("template_id.csv")
#     # data=pd.read_csv("template_id.csv",index_col=1, skiprows=1).T.to_dict()
#     #wxid,template_id
#     # allids=pd.DataFrame(['wx65e149bfea342554','wxdeadbeefdeadbeef'],columns =['wxid'])
#     # print(data['wx65e149bfea342554'])
#     # print(df.loc[df['wxid'] == allids['wxid']])
#         #     
#     df=pd.read_csv('template_id.csv')
#     return list(df['wxid']), df


# if __name__ == '__main__':
#     task_queue = queue.Queue()
#     result_queue = queue.Queue()

#     class QueueManager(BaseManager):
#         pass

#     QueueManager.register('get_task_queue', callable=lambda: task_queue)
#     QueueManager.register('get_result_queue', callable=lambda: result_queue)
#     manager = QueueManager(address=('', 8989), authkey=b'abc')
#     manager.start()
#     task = manager.get_task_queue()
#     result = manager.get_result_queue()
#     print("App analyzer Master is running")
#     scanned=set()
    
#     scanned,lastone=loadscanned()
    

    
#     templatelist,df=loadTemplateMiniapps()
    
#     file=open(all_package_path_list,'r')
#     count = 0
#     total=0
#     scancnt=0
#     flag=False
#     for line in file:
#         # if '_1' in line:
#         #     continue
#         # print(line.split('/')[7][:-1].split('.wxapkg')[0])
#         appid=line.split('/')[7][:-1].split('.wxapkg')[0]
        
#         # print("loading...(scanned) {} ".format(scancnt))
        
#         # if appid==lastone:
#         #     flag=True
        
#         if flag and appid not in scanned and appid in templatelist:
#             scancnt+=1
#             print("loading... {} ".format(total),  end="\r", flush=True)
#             task.put(appid)
#             total+=1
            
#     print('hmm',total)
#     while(count < total):
#         alldata = result.get(timeout=20000)
#         alldata=json.loads(alldata)
#         print(alldata)
        
        
        
#         count += 1;
#         # print("loading... {} ".format(total),  end="\r", flush=True)

#         print("{}/{}: {}".format(count, total, alldata['appid']),  end="\r", flush=True)
#         print(alldata)
#         output=open(result_file_path, "a")
#         if alldata['similarityhit']:
#             print("FOUND!")
#             output.write("{}/{}: {}".format(count, total, alldata['appid'])+"\r\n")
#             output.close()
#             writeres(alldata)
        

#     manager.shutdown()

