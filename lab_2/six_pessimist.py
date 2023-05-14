from threading import Thread

from base_client import ClientOperator



def back_loop_infinite(map_dist) -> int:
    for key in range(4000):
        map_dist.lock("key")
        get_value = map_dist.get("key")
        map_dist.set("key", get_value + 1)
        map_dist.unlock('key')
    else:
        print(f"Finnal = {key}")            


def work_proccesor(number_process):
    enter_param = {
        "list_nodes":[
            "192.168.176.2:5701", 
            "192.168.176.4:5701", 
            "192.168.176.5:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "Six task pessimist"
    }
    
    with ClientOperator(**enter_param) as map_dist:
        print(
            "Counter = {} Proccess number = {}".format(
                back_loop_infinite(map_dist),
                number_process
                )           
            )


if __name__ == "__main__":
    Thread(target=work_proccesor, args=(1,)).start()
    Thread(target=work_proccesor, args=(2,)).start()
    Thread(target=work_proccesor, args=(3,)).start()