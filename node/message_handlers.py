import copy
import multiprocessing as mp
import time
from ..messages import message
from ..messages import messageutils
from .__main__ import elect_leader


def leader_elect_handler(neighbour_file,
						 received_msg,
						 selfip,
						 selfid,
						 leader_ip,
						 leader_id,
						 parent_ip,
						 leader_elect_acks
						 ):
	content = received_msg.content
	msg_leaderid = content['leader_id']
	msg_leaderip = content['leader_ip']
	msg_senderip = content['sender_ip']

	if leader_id == -1:
		#It hasn't started leader election so start it.
		leader_id = selfid
		leader_ip = selfip
		parent_ip = selfip
		elect_leader(neighbour_file,selfid,selfip)

	elif leader_id == msg_leaderid:
		#send negative ack indicating it already has parent
		messageutils.make_and_send_message(
	                msg_type='LEADER_ELECT_ACK',
	                content=None,
	                file_path=None,
	                to=msg_senderip,
	                msg_socket=None,
	                port=network_params.CLIENT_SEND_PORT)
		
	elif leader_id < msg_leaderid:
		#some node is misinterpreting the leader
		content = {"leader_id":leader_id,"leader_ip":leader_ip,"sender_ip":selfip}
		messageutils.make_and_send_message(
                msg_type='LEADER_ELECT',
                content=content,
                file_path=None,
                to=msg_senderip,
                msg_socket=None,
                port=network_params.CLIENT_SEND_PORT)
	else:
		#This node should change its leader
		leader_id = msg_leaderid
		leader_ip = msg_leaderip
		leader_elect_acks = 0
		#sending new leader info to its current parent
		if parent_ip!=selfip:
			content = {"leader_id":leader_id,"leader_ip":leader_ip,"sender_ip":selfip}
			messageutils.make_and_send_message(
	                msg_type='LEADER_ELECT',
	                content=content,
	                file_path=None,
	                to=parent_ip,
	                msg_socket=None,
	                port=network_params.CLIENT_SEND_PORT)

		parent_ip = msg_senderip

		#sending new leader info to its neighbours
		neighbour_list = parse_neighbour_file(neighbour_file)
		for ip in neighbour_list:
			messageutils.make_and_send_message(
			        msg_type='LEADER_ELECT',
			        content=content,
			        file_path=None,
			        to=ip,
			        msg_socket=None,
			        port=network_params.CLIENT_SEND_PORT)

	return leader_id,leader_ip,parent_ip,leader_elect_acks


def leader_elect_ack_handler(
							  no_of_neighbours,
							  leader_elect_acks,
							  parent_ip
							 ):
	leader_elect_acks += 1 
	leader_election_done = False
	if leader_elect_acks==no_of_neighbours :
		#send ack to parent node to denote completion of leader
		#election of its subtree
		messageutils.make_and_send_message(
	                msg_type='LEADER_ELECT_ACK',
	                content=None,
	                file_path=None,
	                to=parent_ip,
	                msg_socket=None,
	                port=network_params.CLIENT_SEND_PORT)

		leader_election_done = True

	return leader_elect_acks,leader_election_done


                                                                          


		
