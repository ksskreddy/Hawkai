"""File with class for message objects.
"""


class Message(object):
    """Class defining messages to be passed for system communication.

    Attributes:
          msg_type: String with type of message.
          content: Data structure/string with message contents.
                Default:None
                LEADER_ELECT:dict with node_ip and node_id
                LEADER_ELECT_ACK:None
          sender: String with IP address of sender machine.
          file: Byte string with file contents.
                Default: None
                LEADER_ELECT:None
                LEADER_ELECT_ACK:None
    """

    def __init__(self, msg_type, content=None, file_path=None, file=None):
        """Initializes Message object with type parameters and adds content.

        Args:
            msg_type: String with type of message.
            content: Data structure/string with message contents.
            file_path: String with absolute path to file to be included. If file
                is also given, it will be ignored.
            file: Byte stream of file. If file_path is not None, this will be
                ignored.
        """
        self.msg_type = msg_type
        self.content = content

        self.sender = None
        self.file = file
        if file_path is not None:
            with open(file_path, 'rb') as file:
                self.file = file.read()

    def __str__(self):
        """Custom function to print message details.

        :return: String representation of message information.
        """
        return self.msg_type + ' ' + str(self.content)
