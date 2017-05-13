# ipamtools
Tools for dealing with phpIPAM

ipam2zone:
  Creates DNS zone file(s) containing forward and/or reverse records for
	a domain from phpIPAM.

ipam2dns:
	Updates a DNS server using TSIG update records for all IPs in a domain.


Usage:

Create an api user on phpipam. Create /etc/phpipamtools.cfg as per
examples/phpipamtools.cfg with the credentials for this user.

Create configuration files for ipam2zone and/or ipam2dns as per examples.

Run as:

ipam2dns dns.cfg
ipam2zone zone.cfg
