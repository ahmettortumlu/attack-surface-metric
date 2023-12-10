import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_all_urls_from_list(urls):
    http_urls = []
    https_urls = []

    for url in urls:
        try:
            # Send a GET request to the specified URL
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all links from the page
            all_links = soup.find_all('a', href=True)

            for link in all_links:
                href = link['href']
                full_url = urljoin(url, href)  # Make sure to create an absolute URL

                parsed_url = urlparse(full_url)
                if parsed_url.scheme == 'http':
                    http_urls.append(full_url)
                elif parsed_url.scheme == 'https':
                    https_urls.append(full_url)

        except requests.exceptions.RequestException as e:
            print(f"Error making request for {url}: {e}")

    return http_urls, https_urls

# Get a list of URLs from the user
user_urls_input = input("Enter a list of URLs separated by commas: ")
user_urls = [url.strip() for url in user_urls_input.split(',')]

# Call the function and get the results
http_results, https_results = get_all_urls_from_list(user_urls)

# Print the results
print("\nHTTP URLs:")
for http_url in http_results:
    print(http_url)

print("\nHTTPS URLs:")
show_https_urls = input("Do you want to see HTTPS URLS too? (yes/no) ")
if show_https_urls == "yes":
    for https_url in https_results:
        print(https_url)