from base_client import WithQuiene
from time import sleep


def wait_answer(quiene):
    while True:
        if quiene.is_empty():
            return
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
        for i in range(30):
            quiene.put(i)
        
        wait_answer(quiene) 


if __name__ == "__main__":
    write_proccesor()