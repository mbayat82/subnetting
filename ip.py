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
    num_addresses = network.num_addresses

    table = Table(show_header=True, box=box.SIMPLE_HEAD, header_style="bold magenta")
    table.add_column("Network")
    table.add_column("Netmask")
    table.add_column("Start Range")
    table.add_column("End Range")
    table.add_column("Hosts")

    table.add_row(
        format(network.network_address),
        format(network.netmask),
        format(network.network_address+1),
        format(network.network_address+num_addresses-1),
        str(num_addresses-2),
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
