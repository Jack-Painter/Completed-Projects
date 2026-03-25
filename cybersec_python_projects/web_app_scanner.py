# Python Web App Scanner
import requests

def scan_web_app(url):
    vulnerabilities = []

    # SQL Injection
    payload = "' OR '1'='1"
    response = requests.get(url + "?param=" + payload)
    if "error" in response.text:
        vulnerabilities.append("SQL Injection")

    # XSS
    payload = "<script>alert('XSS')</script>"
    response = requests.get(url + "?param=" + payload)
    if "<script>alert('XSS')</script>" in response.text:
        vulnerabilities.append("Cross-Site Scripting (XSS)")

    # Directory Traversal
    payload = "../../../../etc/passwd"
    response = requests.get(url + "?file=" + payload)
    if "root:" in response.text:
        vulnerabilities.append("Directory Traversal")

    return vulnerabilities

target_url = "your URL to check goes here"
vulnerabilities_found = scan_web_app(target_url)
if vulnerabilities_found:
    print("Vulnerabilities found in the web app:")
    for vulnerability in vulnerabilities_found:
        print("- " + vulnerability)
else:
    print("No vulnerabilities found in the web app.")
