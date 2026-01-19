import urllib.request
import urllib.parse
import http.cookiejar
import re
from urllib.error import HTTPError

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

print("Step 1: Fetching Login Page...")
try:
    resp = opener.open("https://mindspace-at8f.onrender.com/login/")
    html = resp.read().decode('utf-8')
    
    # Extract CSRF token
    match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', html)
    if not match:
        print("ERROR: Could not find CSRF token in login page.")
        # Proceeding without token might fail, but let's see.
        csrf_token = ""
    else:
        csrf_token = match.group(1)
        print("CSRF Token found.")

    print("Step 2: Submitting Login Form...")
    data = urllib.parse.urlencode({
        'username': 'test',
        'password': 'test',
        'csrfmiddlewaretoken': csrf_token
    }).encode()
    
    # Ensure Referer header is set (Django CSRF strictness)
    req = urllib.request.Request("https://mindspace-at8f.onrender.com/login/", data=data)
    req.add_header('Referer', 'https://mindspace-at8f.onrender.com/login/')
    
    resp = opener.open(req)
    print("Response Code:", resp.getcode())
    content = resp.read().decode('utf-8')
    
    if "Invalid username" in content:
        print("SUCCESS: Login logic executed. Result: Invalid Username (Expected)")
    elif "Server Error" in content or "Traceback" in content:
         print("CRASH DETECTED in 200 OK response!")
         print(content[:1000])
    else:
        print("Response Content Preview:")
        print(content[:500])

except HTTPError as e:
    print(f"CRASH: HTTP {e.code}")
    error_content = e.read().decode('utf-8')
    print("Error Details:")
    # Print the exception type and value from Django debug page
    if "exception_value" in error_content:
        # Simple extraction
        print(error_content[:2000]) 
    else:
        print(error_content[:1000])

except Exception as e:
    print(f"Script Error: {e}")
