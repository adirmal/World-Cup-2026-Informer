import socket
import time

host = '127.0.0.1'
port = 7777

def send_frame(sock, frame):
    print(f"Sending:\n{frame}")
    sock.sendall(frame.encode('utf-8'))
    time.sleep(0.1) # קצת זמן לשרת לעבד
    response = sock.recv(1024).decode('utf-8')
    print("--- Response ---")
    print(response)
    print("----------------")
    return response

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    # 1. התחברות
    connect_frame = "CONNECT\naccept-version:1.2\nhost:stomp\nlogin:guest\npasscode:guest\n\n\0"
    send_frame(sock, connect_frame)

    # 2. הרשמה עם בקשת קבלה (Receipt)
    # שים לב לשדה receipt:77
    sub_frame = "SUBSCRIBE\ndestination:/topic/a\nid:1\nreceipt:77\n\n\0"
    resp = send_frame(sock, sub_frame)
    
    if "RECEIPT" in resp and "receipt-id:77" in resp:
        print("✅ SUCCESS: Received Receipt for SUBSCRIBE")
    else:
        print("❌ FAILURE: Did not receive Receipt")

    sock.close()

except Exception as e:
    print(f"Error: {e}")
