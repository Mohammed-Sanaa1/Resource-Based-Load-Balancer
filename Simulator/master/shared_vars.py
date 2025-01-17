#master.shared_vars

#variables that are shared between all packages are stored here
#import as "import master.shared_vars" to maintain state across your files

#!!!
#PLEASE ensure race condition handling! otherwise we might brick the simulation
#!!!

#variable used to count the number of active threads. Useful for the parent/main if it has no prior knowledge of threads (ex. threads of a grandchild)
threads_remaining = 0

#helper function. Self-explanatory. Prevents code congestion
def wait_for_all_threads():
    global threads_remaining
    while threads_remaining > 0:
        pass
    return