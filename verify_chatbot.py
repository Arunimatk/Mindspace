import urllib.request
import json
import sys

def test_chatbot():
    url = "http://127.0.0.1:8000/pdashboard/chatbot/api/chat/"
    
    # Helper to send POST request
    def send_msg(message):
        data = json.dumps({"message": message}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    body = response.read().decode('utf-8')
                    return json.loads(body)
                else:
                    return {"error": f"Status {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    # Test 1: Simple hello
    print("Test 1: Sending 'Hello'...")
    res = send_msg("Hello")
    print("Response:", res.get('reply', res))

    # Test 2: Fallback Logic
    print("\nTest 2: Sending 'I feel lonely'...")
    res = send_msg("I feel lonely")
    print("Response:", res.get('reply', res))

    # Test 3: Fallback Logic (Bypassing emotion detection)
    print("\nTest 3: Sending 'Tell me a story about a cat'...")
    res = send_msg("Tell me a story about a cat")
    print("Response:", res.get('reply', res))

if __name__ == "__main__":
    test_chatbot()
