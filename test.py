import threading
import time
from queue import Empty, Queue
from intake.catalog.local import YAMLFilesCatalog


def worker(queue):
    try:
        catalog = YAMLFilesCatalog("/tmp/sscce/catalogs/*.yml")
        catalog["source1"]
    except Exception as exc:
        queue.put(exc)


def test():
    queue = Queue()
    worker1 = threading.Thread(target=worker, args=(queue,))
    worker2 = threading.Thread(target=worker, args=(queue,))
    worker1.start()
    time.sleep(1)
    worker2.start()
    worker1.join()
    worker2.join()
    try:
        exc = queue.get_nowait()
    except Empty:
        print("success")
    else:
        raise exc


if __name__ == "__main__":
    test()
