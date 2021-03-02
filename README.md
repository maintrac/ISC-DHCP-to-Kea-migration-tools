# ISC-DHCP-to-Kea-migration-tools
Tools to help migrate a ISC DHCP to Kea

## convert_isc_dhcpd_leases_to_kea.py
Script to convert ISC DHCP leases file to Kea mem-file leases

Takes two or three inputs, the first is the ISC DHCP leases file and the second the output file in Kea mem-file format. 

The third and optional input is the location of Kea dhcp4 configuration which defaults to /etc/kea/kea-dhcp4.conf. 
This input is used to get the subnet id for each ip address and is part of the leases file.
