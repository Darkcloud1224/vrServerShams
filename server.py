import asyncio
import websockets

# Dictionary to store connected clients in their respective rooms
rooms = {}

async def handle_client(websocket, path):
    # Get the room ID from the client
    room_id = await websocket.recv()
    
    # Create the room if it doesn't exist
    if room_id not in rooms:
        rooms[room_id] = set()

    # Add the client to the room
    rooms[room_id].add(websocket)
    print(f"Client joined room {room_id}")

    try:
        async for message in websocket:
            # Broadcast the message to all clients in the room
            for client in rooms[room_id]:
                if client != websocket:  # Don't send the message back to the sender
                    await client.send(message)
                    print(f"Message broadcasted in room {room_id}: {message}")

    finally:
        # Remove the client from the room upon disconnection
        rooms[room_id].remove(websocket)
        print(f"Client left room {room_id}")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
