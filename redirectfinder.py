import re
import sys
import argparse
import urllib.parse
import concurrent.futures
import random
import subprocess
from urllib.parse import urlparse

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--threads", type=int, default=8, help="number of threads to use")
args = parser.parse_args()

# Read the input URLs from sys.stdin
url_list = sys.stdin.read().splitlines()

with open("redirect_payloads.txt", "r") as f:
    payloads = f.read().splitlines()

    # Read the input domain_name from sys.stdin
    for i, domain in enumerate(url_list):
        parsed_url = urlparse(domain)
        domain_name = parsed_url.netloc

    # Replace the target to domain_name    
    for i, payload in enumerate(payloads):
        if "target.com" in payload:
            payloads[i] = payload.replace("target.com", f"{domain_name}")

def check_url(url, payload):
    # Use a regular expression to replace all values in the query string with the payload
    cleaned_url = re.sub(r'=([^&]*)', f'={urllib.parse.quote(payload)}', url)
    decoded_url = urllib.parse.unquote(cleaned_url)

	# Send a request
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    ]

    headers = {"User-Agent": random.choice(user_agents)}
    # Define the command as a list of strings
    cmd = ['curl', '-H', f"{headers}", '-s', '-L', f"{decoded_url}", '-I']

    # Run the command and capture the output
    output = subprocess.run(cmd, capture_output=True, text=True)

    # Check the output for the string 'evil.com'
    if 'evil' in output.stdout:
        print(f"\033[1;31mVULNERABLE: {decoded_url}\033[0;0m")
    else:
        print(f"\033[1;32mNOT VULNERABLE: {decoded_url}\033[0;0m")

# Create a ThreadPoolExecutor with the specified number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    # Iterate over the payloads
    for payload in payloads:
        # Iterate over the URLs
        for url in url_list:
            try:
                # Submit the task to the executor
                future = executor.submit(check_url, url, payload)
                # Wait for the task to complete
                future.result()
            except KeyboardInterrupt:
                exit(0)
