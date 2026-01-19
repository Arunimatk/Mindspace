import urllib.request
import urllib.parse
import http.cookiejar
import re
import datetime
import sys
from urllib.error import HTTPError

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

base_url = "https://mindspace-at8f.onrender.com"

def get_csrf(url):
    print(f"GET {url}...")
    try:
        resp = opener.open(url)
        html = resp.read().decode('utf-8')
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', html)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Failed to fetch CSRF from {url}: {e}")
        return None

try:
    # 1. Register
    print("Action: Registering new user...")
    csrf_token = get_csrf(base_url + "/register/")
    if not csrf_token:
        print("Could not get CSRF token.")
        sys.exit(1)
    
    unique_user = "user_" + datetime.datetime.now().strftime("%H%M%S")
    
    reg_data = urllib.parse.urlencode({
        'name': unique_user,
        'password': 'password123',
        'email': f'{unique_user}@example.com',
        'age': '25',
        'phone': '1234567890',
        'csrfmiddlewaretoken': csrf_token
    }).encode()
    
    reg_req = urllib.request.Request(base_url + "/register/", data=reg_data)
    reg_req.add_header('Referer', base_url + "/register/")
    opener.open(reg_req) # Should redirect to login
    print("Registration OK (No Crash)")

    # 2. Login
    print(f"Action: Logging in as {unique_user}...")
    csrf_token = get_csrf(base_url + "/login/")
    
    login_data = urllib.parse.urlencode({
        'username': unique_user,
        'password': 'password123',
        'csrfmiddlewaretoken': csrf_token
    }).encode()
    
    login_req = urllib.request.Request(base_url + "/login/", data=login_data)
    login_req.add_header('Referer', base_url + "/login/")
    
    try:
        resp = opener.open(login_req)
        content = resp.read().decode('utf-8')
        final_url = resp.geturl()
        
        print(f"Login Response URL: {final_url}")
        
        # Analyze Cookie
        session_cookie = None
        for cookie in cj:
            if cookie.name == 'sessionid':
                session_cookie = cookie.value
                print(f"Session Cookie Found: Length={len(session_cookie)}")
                break
        
        if session_cookie and len(session_cookie) > 100:
             print("SUCCESS: Session cookie is LARGE, indicating signed_cookies backend.")
        elif session_cookie:
             print("WARNING: Session cookie is SMALL (32 chars?), indicating DB backend!")
             print(f"Cookie Value: {session_cookie}")

        if "projectpart2" in final_url:
            print("SUCCESS: Full Flow Completed. Logged in and redirected to Dashboard.")
        elif "Server Error" in content:
            print("CRASH during Login Success Path!")
        else:
            print("Login Failed (Logic) or Unexpected Redirect.")
            print(content[:500])
            
    except HTTPError as e:
        print(f"CRASH: {e.code}")
        print(e.read().decode('utf-8')[:2000])

except Exception as e:
    print(f"Error: {e}")
