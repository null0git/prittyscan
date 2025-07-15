#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import json
import csv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_nmap(target, ports=None, udp=False, scripts=None, extra_args=None):
    cmd = ["nmap", "-oX", "-", "-sV"]
    if udp:
        cmd[1] = "-oX"  # keep XML output
        cmd.insert(1, "-sU")
    if ports:
        cmd.extend(["-p", ports])
    if scripts:
        cmd.extend(["--script", scripts])
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(target)
    console.print(f"[bold green]Running:[/] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]Nmap error:[/] {result.stderr}")
        exit(1)
    return result.stdout

def parse_nmap_xml(xml_data):
    root = ET.fromstring(xml_data)
    hosts_data = []
    for host in root.findall("host"):
        host_dict = {}
        address = host.find("address")
        host_dict["address"] = address.get("addr") if address is not None else "unknown"
        ports_list = []
        ports = host.find("ports")
        if ports is not None:
            for port in ports.findall("port"):
                p = {}
                p["protocol"] = port.get("protocol")
                p["portid"] = port.get("portid")
                state = port.find("state")
                p["state"] = state.get("state") if state is not None else "unknown"
                service = port.find("service")
                if service is not None:
                    p["name"] = service.get("name")
                    p["product"] = service.get("product", "")
                    p["version"] = service.get("version", "")
                    p["extrainfo"] = service.get("extrainfo", "")
                else:
                    p["name"] = ""
                    p["product"] = ""
                    p["version"] = ""
                    p["extrainfo"] = ""

                # Parse NSE scripts output attached to port
                script_elems = port.findall("script")
                p["scripts"] = []
                for s in script_elems:
                    p["scripts"].append({
                        "id": s.get("id"),
                        "output": s.get("output")
                    })
                ports_list.append(p)
        host_dict["ports"] = ports_list
        hosts_data.append(host_dict)
    return hosts_data

def show_results(hosts_data):
    for host in hosts_data:
        console.print(f"\n[bold underline]Host: {host['address']}[/]\n")
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Port", style="cyan", no_wrap=True)
        table.add_column("Protocol")
        table.add_column("State")
        table.add_column("Service")
        table.add_column("Version")

        for port in host["ports"]:
            version_str = " ".join(filter(None, [port["product"], port["version"], port["extrainfo"]]))
            table.add_row(
                port["portid"],
                port["protocol"],
                port["state"],
                port["name"],
                version_str
            )
            # Show NSE scripts output nested under this port if present
            for script in port.get("scripts", []):
                console.print(Panel(f"[yellow]{script['output']}[/]", title=f"NSE Script: {script['id']}", padding=(0,1), border_style="green"))
        console.print(table)

def export_csv(hosts_data, filename):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["host", "port", "protocol", "state", "service", "product", "version", "extrainfo"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for host in hosts_data:
            for port in host["ports"]:
                writer.writerow({
                    "host": host["address"],
                    "port": port["portid"],
                    "protocol": port["protocol"],
                    "state": port["state"],
                    "service": port["name"],
                    "product": port["product"],
                    "version": port["version"],
                    "extrainfo": port["extrainfo"]
                })
    console.print(f"[green]Exported CSV to {filename}[/]")

def export_json(hosts_data, filename):
    with open(filename, "w") as jsonfile:
        json.dump(hosts_data, jsonfile, indent=2)
    console.print(f"[green]Exported JSON to {filename}[/]")

def main():
    parser = argparse.ArgumentParser(description="Fancy Nmap TUI Frontend with Export")
    parser.add_argument("target", help="Target host or IP")
    parser.add_argument("-p", "--ports", help="Ports or port ranges to scan, e.g. 22,80,443,1000-2000")
    parser.add_argument("-u", "--udp", action="store_true", help="Enable UDP scan")
    parser.add_argument("-s", "--scripts", help="Nmap NSE scripts to run, comma-separated")
    parser.add_argument("--export-csv", help="Export results to CSV file")
    parser.add_argument("--export-json", help="Export results to JSON file")
    parser.add_argument("--extra-args", help="Extra raw nmap arguments", default="", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    xml_output = run_nmap(args.target, args.ports, args.udp, args.scripts, args.extra_args)
    hosts_data = parse_nmap_xml(xml_output)
    show_results(hosts_data)

    if args.export_csv:
        export_csv(hosts_data, args.export_csv)
    if args.export_json:
        export_json(hosts_data, args.export_json)

if __name__ == "__main__":
    main()
