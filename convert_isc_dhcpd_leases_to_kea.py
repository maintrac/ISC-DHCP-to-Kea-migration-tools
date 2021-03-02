#!/usr/bin/python3
import sys, os
import csv, datetime, ipaddress, json, re


def main():
  if len(sys.argv) < 3:
    print("Usage: convert_isc_dhcpd_leases_to_kea.py <isc_leases_file> <csv_file_name> [<kea_dhcp4.conf>]")
    sys.exit()
  
  if not os.path.isfile(sys.argv[1]):
    print(f"Can't find file '{sys.argv[1]}'")
    sys.exit()
  
  keaConfigurationFile = "/etc/kea/kea-dhcp4.conf"
  if len(sys.argv) >= 4:
    keaConfigurationFile = sys.argv[3]

  if not os.path.isfile(keaConfigurationFile):
    print(f"Unable to find Kea dhcp4 configuration file: {keaConfigurationFile}")
    sys.exit()

  with open(sys.argv[1]) as f:
    raw = f.read()

  with open(keaConfigurationFile) as f:
    keaConf = json.load(f)

  subnets = {}

  if 'Dhcp4' not in keaConf:
    print("Can not find Dhcp4 part of Kea configuration file")
    sys.exit()

  if 'subnet4' in keaConf['Dhcp4']:
    for subnet in keaConf['Dhcp4']['subnet4']:
     subnets[ipaddress.ip_network(subnet['subnet'])] = subnet['id']
  if 'shared-networks' in keaConf['Dhcp4']:
    for sharedNet in keaConf['Dhcp4']['shared-networks']:
      for subnet in sharedNet['subnet4']:
         subnets[ipaddress.ip_network(subnet['subnet'])] = subnet['id']

  regex = r"lease ([\d\.]+) \{((?!starts ).)*starts [\d]+ ([\d\/\ :]+)((?!ends ).)*ends [\d]+ ([\d\/\ :]+)((?!ethernet).)*ethernet ([0-9a-f:]+)[^\}]+\}"

  matches = re.finditer(regex, raw, re.MULTILINE | re.DOTALL)

  f = open(sys.argv[2], mode='w')
  f.write("address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context\n")

  for matchNum, match in enumerate(matches, start=1):
    ipAddress = match.group(1)
    macAddress = match.group(7)
    starttime = datetime.datetime.strptime(match.group(3), "%Y/%m/%d %H:%M:%S")
    endtime = datetime.datetime.strptime(match.group(5), "%Y/%m/%d %H:%M:%S")
    leasetime = endtime - starttime
    subnetId = 0
    for subnet in subnets:
      if ipaddress.ip_address(ipAddress) in subnet:
        subnetId = subnets[subnet]
        break

    data = f"{ipAddress},{macAddress},{macAddress},14400,{int(endtime.timestamp())},{subnetId},0,0,,0,"
    f.write(data)
    f.write("\n")

  f.close()

if __name__ == '__main__':
  main()
