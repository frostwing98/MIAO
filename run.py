import os
import multiprocessing as mp
import subprocess
import signal
import shutil
import tempfile
# from itertools import repeat


PREFIX = "/storage/miniapp/wechat/packages"
OUTPUT = "/home/evi0s/miniinput/results"


def unpack(wxid):
    print(f"[unpack] processing: {wxid}")
    miniapp_path = os.path.join(PREFIX, wxid[:4], wxid[4:6], wxid) + ".wxapkg"
    temp_dir = tempfile.TemporaryDirectory(dir="/dev/shm/miniapp/package")
    shutil.copy(miniapp_path, temp_dir.name)
    try:
        subprocess.run(["node",
                        "/home/evi0s/miniinput/wxunpacker/wuWxapkg.js",
                        os.path.join(temp_dir.name, f"{wxid}.wxapkg")],
                       timeout=600)
    except subprocess.TimeoutExpired:
        print("[unpack] timeout, kill the subprocess")
    return temp_dir


def analyze(wxid, temp_dir):
    print(f"[analyze] processing: {wxid} in {temp_dir.name}")
    try:
        subprocess.run(["python3",
                        "/home/evi0s/miniinput/TaintMini/main.py",
                        "-i", os.path.join(temp_dir.name, wxid),
                        "-o", OUTPUT,
                        "-j", "8"], timeout=600)
    except subprocess.TimeoutExpired:
        print("[analyze] timeout, kill the subprocess")
    temp_dir.cleanup()


def task(wxid, queue):
    try:
        temp_dir = unpack(wxid)
        analyze(wxid, temp_dir)
    except Exception as e:
        print(f"[task] error in handling {wxid}: {e}", open("taskerror.log", "a+"))
    queue.put({"wxid": wxid})


def progress_listener(checkpoint, queue):
    print("[progress listener] watching progress...")
    finished_miniapps = set()
    while True:
        message = queue.get()
        if message == "kill":
            print("[progress listener] kill received, saving progress...")
            open("checkpoint.list", "w").write("\n".join(list(checkpoint | finished_miniapps)))
            break
        if isinstance(message, dict):
            finished_miniapps.add(message["wxid"])


def main(workers, timeout):
    dataset_index = set(filter(None, open("index.list").read().split("\n")))
    checkpoint = set(filter(None, open("checkpoint.list").read().split("\n")))
    print(f"[main] {len(checkpoint)} have been processed, resuming")

    remains = dataset_index - checkpoint

    manager = mp.Manager()
    queue = manager.Queue()

    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = mp.Pool(workers + 1 if workers is not None else mp.cpu_count())
    signal.signal(signal.SIGINT, original_sigint_handler)

    pool.apply_async(progress_listener, (checkpoint, queue, ))

    workers = dict()

    try:
        # res = pool.starmap_async(task, zip(list(remains), repeat(queue)))
        # res.get(timeout if timeout is not None else 600)
        for wxid in list(remains):
            workers[wxid] = pool.apply_async(task, (wxid, queue, ))

        for wxid in workers:
            workers[wxid].get(timeout if timeout is not None else 600)

    except KeyboardInterrupt:
        print("[main] caught KeyboardInterrupt, saving checkpoint...")
        queue.put("kill")
        pool.terminate()
    except Exception as e:
        print(f"[main] error: {e}", file=open("err.log", "a+"))
    else:
        print("[main] normal termination")
        queue.put("kill")
        pool.close()
    pool.join()


if __name__ == "__main__":
    main(16, 600)
