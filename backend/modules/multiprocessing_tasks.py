from multiprocessing import Process

def run_process(task, data):
    try:
        process = Process(target=task, args=(data,))
        process.start()
        process.join()
    except Exception as e:
        print(f"[MULTIPROCESSING] Serverless fallback: {e}")
        task(data)

def sample_task(data):
    print(f"[MULTIPROCESSING] Processing chunk of size: {len(data)}")