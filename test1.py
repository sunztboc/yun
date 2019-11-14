from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
remote_device = {'device_type': 'autodetect',
                     'host': 'www.hblzjz.com',
                     'username': 'root',
                     'password': 'citicnet'}
guesser = SSHDetect(**remote_device)
best_match = guesser.autodetect()
# Netmiko connection creation section
remote_device['device_type'] = best_match
net_connect = ConnectHandler(**remote_device)
output = net_connect.send_command('df -h')
print(output)