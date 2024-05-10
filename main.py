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
    unformat = "OS:\t" + temp
    r.append(unformat)


def get_kernel(r):
    command = subprocess.run(["uname", "-rm"], stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    final = "Kernel:\t" + command
    r.append(final)


def get_uptime(r):
    command = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip("up ").rstrip()
    final = "Uptime:\t" + command
    r.append(final)


def get_memory(r):
    with open("/proc/meminfo", "r") as file:
        mem_total = file.readline().strip("MemTotal:\t").lstrip().rstrip().strip("kB")
        file.readline()
        mem_avail = file.readline().strip("MemAvailable:\t").lstrip().rstrip().strip("kB")
    mem_used = int(mem_total)//1024 - int(mem_avail)//1024
    final = "Memory:\t" + str(mem_used) + "M / " + str(int(mem_total)//1024) + "M"
    r.append(final)


def get_cpu(r):
    with open("/proc/cpuinfo", "r") as file:
        for i in range(4):
            file.readline()
        unformat_cpu = re.search(": ", file.readline())
        cpu = unformat_cpu.string.strip("model name:\t").rstrip()
    final = "CPU:\t" + cpu
    r.append(final)


def get_mobo_info(r):
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
    get_mobo_info(info)
    get_cpu(info)
    get_memory(info)
    get_kernel(info)
    get_uptime(info)
    for s in info:
        print(s)
