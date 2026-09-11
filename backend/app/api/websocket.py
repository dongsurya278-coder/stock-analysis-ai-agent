"""WebSocket endpoints for real-time updates"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
from loguru import logger

router = APIRouter()

# Store active connections
active_connections: List[WebSocket] = []


@router.websocket("/signals")
async def websocket_signals(websocket: WebSocket):
    """WebSocket endpoint for real-time signals"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"Client connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or process the data
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(active_connections)}")


async def broadcast_signal(message: dict):
    """Broadcast signal to all connected clients"""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            disconnected.append(connection)
    
    # Clean up disconnected clients
    for connection in disconnected:
        active_connections.remove(connection)
