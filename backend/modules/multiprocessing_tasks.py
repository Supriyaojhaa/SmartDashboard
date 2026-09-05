from multiprocessing import Process

def run_process(task, data):

    process = Process(target=task, args=(data,))
    process.start()
    process.join()

def sample_task(data):
    print(f"[MULTIPROCESSING] Processing chunk of size: {len(data)}")