from threading import Thread

def run_threading(task, data):

    thread = Thread(target=task, args=(data,))
    thread.start()
    thread.join()