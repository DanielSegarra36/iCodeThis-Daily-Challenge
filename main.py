import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://icodethis.com/app'

try:
  # Send an HTTP GET request to the URL
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags on the page associated with challenge
    img_tags = soup.find_all('img', {'alt': 'Challenge Image'})

    # Loop through the <img> tags
    for img_tag in img_tags:
      src_attribute = img_tag.get('src', '')
      alt_attribute = img_tag.get('alt', '')

      if 'base64' not in src_attribute.lower():
        print('Found <img> tag without "base64" in src attribute')
        image_url = img_tag.get('src')
        print(f'Image URL: icodethis.com{image_url}')
        break

      # print their attributes
      # attributes = img_tag.attrs
      # print('Attributes for the current image tag:')
      # for attr_name, attr_value in attributes.items():
      #     print(f'{attr_name}: {attr_value}')
      # print('\n')
  else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)

except requests.exceptions.RequestException as e:
  print('An error occurred:', e)
