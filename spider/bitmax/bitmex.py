from websocket import create_connection

if __name__ == '__main__':
    ws = create_connection("wss://bitmex.com/realtime?subscribe=quoteBin1m", timeout=5)
    if ws.connected:
        ws.send('8')
        print(ws.recv())
        # ws.close()