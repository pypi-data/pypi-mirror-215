import threading
import time

jobs = []
verbose = False

def initialize(ver):
    global verbose
    verbose = ver

def addJob(function, timeout, args = None):
    global verbose
    """
    Adds job to the cron list
    :param func function: Function to call
    :param int timeout: Call after every x seconds
    """
    jobs.append([function, timeout, args])
    if(verbose):
        print("Cron Job [ {0}('{1}') ] Registered [Running Every {2}s]".format(function.__name__, args, timeout))

def start(doThread = False):
    """
    Start the cron job counter
    This is a thread blocking function
    :param bool doThread: Should the cron counter run in a thread? Default: False
    """
    if doThread:
        thread = threading.Thread(target = start)
        thread.start()
    else:
        seconds = 1
        while 1:

            for job in jobs:
                if seconds % job[1] == 0:
                    if job[2] == None:
                        job[0]()
                    else:
                        job[0](job[2])

            time.sleep(1)
            seconds += 1
