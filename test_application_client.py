import asyncio
import websockets
import json
from datetime import datetime

class TestApplicationClient:
    def __init__(self, app_id="test_app_001"):
        self.app_id = app_id
        self.uri = f"wss://web-production-190fc.up.railway.app/ws/application/{app_id}"
        self.received_alerts = []
        
    async def connect_and_listen(self):
        """Connect to WebSocket and listen for alerts"""
        try:
            async with websockets.connect(self.uri) as websocket:
                print(f"Application {self.app_id} connected to WebSocket server")
                
                # Listen for messages
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        print(f"\n--- Received Message ---")
                        print(f"Type: {data.get('type')}")
                        print(f"Timestamp: {data.get('timestamp')}")
                        
                        if data.get('type') == 'initial_alerts':
                            alerts = data.get('alerts', [])
                            print(f"Received {len(alerts)} initial alerts")
                            self.received_alerts.extend(alerts)
                            
                        elif data.get('type') == 'new_alert':
                            alert = data.get('alert', {})
                            alert_id = data.get('alert_id')
                            print(f"New alert received: {alert.get('alert', 'Unknown')}")
                            print(f"Alert ID: {alert_id}")
                            self.received_alerts.append(alert)
                            
                        elif data.get('type') == 'alert_update':
                            change = data.get('change', {})
                            print(f"Alert update: {change.get('operationType', 'Unknown')}")
                            
                        elif data.get('type') == 'connection_established':
                            print(f"Connection established: {data.get('client_id')}")
                            
                        else:
                            print(f"Unknown message type: {data.get('type')}")
                            
                        print(f"Total alerts received so far: {len(self.received_alerts)}")
                        
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
        """Get statistics about received alerts"""
        return {
            "total_alerts": len(self.received_alerts),
            "alert_types": list(set(alert.get('alert_type', 'unknown') for alert in self.received_alerts)),
            "drone_ids": list(set(alert.get('drone_id', 'unknown') for alert in self.received_alerts))
        }

async def main():
    """Main function to run the test application client"""
    client = TestApplicationClient()
    
    print("Starting test application client...")
    print("This will connect to the WebSocket server and listen for alerts.")
    print("Press Ctrl+C to stop.")
    
    try:
        await client.connect_and_listen()
    except KeyboardInterrupt:
        print("\nStopping test application client...")
        stats = client.get_stats()
        print(f"Final stats: {stats}")

if __name__ == "__main__":
    asyncio.run(main()) 