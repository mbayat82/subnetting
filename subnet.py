import ipaddress
from rich import print
from rich.tree import Tree
from rich.console import Console
import networks
from operator import itemgetter

# sort network from largest to smallest
networks_sorted =  sorted(networks.NETWORKS, key=itemgetter('subnet'))

all_networks =[ipaddress.IPv4Network(networks.SUPERNET)]
prefix_list = []
for network in networks_sorted:
    
    if len(all_networks) == 0:
        print('Ran out of prefixes while subnetting. Concider a bigger supernet')
        exit()
    
    elif network['subnet'] == all_networks[0].prefixlen:
        temp_network = format(all_networks.pop(0))
    else:
        last_network = list(all_networks[0].subnets(new_prefix=network['subnet']))
        all_networks.pop(0)
        all_networks = last_network + all_networks
        temp_network = format(all_networks.pop(0))
    
    prefix_dict = {
        'prefix': temp_network,
        'description': network['description']
    }
    prefix_list.append(prefix_dict)

# Printing Prefixes
console = Console(record=True, width=100)
tree = Tree(f"\n[bold blue]{networks.SUPERNET}[/]")
for prefix in prefix_list:
    subnet_tree = tree.add(f"[yellow]{prefix['prefix']}[/] - {prefix['description']}")
console.print(tree)
print("\n")