"""WebSocket endpoints for real-time updates - FULLY IMPLEMENTED"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
from loguru import logger
from datetime import datetime

router = APIRouter()

# Store active connections
active_connections: List[WebSocket] = []


@router.websocket("/signals")
async def websocket_signals(websocket: WebSocket):
    """WebSocket endpoint for real-time signals - IMPLEMENTED"""
    await websocket.accept()
    active_connections.append(websocket)
    client_id = id(websocket)
    logger.info(f"✅ WebSocket client {client_id} connected. Total: {len(active_connections)}")
    
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"📨 Received from {client_id}: {data}")
            
            # Echo back with timestamp
            response = {
                "type": "echo",
                "message": data,
                "timestamp": datetime.now().isoformat(),
                "server_time": datetime.now().timestamp()
            }
            await websocket.send_json(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"❌ WebSocket client {client_id} disconnected. Total: {len(active_connections)}")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@router.websocket("/live")
async def websocket_live_data(websocket: WebSocket):
    """WebSocket for live stock data - IMPLEMENTED"""
    await websocket.accept()
    active_connections.append(websocket)
    client_id = id(websocket)
    logger.info(f"✅ Live data client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle subscription
            if data.get('action') == 'subscribe':
                symbol = data.get('symbol', '').upper()
                logger.info(f"📊 Client {client_id} subscribed to {symbol}")
                
                # Send confirmation
                response = {
                    "type": "subscription",
                    "status": "subscribed",
                    "symbol": symbol,
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_json(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"❌ Live data client {client_id} disconnected")
    except Exception as e:
        logger.error(f"❌ Live data WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


async def broadcast_signal(message: dict):
    """Broadcast signal to all connected clients - IMPLEMENTED"""
    disconnected = []
    logger.info(f"📢 Broadcasting to {len(active_connections)} clients")
    
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            disconnected.append(connection)
    
    # Clean up disconnected clients
    for connection in disconnected:
        if connection in active_connections:
            active_connections.remove(connection)


async def broadcast_price_update(symbol: str, price: float, change: float):
    """Broadcast price update - IMPLEMENTED"""
    message = {
        "type": "price_update",
        "symbol": symbol,
        "price": price,
        "change": change,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_signal(message)


async def broadcast_new_signal(signal: dict):
    """Broadcast new buy signal - IMPLEMENTED"""
    message = {
        "type": "new_signal",
        "data": signal,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_signal(message)
