from base_client import ClientOperator


if __name__ == "__main__":
    enter_param = {
        "list_nodes":[
            "192.168.176.2:5701", 
            "192.168.176.4:5701", 
            "192.168.176.5:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "Three task"
    }
    
    with ClientOperator(**enter_param) as map_dist:
        for key in range(0, 1001):
            value = ClientOperator.send_data(map_dist=map_dist, key=key)
            print(f"key = {key}, value = {value}")
    