import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_domain_and_subdomains(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    domain_set = set()

    # Extract domain from the provided URL
    base_domain = urlparse(url).hostname
    domain_set.add(base_domain)

    # Find all links in the page
    links = soup.find_all('a', href=True)

    for link in links:
        # Parse each link to extract the domain
        href = link['href']
        parsed_url = urlparse(href)
        domain = parsed_url.hostname

        # Check if the domain is not None and add it to the set
        if domain:
            domain_set.add(domain)

    return list(domain_set)

# Example usage for "example.com"
url = "https://example.com"
domains = get_domain_and_subdomains(url)

print("Domains and Subdomains:")
for domain in domains:
    print(domain)
