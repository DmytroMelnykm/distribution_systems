from base_client import WithQuiene
from threading import Thread
from time import sleep


def wait_answer(quiene):
    while True:
        if (read_in_quiene := quiene.poll()) is None:
            return
        print(f"Read element = {read_in_quiene}")
        sleep(5)
    


def write_proccesor():
    enter_param = {
        "list_nodes":[
            "192.168.240.2:5701", 
            "192.168.240.4:5701", 
            "192.168.240.5:5701"
            ], 
        "cluster_name":"dev",
        "name_quiene": "my_queue_first"
    }
    
    with WithQuiene(**enter_param) as quiene:
        wait_answer(quiene) 


if __name__ == "__main__":
    Thread(target=write_proccesor).start()
    Thread(target=write_proccesor).start()