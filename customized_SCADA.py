import siemens
import time
from multiprocessing import Process
from sys import exit
import numpy as np
from scipy.io import savemat
from datetime import datetime

import matplotlib.pyplot as plt

def readVars(plc, vars_index_dict):
	data_dict = plc.plc_read_data(vars_index_dict["I"], vars_index_dict["Q"], vars_index_dict["DB"])
	return data_dict

# def writeVars(plc) :
# 	# some_params_you_may_need:
# 	# for any block, format is [db_num, start_byte, data], data must be bytearray
# 	# the format of writing a data to PLC: [0, 110, 10000] --- "0" is default 0 for I/Q; 
# 	# "100" is the offset of address; 10000 is the writing data 
# 	write_vars_dict = {"I":[[0, 110, 0]], "Q":[[0, 100, 0]], "DB":[]}

# 	# YOUR LOGIC HERE -- determine the write target and the write value in write_vars_dict

# 	plc.plc_write_data(write_vars_dict["I"], write_vars_dict["Q"], write_vars_dict["DB"])
# 	return write_vars_dict


# def generateTimeInterval():
# 	interval = 0.5

# 	# YOUR LOGIC HERE -- determine the time interval

# 	return interval


def customized_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, initialzation = False) :
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
	condensing_paras = [1, 1, 0.9273, 0.4388, 0.0002] 
	feeding_paras = [1.0021, 1, 72.1622, 36.1825, 0.000018225]

	if initialzation:
		flow_x_pre = (cooling_valve - condensing_paras[3]*flow_error) / condensing_paras[2]
		flow_x_est = flow_x_pre
		feeding_x_pre = (material_valve - feeding_paras[3]*level_error ) / feeding_paras[2]
		feeding_x_est = (feeding_x_pre)

	# predict command, update the innvation for condensing loop 
	flow_estimation = online_state_estimation(condensing_paras, cooling_valve, flow_error, flow_x_pre, flow_x_est) 
	# [flow_innovation, flow_command_pre, flow_x_pre, flow_x_est]
	flow_estimation = list(flow_estimation)
	flow_estimation.append(cooling_valve) 
	flow_estimation.append(cooling_flow)

	# predict command, update the innvation for material feeding loop 
	level_estimation = online_state_estimation(feeding_paras, material_valve, level_error, feeding_x_pre, feeding_x_est) 
	# [level_innovation, level_command_pre, feeding_x_pre, feeding_x_est]
	level_estimation = list(level_estimation)
	level_estimation.append(material_valve) 
	level_estimation.append(liquid_level)

	return flow_estimation, level_estimation



def online_state_estimation(loop_paras, u_read, e_read, x_pre, x_est) :
	# predict control command "u_pre",  the estimation innvation "z"
	# based on the customized_SCADA reading 

	# controller parameters 
	A = loop_paras[0]
	B = loop_paras[1]
	C = loop_paras[2]
	D = loop_paras[3]

	# predict the control command 
	u_pre = C * x_pre + D * e_read

	# calculate the innovation, and update the state estimation 
	if u_pre < 5.03:
		u_pre = 5.03
		innovation = u_read - u_pre
		x_pre =  A * x_est + B * e_read 
	elif u_pre > 95:
		u_pre = 95
		innovation = u_read - u_pre
		x_pre =  A * x_est + B * e_read 
	else:
		innovation = u_read - u_pre
		x_est = x_pre + 1/C * innovation 
		x_pre =  A * x_est + B * e_read 


	return innovation, u_pre, x_pre, x_est






if __name__ == '__main__':
	# setup for connection
	# plc = siemens.SIEMENSPLC("192.168.0.2", "elevator")
	plc = siemens.SIEMENSPLC("192.168.10.222", "distillation tower")
	plc.plc_connect()
	if not plc.check_connection:
		print('\nERROR with connection')
		exit()

	# Loop-1 Temperature control: IW108 is for the "heater temp.", Q1.2 is for the "heater switch"
	# Loop-2 Gas condensing control: IW94 is for the "cooling water flow", IW110 is for the "tower liquid level", 
	# Loop-3 Tower liquid level control: QW74 is for the "cooling water valve", QW70 is for the "material input valve", 

	# for any block, format is [db_num, start_byte, size_of_bytes], e.g., "Q":[[0, 0, 1], [0, 2, 1]] reads the first and third byte of Q 
	read_vars_dict = {"I":[[0, 94, 2], [0, 110, 2]], "Q":[[0, 74, 2], [0, 70, 2],[0, 76, 2]], "DB":[[10, 2, 4], [13, 2, 4], [10, 30, 4], [13, 30, 4]]}
	initialize = True
	sensor_SCADA_logged = []
	command_SCADA_logged = []
	command_SCADA_predicted = []
	prediction_error_SCADA = []
	command_System_expected = []
	while (True):
		try:
			# read vars
			read_vars_value_dict = readVars(plc, read_vars_dict)

			expected_flow_u = read_vars_value_dict["Q"][2][0] 
			# expected_level_u = read_vars_value_dict["DB"][3][0] 

			# print(read_vars_value_dict)
			# # YOUR LOGIC HERE -- anything helpful
			if initialize:
				flow_x_pre = 0
				flow_x_est = 0 
				feeding_x_pre = 0 
				feeding_x_est = 0
				[flow_estimation, level_estimation] = customized_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, initialzation = True)
				[flow_innovation, flow_command_pre, flow_x_pre, flow_x_est, flow_command_log, flow_sensor] = flow_estimation 
				[level_innovation, level_command_pre, feeding_x_pre, feeding_x_est, level_command_log, level_sensor] = level_estimation

				initialize=False
			else:
				
				[flow_estimation, level_estimation] = customized_SCADA(read_vars_value_dict,  flow_x_pre, flow_x_est, feeding_x_pre, feeding_x_est, initialzation = False)
				[flow_innovation, flow_command_pre, flow_x_pre, flow_x_est, flow_command_log, flow_sensor] = flow_estimation 
				[level_innovation, level_command_pre, feeding_x_pre, feeding_x_est, level_command_log, level_sensor] = level_estimation
			
			print("the logged cooling flow is: {}".format(flow_sensor))
			sensor_SCADA_logged.append(flow_sensor)
			print("the logged cooling command is: {}".format(flow_command_log))
			command_SCADA_logged.append(flow_command_log)
			print("the predicted cooling command is: {}".format(flow_command_pre))
			command_SCADA_predicted.append(flow_command_pre)
			print("the command prediction error is: {}".format(flow_innovation))
			prediction_error_SCADA.append(flow_innovation)
			print("the normal PLC cooling command is: {}% \n".format(expected_flow_u/27648*100)) 
			command_System_expected.append(expected_flow_u/27648*100)
			

			# # time_interval = generateTimeInterval() # in secs (float)
			# time.sleep(0.5)  # in secs (float)

			# the force interval is 0.5s
			time_now = time.time()
			while(time.time() - time_now < 1.0):
				time.sleep(0.001)

		except KeyboardInterrupt as e:
			print('\nKeyboardInterrupt')

			SCADA_detection = {"sensor_SCADA_logged": np.array(sensor_SCADA_logged), 
			"command_SCADA_logged":np.array(command_SCADA_logged),
			"command_SCADA_predicted":np.array(command_SCADA_predicted), 
			"prediction_error_SCADA":np.array(prediction_error_SCADA),
			"command_System_expected":np.array(command_System_expected)}
			plt.plot(prediction_error_SCADA)
			plt.show()

			savemat(".\SCADAdetection\SCADA_detection" + str(datetime.now().strftime("-%y-%m-%d-%H-%M-%S")) + ".mat", SCADA_detection)
			print('\nDetection data saved!')

			plc.plc_disconnect()
			exit()
			

