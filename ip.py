import ipaddress
from rich import print
from rich.table import Table
from rich import box
from rich.console import Console
from rich.tree import Tree
import argparse


def main():
    args = parse_args()
    console = Console()

    if not "/" in args.ip:
        print("Wrong format")

    network = extract_network(args.ip)
    mask = network.prefixlen
    num_addresses = network.num_addresses
    if mask == 31:
        hosts = list(network.hosts())
        first_host = hosts[0]
        last_host = hosts[-1]
        host_count = 2
    elif mask == 32:
        first_host = list(network.hosts())[0]
        last_host = list(network.hosts())[0]
        host_count = 1
    else:
        first_host = network.network_address+1
        last_host = network.network_address+num_addresses-1
        host_count = num_addresses-2
    
    table = Table(show_header=True, box=box.SIMPLE_HEAD, header_style="bold magenta")
    table.add_column("Network")
    table.add_column("Netmask")
    table.add_column("Start Range")
    table.add_column("End Range")
    table.add_column("Hosts")

    table.add_row(
        format(network.network_address),
        format(network.netmask),
        format(first_host),
        format(last_host),
        str(f'{host_count:,}'),
    )

    console.print(table)

    if args.detail or args.subnet:
        inside_subnets(network, args)


def parse_args():

    parser = argparse.ArgumentParser(description="CLI args for IP calculator")

    parser.add_argument("ip", type=str)

    parser.add_argument(
        "-d",
        "--details",
        dest="detail",
        help="print network details",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-s",
        "--subnet",
        dest="subnet",
        help="print network extesive",
    )

    args = parser.parse_args()
    return args


def extract_network(ip):
    try:
        network = ipaddress.ip_network(ip, strict=False)
        return network
    except ValueError:
        print("IP not valid")
        exit()


def inside_subnets(network, args):
    mask = network.prefixlen
    subnets = ""

    console = Console()
    table = Table(show_header=True, box=box.SIMPLE_HEAD, header_style="bold magenta")
    table.add_column("#")
    table.add_column("CIDR")

    for i in range(mask + 1, mask + 8):

        temp_subnets = list(network.subnets(new_prefix=i))
        num = len(temp_subnets)

        table.add_row(
            str(num),
            str(f"/{i}"),
        )

        if args.subnet and (str(i) == args.subnet) or ('/'+str(i) == args.subnet):
            subnets = temp_subnets

    console.print(table)

    if args.subnet:
        tree = Tree(format(network), guide_style="magenta")
        for sub in subnets:
            tree.add(format(sub))
        console.print(tree)


if __name__ == "__main__":
    main()
