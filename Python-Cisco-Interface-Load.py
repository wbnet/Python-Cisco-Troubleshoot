from netmiko import ConnectHandler
import re

LabSW3 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.2.238',
    'username': 'MyUser',
    'password': 'MyPass',
}

LabSW4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.2.239',
    'username': 'MyUser',
    'password': 'MyPass',
}

LabSW5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.2.240',
    'username': 'MyUser',
    'password': 'MyPass',
}

# Set interface threshold as percentage
myThr = 80
print("Interface load threshold is", myThr, "percent")

myThr = 255 * (myThr / 100)
# print(myThr)

myThr = int(myThr)
# print(myThr)

all_devices = [LabSW3, LabSW4, LabSW5]
# all_devices = [LabSW3, LabSW4]
# all_devices = [LabSW5]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)

    mySwitch = net_connect.send_command('show version | include uptime')

    myRaw = net_connect.send_command('show interfaces | include line protocol|load')
    # print(myRaw)

    x = re.findall("(\S+)\sis\s.+\n.+txload\s(\d{1,3})\/255,\srxload\s(\d{1,3})\/255", myRaw)
    # print(x)

    intCount = len(x)
    # print(intCount, "matches found with regex")
    # print(intCount)

    # print("For example, match 10")
    # print(x[10])
    # print(x[10][0])
    # print(x[10][1])
    # print(x[10][2])

    print("--------------------------------")
    print("")
    print(mySwitch)
    print("Interface load is above threshold on the following interfaces")

    for n in range (0,intCount):
        # print(x[n][0])
        # print(x[n][1])
        # print(x[n][2])

        txload = int(x[n][1])
        rxload = int(x[n][2])

        if txload > myThr or rxload > myThr:
            # Convert to percentage
            txload = 100 * (txload / 255)
            rxload = 100 * (rxload / 255)

            # Round to 1 decimal place
            txload = round(txload, 1)
            rxload = round(rxload, 1)

            print(x[n][0])
            print("txload is", txload, "percent")
            print("rxload is", rxload, "percent")

    print("")
    print("--------------------------------")
