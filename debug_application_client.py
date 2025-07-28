import asyncio
import websockets
import json
from datetime import datetime

class DebugApplicationClient:
    def __init__(self, app_id="debug_app_001"):
        self.app_id = app_id
        self.uri = f"wss://web-production-190fc.up.railway.app/ws/application/{app_id}"
        self.received_messages = []
        
    async def connect_and_listen(self):
        """Connect to WebSocket and listen for alerts"""
        try:
            async with websockets.connect(self.uri) as websocket:
                print(f"Debug application {self.app_id} connected to WebSocket server")
                
                # Listen for messages
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        print(f"\n=== DEBUG: Received Message ===")
                        print(f"Message Type: {data.get('type')}")
                        print(f"Timestamp: {data.get('timestamp')}")
                        print(f"Full Message: {json.dumps(data, indent=2)}")
                        
                        self.received_messages.append(data)
                        
                        if data.get('type') == 'initial_alerts':
                            alerts = data.get('alerts', [])
                            print(f"Received {len(alerts)} initial alerts")
                            
                        elif data.get('type') == 'new_alert':
                            alert = data.get('alert', {})
                            alert_id = data.get('alert_id')
                            print(f"NEW ALERT RECEIVED!")
                            print(f"Alert ID: {alert_id}")
                            print(f"Alert Data: {json.dumps(alert, indent=2)}")
                            
                        elif data.get('type') == 'alert_update':
                            change = data.get('change', {})
                            print(f"Alert update: {change.get('operationType', 'Unknown')}")
                            
                        elif data.get('type') == 'connection_established':
                            print(f"Connection established: {data.get('client_id')}")
                            
                        else:
                            print(f"Unknown message type: {data.get('type')}")
                            
                        print(f"Total messages received: {len(self.received_messages)}")
                        print("=" * 50)
                        
                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket connection closed")
                        break
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")
    
    def get_stats(self):
        """Get statistics about received messages"""
        alert_messages = [msg for msg in self.received_messages if msg.get('type') == 'new_alert']
        return {
            "total_messages": len(self.received_messages),
            "alert_messages": len(alert_messages),
            "message_types": list(set(msg.get('type') for msg in self.received_messages))
        }

async def main():
    """Main function to run the debug application client"""
    client = DebugApplicationClient()
    
    print("Starting debug application client...")
    print("This will connect to the WebSocket server and show all received messages.")
    print("Press Ctrl+C to stop.")
    
    try:
        await client.connect_and_listen()
    except KeyboardInterrupt:
        print("\nStopping debug application client...")
        stats = client.get_stats()
        print(f"Final stats: {stats}")

if __name__ == "__main__":
    asyncio.run(main()) 