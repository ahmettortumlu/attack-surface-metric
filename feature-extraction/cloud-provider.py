import socket
import whois
import dns.resolver

def get_a_record(fqdn):
    try:
        answers = dns.resolver.resolve(fqdn, 'A')
        return [answer.address for answer in answers]
    except dns.resolver.NoAnswer:
        return []

def get_cloud_provider(emails):
    cloud_providers = {
        'amazon': 'Amazon Web Services (AWS)',
        'google': 'Google Cloud Platform (GCP)',
        'microsoft': 'Microsoft Azure',
        'lgcns': 'LGCNS'
    }

    for email in emails:
        for provider, name in cloud_providers.items():
            if provider in email:
                return name

    return 'Unknown Cloud Provider'

def get_whois_info(ip_address):
    try:
        # Perform a WHOIS query for the IP address
        w = whois.whois(ip_address)
        return w

    except whois.parser.PywhoisError:
        return None

# Get the Fully Qualified Domain Name (FQDN) from the user
fqdn = input("Enter the Fully Qualified Domain Name (FQDN): ")

# Get the A records for the FQDN
ip_addresses = get_a_record(fqdn)

if not ip_addresses:
    print(f"No A records found for {fqdn}")
else:
    print(f"\nIP Addresses for {fqdn}: {', '.join(ip_addresses)}")

    # Check cloud provider for each IP address
    for ip_address in ip_addresses:
        whois_info = get_whois_info(ip_address)

        if whois_info:
            cloud_provider = get_cloud_provider(whois_info.get('emails', []))
            print(f"\nCloud Provider for {ip_address}: {cloud_provider}")
        else:
            print(f"\nUnable to retrieve WHOIS information for {ip_address}")
