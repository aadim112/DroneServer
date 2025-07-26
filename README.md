# Real-Time Drone Alert Management System

A comprehensive real-time drone alert management system with WebSocket communication and MongoDB Change Streams for instant updates.

## 🚀 Features

- **Real-time Communication**: Bidirectional WebSocket communication between drones, applications, and server
- **MongoDB Change Streams**: Database cursor monitoring for instant alert updates
- **Persistent Storage**: MongoDB database with proper indexing for performance
- **Scalable Architecture**: Modular design supporting multiple drones and applications
- **REST API**: Additional HTTP endpoints for integration
- **Example Clients**: Python clients for testing and demonstration

## 🏗️ Architecture

```
┌─────────────┐    WebSocket    ┌─────────────┐    WebSocket    ┌─────────────┐
│    Drone    │ ◄──────────────► │    Server   │ ◄──────────────► │ Application │
│             │                 │             │                 │             │
└─────────────┘                 └─────────────┘                 └─────────────┘
                                        │
                                        │ MongoDB
                                        ▼
                                ┌─────────────┐
                                │  Database   │
                                │ (Change     │
                                │  Streams)   │
                                └─────────────┘
```

## 📋 Requirements

- Python 3.8+
- MongoDB 4.0+ (with Change Streams support)
- FastAPI
- WebSocket support

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd drone-alert-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**
   - Install MongoDB 4.0+ with Change Streams support
   - Start MongoDB service
   - Create database: `drone_alerts_db`

4. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string and other settings
   ```

## 🚀 Quick Start

1. **Start the server**
   ```bash
   python main.py
   ```
   The server will start on `http://localhost:8000`

2. **Run example clients** (in separate terminals)
   ```bash
   # Terminal 1: Start application client
   python examples/application_client.py
   
   # Terminal 2: Start drone client
   python examples/drone_client.py
   ```

3. **Access the API documentation**
   - Open `http://localhost:8000/docs` for Swagger UI
   - Open `http://localhost:8000/redoc` for ReDoc

## 📊 Database Schema

### Alerts Collection
```json
{
  "alert_id": "string (unique)",
  "alert_type": "intrusion|fire|accident|security_breach|environmental|other",
  "score": "float (0.0-1.0)",
  "image_url": "string (optional)",
  "location": {
    "lat": "float",
    "lng": "float"
  },
  "drone_id": "string",
  "timestamp": "datetime",
  "response": "int (0=no response, 1=responded)",
  "image_received": "int (0=no image, 1=received)",
  "actions": ["array of strings"],
  "status": "pending|responded|completed",
  "description": "string (optional)"
}
```

## 🔄 Data Flow

### 1. Drone to Server Flow
1. Drone detects event and sends alert via WebSocket
2. Server stores alert in MongoDB with `response=0`, `image_received=0`
3. MongoDB Change Stream detects insert and broadcasts to applications
4. Applications receive real-time alert notification

### 2. Application Response Flow
1. Application processes alert with RL model
2. Application sends response with actions via WebSocket
3. Server updates alert in MongoDB with `response=1` and actions
4. Change Stream broadcasts update to all applications
5. Server sends command to specific drone

### 3. Drone Execution Flow
1. Drone receives command from server
2. Drone executes actions and captures image
3. Drone sends image data via WebSocket
4. Server updates alert with `image_received=1` and image URL
5. Change Stream broadcasts final update to applications

## 🌐 API Endpoints

### WebSocket Endpoints
- `ws://localhost:8000/ws/drone/{drone_id}` - Drone connections
- `ws://localhost:8000/ws/application/{app_id}` - Application connections

### REST API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/alerts` - Get all alerts
- `GET /api/alerts/{alert_id}` - Get specific alert
- `POST /api/alerts` - Create new alert
- `PUT /api/alerts/{alert_id}/response` - Update alert response
- `PUT /api/alerts/{alert_id}/image` - Update alert image
- `GET /api/stats` - Get system statistics

## 📡 WebSocket Message Format

### Alert Message (Drone → Server)
```json
{
  "type": "alert",
  "data": {
    "alert_type": "intrusion",
    "score": 0.85,
    "location": {"lat": 40.7128, "lng": -74.0060},
    "drone_id": "drone_001",
    "description": "Suspicious activity detected"
  }
}
```

### Response Message (Application → Server)
```json
{
  "type": "response",
  "alert_id": "alert_123",
  "data": {
    "actions": ["activate_security", "notify_authorities"],
    "response": 1
  }
}
```

### Image Message (Drone → Server)
```json
{
  "type": "image",
  "data": {
    "alert_id": "alert_123",
    "image_url": "http://localhost:8000/uploads/image.jpg"
  }
}
```

## 🔧 Configuration

### Environment Variables
```bash
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=drone_alerts_db
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here
```

### MongoDB Setup
```bash
# Start MongoDB
mongod --dbpath /path/to/data/db

# Create database and collection
mongo
use drone_alerts_db
db.createCollection("alerts")
```

## 🧪 Testing

### Manual Testing
1. Start the server
2. Run example clients
3. Monitor the console output for real-time updates

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Get all alerts
curl http://localhost:8000/api/alerts

# Create test alert
curl -X POST http://localhost:8000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "intrusion",
    "score": 0.8,
    "location": {"lat": 40.7128, "lng": -74.0060},
    "drone_id": "test_drone"
  }'
```

## 📈 Monitoring

### System Statistics
- Active WebSocket connections
- Database connection status
- Alert processing metrics

### Logs
- Connection events
- Alert processing
- Error handling
- Change stream events

## 🔒 Security Considerations

- Implement authentication for production use
- Use HTTPS/WSS for secure communication
- Validate all incoming data
- Implement rate limiting
- Secure MongoDB access

## 🚀 Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Environment Setup
1. Set production MongoDB URI
2. Configure proper CORS settings
3. Set up SSL certificates
4. Implement authentication
5. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the example clients

## 🔄 Changelog

### v1.0.0
- Initial release
- WebSocket communication
- MongoDB Change Streams
- Example clients
- REST API endpoints # DroneServer
