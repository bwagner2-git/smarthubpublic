import psutil
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        #print(proc)
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
            if processName.lower() in pinfo['name']:
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
            pass
    return listOfProcessObjects

def filterMinecraft():
    hello = findProcessIdByName('java')
    pids = []
    for util in hello:
        pid = util['pid']
        if 'minecraft' in psutil.Process(pid).cmdline()[2]:
            pids.append(pid)
    return(pids)

