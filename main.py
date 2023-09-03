import re
import datetime
import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://icodethis.com/app'

# File to append URLs to
urlsOnlyFile = 'iCodeThisMockupURLs.txt'
markdownFile = 'iCodeThisMockupURLs.md'

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
        full_url = f'https://www.icodethis.com{image_url}'
        print(f'Image URL: {full_url}')

        # Open the file in append mode
        with open(urlsOnlyFile, 'a') as urlFile:
          # Append the URL to the file
          urlFile.write(full_url + '\n')

        # Open the file in append mode
        with open(markdownFile, 'a') as mdFile:
          # Define the regular expression pattern to match the desired substring
          pattern = r'image\?url=%2Fimages%2Fprojects%2F(.*?)\.jpg'

          # Use re.search to find the match in the input string
          match = re.search(pattern, image_url)

          # Check if a match was found
          if match:
            extracted_string = match.group(1).replace(
                '_', ' ').title()  # Extract the matched substring
            print(f'extracted_string: {extracted_string}\n')

            # Get the current date and time
            current_datetime = datetime.datetime.now()

            # Format the timestamp as a string
            timestamp = current_datetime.strftime("%Y-%m-%d")

            mdFile.write(f'[{timestamp}: {extracted_string}]({full_url})  \n')
          else:
            print("No match found")
          # Append the URL to the file
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
