from . import message

def make_and_send_message(msg_type, content, file_path, to, msg_socket, port):
    """Construct a message object with given attributes & send to address

    :param msg_type: str, one of the pre-defined message types
    :param content: obj, custom message content
    :param file_path: str, destination address of file to accompany message
    :param to: str, ip address of destination machine
    :param msg_socket: socket, via which to send the message
    :param port: int, port number on which message should be received
    """
    msg = message.Message(
        msg_type=msg_type, content=content, file_path=file_path)
    send_message(msg=msg, to=to, msg_socket=msg_socket, port=port)


def send_message(msg, to, msg_socket=None, port=PORT):
    """Sends binary/pickle of message object to receiver.

    :param msg: Message object with data of message to be sent
    :param to: String with IP address of receiver node
    :param msg_socket: Socket object on which message is to be sent. Opens new
        socket if value is None.
    :param port: Integer with port to be used for sending/receiving messages.
        Default is 5005.
    """
    if msg_socket is None:
        msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            msg_socket.connect((to, port))
        except OSError:
            # Raised if endpoint is already connected. No action is needed.
            pass

    msg.sender = msg_socket.getsockname()[0]
    msg_data = io.BytesIO(pickle.dumps(msg))

    try:
        while True:
            chunk = msg_data.read(BUFFER_SIZE)
            if not chunk:
                break
            msg_socket.send(chunk)
    except BrokenPipeError:
        # Connection with end-point broken due to node crash.
        # Do nothing as crash will be handled by crash detector and handler.
        pass

    try:
        msg_socket.shutdown(socket.SHUT_WR)
        msg_socket.close()
    except OSError:
        # Connection with end-point broken due to node crash.
        # Do nothing as crash will be handled by crash detector and handler.
        pass
   
