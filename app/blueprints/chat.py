from flask import current_app, Blueprint, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

from app import db, socketio, ip_handler
from app.models import Message

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/tos')
def tos():
    ip_handler.check_ip()
    return render_template('tos.html')


@chat_bp.route('/chat')
def chat():
    ip_handler.check_ip()
    return render_template('chat.html')


@chat_bp.route('/get_messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp).all()  # Fetch all messages
    return jsonify([
        {
            'username': message.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat()  # Convert timestamp to ISO format
        } for message in messages
    ])


# SocketIO event for receiving messages
@socketio.on('send_message')
def handle_send_message_event(data):
    print(f"Received message: {data}")  # Debugging
    username = data['username']
    message_content = data['message']

    # Save the message in the database
    message = Message(username=username, content=message_content)
    db.session.add(message)
    db.session.commit()

    # Broadcast the message to all connected clients
    emit('receive_message', {
        'username': username,
        'message': message_content,
        'timestamp': message.timestamp.isoformat()  # Include the timestamp in the emitted message
    }, broadcast=True)


# SocketIO event for joining a room
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('receive_message', {'username': 'System', 'message': f'{username} has joined the room.'}, room=room)


# SocketIO event for leaving a room
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('receive_message', {'username': 'System', 'message': f'{username} has left the room.'}, room=room)