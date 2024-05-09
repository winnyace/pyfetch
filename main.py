import re
import subprocess
import termcolor


def get_user(r):
    username = subprocess.run(["whoami"], stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    hostname = subprocess.run(["hostname"], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    unformat = username + str("@") + hostname
    final = termcolor.colored(unformat, attrs=['bold'])
    r.append(final)


def get_distro(r):
    with open("/usr/lib/os-release", "r") as f:
        for line in f:
            if re.search("PRETTY_NAME=", line):
                temp = line[line.find("\""):]
                temp = temp.replace('"', '')
                temp = temp.rstrip()
    unformat = "OS:\t\t" + temp
    r.append(unformat)


def get_kernel(r):
    command = subprocess.run(["uname", "-srm"], stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    final = "Kernel:\t" + command.strip("Linux ")
    r.append(final)


def get_uptime(r):
    command = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip("up ").rstrip()
    final = "Uptime:\t" + command
    r.append(final)


def get_memory(r):
    with open("/proc/meminfo", "r") as file:
        memtotal = file.readline().strip("MemTotal:\t").lstrip().rstrip().strip("kB")
        file.readline()
        memavail = file.readline().strip("MemAvailable:\t").lstrip().rstrip().strip("kB")
    memused = int(memtotal)//1024 - int(memavail)//1024
    final = "Memory:\t" + str(memused) + "M / " + str(int(memtotal)//1024) + "M"
    r.append(final)


def get_cpu(r):
    with open("/proc/cpuinfo", "r") as file:
        for i in range(4):
            file.readline()
        unformattedcpu = re.search(": ", file.readline())
        cpu = unformattedcpu.string.strip("model name:\t").rstrip()
    final = "CPU:\t" + cpu
    r.append(final)


def get_moboinfo(r):
    with open("/sys/devices/virtual/dmi/id/product_name") as file:
        name = file.read().rstrip()
    with open("/sys/devices/virtual/dmi/id/product_version") as file:
        ver = file.read().rstrip()
    final = "Mobo:\t" + name + " " + ver
    r.append(final)


if __name__ == "__main__":
    info = []

    get_user(info)
    get_distro(info)
    get_moboinfo(info)
    get_cpu(info)
    get_memory(info)
    get_kernel(info)
    get_uptime(info)
    for s in info:
        print(s)
