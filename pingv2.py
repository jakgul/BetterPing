import os
import subprocess
import platform
import ipaddress

class betterping():

    def __init__(self,ips=[],ping_count=2, subnet=""):
        self.master_ip_list=ips
        self.ping_count = ping_count
        self.subnet = subnet
        self.platform = platform.system().lower()
        self.ping_result = ""

    def flatten_ips(self,ip):
        if "/" in ip:  #convert network address to IPs
            self.find_ips_in_subnet(ip)
        else:
            self.master_ip_list.append(ip)

    def load_ips(self,filename):
        with open(filename) as file:  #load IPs from a spesific file
            ip_text_file = file.read()
            ip_list = ip_text_file.split("\n")
            for ip in ip_list:
               self.flatten_ips(ip.strip())

    def find_ips_in_subnet(self,subnet):
        for addr in ipaddress.ip_network(subnet):  #find all the IPs in network, add it to list
            self.master_ip_list.append(str(addr))

    def save_output(self,filename="pingresult.txt"):  #write the ping result to a file
        file = open(filename, "w")
        file.write(self.ping_result)
        file.close()

    def get_ip_from_user_or_file(self,ip):
        if '/' in ip:
            self.find_ips_in_subnet(ip)
        if not ip=='none' and type(ip)==str :
            self.master_ip_list.append(ip)
        if type(ip)==list:
            for each_ip in ip:
                self.flatten_ips(each_ip.strip())

    def is_up(self,ip):
        if self.platform == "windows":
            return self.windows_ping(ip)
        else:
            return self.linux_ping(ip)

    def ping(self,ip='none'):
        self.get_ip_from_user_or_file(ip)
        for ip in self.master_ip_list:
            if self.platform == "windows":
                if self.windows_ping(ip):
                    print(ip + ' is UP!')
                    self.ping_result += ip + ' is UP!\n'
                else:
                    print(ip + ' is DOWN!')
                    self.ping_result += ip + ' is DOWN!\n'
            else:
                if self.linux_ping(ip):
                    print(ip + ' is UP!')
                    self.ping_result += ip + ' is UP!\n'
                else:
                    print(ip + ' is DOWN!')
                    self.ping_result += ip + ' is DOWN!\n'
        return self.ping_result

    def linux_ping(self,ip):
        command = "ping -c {} {}".format(str(self.ping_count), ip)  #EX: ping -c 1 10.10.10.1  (send 1 ping)
        response = os.system(command)
        if response == 0:
            return True
        else:
            return False

    def windows_ping(self,ip):
        command = "ping -n {} {}".format(str(self.ping_count), ip)   #EX: ping -n 1 10.10.10.1  (send 1 ping)
        response = subprocess.run(command, capture_output=True)
        output = response.stdout.decode()
        if "Destination host unreachable" in output:
            return False
        elif "Request timed out" in output:
            return False
        else:
            return True





############################################
#Run the script by editing below
############################################

# Step 1, call the class object and create a smartping object
# a = betterping()
# a.ping_count = 1
# #Step 2, load IPs.
# #a.load_ips("ips.txt")    #load IPs from file
# #a.ips = ["10.70.69.0/30","10.70.70.2","10.70.70.3"] #load IPs as a list
# print(a.ping("2.2.2.0/29"))

# Step 3 Specify the ping count(default is 2)
# a.ping_count = 1
# Step 4, call the ping function
# a.ping()
# print(a.is_up('10.1.10.0'))
# Step 5, save the ping results to a file. Default file name is pingresult.txt or specify the name
# a.save_output("writehere.txt")
#

