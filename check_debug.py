import urllib.request
from urllib.error import HTTPError

try:
    # Use a random path to trigger 404
    urllib.request.urlopen("https://mindspace-at8f.onrender.com/debug-check-123/")
except HTTPError as e:
    content = e.read().decode('utf-8')
    if "Page not found" in content and "Using the URLconf defined" in content:
        print("DEBUG_ACTIVE: True")
        print("Snippet:", content[:200])
    else:
        print("DEBUG_ACTIVE: False")
        print("Snippet:", content[:200])
except Exception as e:
    print(f"ERROR: {e}")
