import subprocess
import time
import os
import signal

# הגדרות
CLIENT_EXE = "../bin/StompWCIClient"
HOST = "127.0.0.1"
PORT = "7777"
JSON_FILE = "events.json"

def run_client():
    """מריץ את הלקוח כתהליך ומחזיר את האובייקט שלו"""
    process = subprocess.Popen(
        [CLIENT_EXE, HOST, PORT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0 # Unbuffered כדי לקרוא פלט בזמן אמת
    )
    return process

def send_command(process, cmd):
    """שולח פקודה ללקוח ומדפיס אותה"""
    print(f"[{process.pid}] Sending: {cmd}")
    process.stdin.write(cmd + "\n")
    process.stdin.flush()
    time.sleep(0.5) # לתת זמן לעיבוד

def read_output(process, timeout=2):
    """קורא פלט מהלקוח (לא חוסם לגמרי)"""
    # הערה: קריאה מ-stdout בצורה לא חוסמת היא מסובכת ב-Python פשוט.
    # כאן אנחנו נשתמש בפתרון פשוט: ניתן לו לרוץ ונבדוק מה הוא כתב עד כה.
    # לסקריפט בדיקה אמיתי ומורכב יותר, צריך להשתמש ב-select או threads.
    return "" 
    # לצורך הפשטות, הבדיקה האוטומטית הזו תסתמך על כך שהשרת לא קורס.
    # בדיקת התוכן המדויק ("Login successful") דורשת קצת יותר קוד לקריאה אסינכרונית.

def test_login_logout():
    print("--- TEST 1: Login & Logout ---")
    alice = run_client()
    time.sleep(1) # זמן לחיבור
    
    send_command(alice, f"login {HOST}:{PORT} alice 1234")
    time.sleep(1)
    
    # אם הלקוח עדיין חי, זה סימן טוב
    if alice.poll() is not None:
        print("❌ FAILED: Client crashed after login")
        return

    send_command(alice, "logout")
    time.sleep(1)
    
    # כאן אנחנו מצפים שהלקוח ייסגר או יתנתק
    alice.terminate()
    print("✅ PASSED: Login & Logout executed without crash\n")

def test_pub_sub():
    print("--- TEST 2: Pub/Sub (Alice reports, Bob receives) ---")
    
    # 1. מפעילים את בוב ונרשמים
    bob = run_client()
    time.sleep(1)
    send_command(bob, f"login {HOST}:{PORT} bob 5678")
    send_command(bob, "join Germany_Japan")
    
    # 2. מפעילים את אליס ושולחים דיווח
    alice = run_client()
    time.sleep(1)
    send_command(alice, f"login {HOST}:{PORT} alice 1234")
    send_command(alice, "join Germany_Japan") # גם היא צריכה להצטרף כדי לשלוח? (ב-STOMP לא חייב, אבל במימוש שלך כן)
    
    send_command(alice, f"report {JSON_FILE}")
    time.sleep(2) # זמן להפצה
    
    # 3. בדיקה (ידנית או חצי אוטומטית)
    # כאן היינו רוצים לקרוא את הפלט של בוב ולראות "Kickoff".
    # מכיוון שזה מורכב טכנית בסקריפט פשוט, אנחנו נסתפק בלוודא שהם לא קרסו.
    
    if bob.poll() is None and alice.poll() is None:
        print("✅ PASSED: Clients are alive after Pub/Sub exchange")
    else:
        print("❌ FAILED: One of the clients crashed")
        
    alice.terminate()
    bob.terminate()
    print("\n")

def test_summary():
    print("--- TEST 3: Summary Generation ---")
    alice = run_client()
    time.sleep(1)
    send_command(alice, f"login {HOST}:{PORT} alice 1234")
    send_command(alice, "join Germany_Japan")
    send_command(alice, f"report {JSON_FILE}")
    time.sleep(1)
    
    summary_file = "test_summary.txt"
    # מוחקים אם קיים
    if os.path.exists(summary_file):
        os.remove(summary_file)
        
    send_command(alice, f"summary Germany_Japan alice {summary_file}")
    time.sleep(1)
    
    if os.path.exists(summary_file):
        with open(summary_file, 'r') as f:
            content = f.read()
            if "Germany vs Japan" in content and "Kickoff" in content:
                print("✅ PASSED: Summary file created with correct content")
            else:
                print("❌ FAILED: Summary file content is incorrect")
                print(f"Content: {content}")
    else:
        print("❌ FAILED: Summary file was not created")
        
    alice.terminate()
    print("\n")

if __name__ == "__main__":
    # וודא שהקובץ JSON קיים
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            f.write('{"team a": "Germany", "team b": "Japan", "events": [{"event name": "Kickoff", "time": 0, "general game updates": {}, "team a updates": {}, "team b updates": {}, "description": "Start"}]}')

    try:
        test_login_logout()
        test_pub_sub()
        test_summary()
    except Exception as e:
        print(f"Error during tests: {e}")
