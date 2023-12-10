import requests
from bs4 import BeautifulSoup
import tldextract

def get_urls_from_user():
    urls = input("Enter a list of URLs separated by commas: ").split(',')
    return [url.strip() for url in urls]

def extract_fqdns(urls):
    fqdns = set()

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all href attributes from <a> tags
            links = [a['href'] for a in soup.find_all('a', href=True) if a.get('href')]

            for link in links:
                extracted_info = tldextract.extract(link)
                domain = extracted_info.domain
                subdomain = extracted_info.subdomain
                suffix = extracted_info.suffix

                # Check if the domain is not empty and add to the set
                if domain:
                    fqdn = f"{subdomain}.{domain}.{suffix}" if subdomain else f"{domain}.{suffix}"
                    fqdns.add(fqdn)

        except requests.exceptions.RequestException as e:
            print(f"Error making request for {url}: {e}")

    return list(fqdns)

# Example usage

user_urls = get_urls_from_user()

if user_urls:
    fqdns_result = extract_fqdns(user_urls)

    if fqdns_result:
        print("Unique Fully Qualified Domain Names (FQDNs):")
        print(fqdns_result)
    else:
        print("No FQDNs extracted from the provided URLs.")
else:
    print("No URLs provided.")
