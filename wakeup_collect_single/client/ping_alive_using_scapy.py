from scapy.all import *
from random import randint
import time
import ipaddress

import threading
lock = threading.Lock()

def ping_once(host):
    ip_id = randint(1,65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet = IP(dst=host, ttl=64, id=ip_id)/ICMP(id=icmp_id, seq=icmp_seq)/b'rootkit'
    ping = sr1(packet, timeout=2, verbose=False)
    if ping:
        print("ping {} ok".format(host))
        # sys.exit(3)
        return True
    return False


def ping_scan_sequnce(network):
    net = ipaddress.ip_network(network)
    ip_processes = {}
    ip_list = []
    for ip in net:
        ip_addr = str(ip)
        if ping_once(ip_addr):
            ip_list.append(ip_addr)
    return sorted(ip_list)

g_addr_done = []
g_addr_todo = []
g_addr_ok = []
THREAD_NUM = 75

def ping_once_thread():
    # global g_addr_done, g_addr_todo, g_addr_ok
    for ip in g_addr_todo:
        if len(g_addr_todo) == len(g_addr_done):
            # print('scan finish')
            return # 这个说明已经扫描完了。
        if not ip in g_addr_done:
            #不要移除，
            #g_addr_todo.remove(ip)
            with lock:
                g_addr_done.append(ip)
                host = ip
            # print("ready to ping {}".format(host))

            ip_id = randint(1,65535)
            icmp_id = randint(1, 65535)
            icmp_seq = randint(1, 65535)
            packet = IP(dst=host, ttl=64, id=ip_id)/ICMP(id=icmp_id, seq=icmp_seq)/b'rootkit'
            ping = sr1(packet, timeout=2, verbose=False)
            if ping:
                print("ping {} ok".format(host))
                with lock:
                    g_addr_ok.append(host)
                # sys.exit(3)

def ping_scan_thread(network):
    # global g_addr_done, g_addr_todo, g_addr_ok
    net = ipaddress.ip_network(network)
    for ip in net:
        g_addr_todo.append(str(ip))
    threads = []
    for i in range(THREAD_NUM):
        t = threading.Thread(target=ping_once_thread)
        threads.append(t)
        t.start()
    for i in range(THREAD_NUM):
        threads[i].join()
    return g_addr_ok




ping_scan = ping_scan_thread

if __name__ == '__main__':
    t1 = time.time()
    #active_ip = ping_scan(sys.argv[1])
    active_ip = ping_scan("192.168.56.0/24")
    for ip in active_ip:
        print(ip)
    t2 = time.time()
    print("use time:{}".format(t2-t1))
