from threading import Thread

from base_client import ClientOperator



def back_loop_infinite(map_dist) -> int:
    counter = 0
    while True:
        if (same_value := map_dist.get('key')) >= 4000:
            return counter
        if map_dist.replace_if_same('key', same_value, same_value + 1):
            counter += 1
            


def work_proccesor(number_process):
    enter_param = {
        "list_nodes":[
            "192.168.176.2:5701", 
            "192.168.176.4:5701", 
            "192.168.176.5:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "Six task Optimize"
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