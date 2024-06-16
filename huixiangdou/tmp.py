from multiprocessing import Process, Value
import time

def worker(num):
    """线程的工作函数"""
    print(f"Worker {num} starts")


if __name__ == '__main__':
    processes = []

    for i in range(5):
        p =  Process(target=worker, args=(i,))
        p.daemon = True  # 设置为守护进程
        processes.append(p)
        p.start()


    print("time sleep")
    time.sleep(10)