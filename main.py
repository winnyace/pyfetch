import re
import subprocess
import termcolor


def get_user(r):
    username = (subprocess.run(["whoami"], stdout=subprocess.PIPE)
                .stdout.decode("utf-8")
                .rstrip())
    hostname = (subprocess.run(["hostname"], stdout=subprocess.PIPE)
                .stdout.decode('utf-8')
                .rstrip())
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
    command = (subprocess.run(["uname", "-rm"], stdout=subprocess.PIPE)
               .stdout.decode("utf-8")
               .rstrip())
    final = "Kernel:\t" + command
    r.append(final)


def get_uptime(r):
    res = {}
    with open('/proc/uptime', 'r') as file:
        time = re.split(" ", file.read())
        time = float(time[0])
        res['days'] = time//86400
        res['hours'] = time//3600
        res['minutes'] = time%3600//60
    final = "Uptime:\t"
    for x in res:
        if res[x] != 0:
            final = final + str(int(res[x])) + " " + str(x) + " "
    r.append(final)

def get_memory(r):
    with (open("/proc/meminfo", "r")) as file:
        mem_total = file.readline().strip("MemTotal:\t").lstrip().rstrip().strip("kB")
        file.readline()
        mem_avail = file.readline().strip("MemAvailable:\t").lstrip().rstrip().strip("kB")
    mem_used = int(mem_total) // 1024 - int(mem_avail) // 1024
    final = "Memory:\t" + str(mem_used) + "M / " + str(int(mem_total) // 1024) + "M"
    r.append(final)


def get_cpu(r):
    with (open("/proc/cpuinfo", "r") as file):
        for _ in range(4):
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


def get_gpu(r):
    cmdp1 = subprocess.Popen(["lspci"], stdout=subprocess.PIPE)
    cmdp2 = subprocess.Popen(["grep", "VGA"], stdin=cmdp1.stdout, stdout=subprocess.PIPE)
    cmdout, cmderr = cmdp2.communicate()
    out = cmdout.decode("utf-8")
    out = out.split('\n')
    out.pop()

    final_temp = []
    for s in out:
        gpu = str()
        manu = str()
        if re.findall("AMD/ATI", s):
            manu = re.findall("AMD/ATI", s)[0] + " "
        if re.findall("NVIDIA", s):
            manu = re.findall("NVIDIA", s)[0] + " "
        if re.findall("Intel", s):
            manu = re.findall("Intel", s)[0] + " "

        model = re.findall(r'\[.*?]', s)
        for j in model:
            temp = j.strip("[]")
            if temp != "AMD/ATI":
                gpu = gpu + manu + temp
            final_temp.append(gpu)

    final_temp = list(filter(lambda x: x != '', final_temp))
    final = final_temp[0] + "; " + final_temp[1]
    final = "GPU(s):\t" + final
    r.append(final)


if __name__ == "__main__":
    result_list = []

    get_user(result_list)
    get_distro(result_list)
    get_kernel(result_list)
    get_uptime(result_list)
    result_list.append(" ")
    get_mobo_info(result_list)
    get_cpu(result_list)
    get_gpu(result_list)
    get_memory(result_list)

    for i in result_list:
        print(i)
