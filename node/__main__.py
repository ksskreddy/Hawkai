import argparse
import multiprocessing as mp
import os.path
import pickle
import socket
import signal
import sys
import time
import psutil
from ctypes import c_bool
from ..messages import messageutils
from ..utils import networkparams
from . import message_handlers

LEADER_ID = -1
LEADER_IP = ""
LEADER_FIXED = False



def parse_neighbour_file(neighbour_file):
    file = open(neighbour_file,"r")
    neigh_list = file.readlines()
    file.close()
    return neigh_list


def elect_leader(neighbour_file,selfid,selfip):
	global LEADER_ID
	global LEADER_IP
	global LEADER_FIXED
	LEADER_ID = selfid
	LEADER_IP = selfip
	neighbour_list = parse_neighbour_file(neighbour_file)
	content = {"leader_id":selfid,"leader_ip":selfip,"sender_ip":selfip}
	for ip in neighbour_list:
	    messageutils.make_and_send_message(
	            msg_type='LEADER_ELECT',
	            content=content,
	            file_path=None,
	            to=ip,
	            msg_socket=None,
	            port=networkparams.CLIENT_SEND_PORT)


def main():
	global LEADER_ID
	global LEADER_IP
	global LEADER_FIXED
	parser = argparse.ArgumentParser()
	parser.add_argument("-selfip",help="IP address of self", type=str, required=True)
	parser.add_argument("-uniqueid",help="Unique Id of the node",type=int, required=True)
	parser.add_argument("-neighbourlist", help="File containing ips of neighbours",type=str, required=True)
	args = vars(parser.parse_args())
	selfip = args['selfip']
	selfid = args['uniqueid']
	neighbourfile = args['neighbourlist']
	neighbourlist = parse_neighbour_file(neighbourfile)
	parent_ip = None
	leader_elect_acks = 0

	if LEADER_ID==-1:
	    elect_leader(neighbourfile,selfid,selfip)
	    parent_ip = selfip


	msg_socket = socket.socket()
	msg_socket.bind(('', networkparams.CLIENT_RECV_PORT))
	msg_socket.listen(5)

	while True:
		# Accept an incoming connection
		connection, client_address = msg_socket.accept()
		# Receive the data
		data_list = []
		data = connection.recv(network_params.BUFFER_SIZE)
		while data:
		    data_list.append(data)
		    data = connection.recv(network_params.BUFFER_SIZE)
		data = b''.join(data_list)

		msg = pickle.loads(data)
		assert isinstance(
		    msg, message.Message), "Received object on socket not of type " \
		                           "Message."

		if msg.msg_type == 'LEADER_ELECT':
		    LEADER_ID,LEADER_IP,parent_ip,leader_elect_acks = message_handlers.leader_elect_handler(
		                                                                          neighbour_file=neighbourfile,
		                                                                          received_msg = msg,
		                                                                          selfip = selfip,
		                                                                          selfid = selfid,
		                                                                          leader_ip = LEADER_IP,
		                                                                          leader_id = LEADER_ID,
		                                                                          parent_ip = parent_ip,
		                                                                          leader_elect_acks = leader_elect_acks)
		    if leader_elect_acks != len(neighbourlist):
		        LEADER_FIXED = False
		    
		elif msg.msg_type == 'LEADER_ELECT_ACK':            
		    leader_elect_acks,LEADER_FIXED = message_handlers.leader_elect_ack_handler(
		                                                                  no_of_neighbours=len(neighbourlist),
		                                                                  leader_elect_acks = leader_elect_acks,
	                                                                          parent_ip = parent_ip)

if __name__ == '__main__':
    main() 




		






