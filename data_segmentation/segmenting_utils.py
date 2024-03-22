
from math import log
import numpy as np
import struct,pickle

from scipy.io import loadmat
import math
from utils import *

from scipy.io import savemat
import scipy.stats





def identify_boundary_MSB(signal_entropy, alpha, signal_size, PII = False):

    least_bits_boundaries = []
    most_bits_boundaries = []
    Act_least_bits_boundaries = []

    # alpha = 0.5
    if PII:
        mu = [0, 1, 2, 3, 4, 5, 6]
    else:
        mu = [0]

    memory_len = int(signal_entropy.size/8)
    for i in range(1, memory_len+1):

        for mu_id in range(len(mu)):

            if i < memory_len:
                most_bit_entroy = signal_entropy[0][8 * i]
                least_bit_entroy = signal_entropy[0][8 * i - 1 - mu[mu_id]]
            else:
                most_bit_entroy = 0
                least_bit_entroy = signal_entropy[0][8 * i - 1 - mu[mu_id]]

            if least_bit_entroy - most_bit_entroy > alpha:
                least_bits_boundaries.append(8 * i - 1)
                Act_least_bits_boundaries.append(8 * i - 1 - mu[mu_id])
                most_bits_boundaries.append(8 * (i - signal_size))

                break

    return least_bits_boundaries, most_bits_boundaries, Act_least_bits_boundaries



def identify_boundary_LSB(signal_entropy, alpha, signal_size, PII = False):

    least_bits_boundaries = []
    most_bits_boundaries = []
    Act_least_bits_boundaries = []

    # alpha is a testing metric
    # alpha = 0.5
    if PII:
        mu = [0, 1, 2, 3, 4, 5, 6]
    else:
        mu = [0]

    memory_len = int(signal_entropy.size/8)

    for i in range(0, memory_len):

        for mu_id in range(len(mu)):
            if i == 0:
                most_bit_entroy = 0
                least_bit_entroy = signal_entropy[0][8 * i + mu[mu_id]]
            else:
                most_bit_entroy = signal_entropy[0][8 * i - 1]
                least_bit_entroy = signal_entropy[0][8 * i + mu[mu_id]]

            if least_bit_entroy - most_bit_entroy > alpha:
                least_bits_boundaries.append(8 * i)
                Act_least_bits_boundaries.append(8 * i + mu[mu_id])
                most_bits_boundaries.append(8 * (i+signal_size)-1)

                break

    return least_bits_boundaries, most_bits_boundaries, Act_least_bits_boundaries





def boundary_verification_MSB(signal_entropy, least_bits, most_bits, Act_least_bits, threshold_beta):

    verified_least_bits = []
    verified_most_bits = []
    conflicting_nodes = []
    num_signals = len(least_bits)

    for sig_id in range(num_signals):
        if sig_id in conflicting_nodes:
            continue
        sig_start = most_bits[sig_id]
        sig_end_whole = least_bits[sig_id]

        sig_end = Act_least_bits[sig_id]
        # if sig_end != sig_end_whole:
        if sig_end+1 < signal_entropy.shape[1]:
            while (signal_entropy[0][sig_end+1] != 0) & (sig_end<sig_end_whole):
                sig_end = sig_end+1
                if sig_end+1 >= signal_entropy.shape[1]:
                    break


        checking_entropy = signal_entropy[0][sig_start: (sig_end + 1)]

        signals_conflicting = False
        if 0:
        # if sig_id < num_signals-1:
            bit_range_A = range(sig_start, sig_end_whole+1)
            bit_range_B = range(most_bits[sig_id+1], least_bits[sig_id+1]+1)
            cross_check = set(bit_range_A).intersection(set(bit_range_B))
            if cross_check:
                sig_start_B = most_bits[sig_id + 1]
                sig_end_B = Act_least_bits[sig_id + 1]
                checking_entropy_B = signal_entropy[0][sig_start_B: (sig_end_B + 1)]
                if sum(checking_entropy) < sum(checking_entropy_B):
                    signals_conflicting = True
                else:
                    # remove the latter one
                    conflicting_nodes.append(sig_id+1)

        # if not signals_conflicting:
        if 1:
            checking_entropy = signal_entropy[0][sig_start: (sig_end + 1)]
            diff_checking_entropy = np.subtract(checking_entropy[1:len(checking_entropy)], checking_entropy[0:len(checking_entropy) - 1])
            if not (len(diff_checking_entropy) == 0):
                the_smallest_ascending = min(diff_checking_entropy)

                if the_smallest_ascending > threshold_beta:
                    verified_least_bits.append(least_bits[sig_id])
                    verified_most_bits.append(most_bits[sig_id])

    return verified_least_bits, verified_most_bits



def boundary_verification_LSB(signal_entropy, least_bits, most_bits, Act_least_bits, threshold_beta):
    verified_least_bits = []
    verified_most_bits = []
    conflicting_nodes = []

    num_signals = len(least_bits)
    for sig_id in range(num_signals):
        if sig_id in conflicting_nodes:
            continue
        sig_start_whole = least_bits[sig_id]
        sig_start = Act_least_bits[sig_id]
        sig_end = most_bits[sig_id]
        checking_entropy = signal_entropy[0][sig_start: (sig_end + 1)]

        # signals_conflicting = False
        if 0:
        # if sig_id < num_signals-1:
            bit_range_A = range(sig_start_whole, sig_end+1)
            bit_range_B = range(least_bits[sig_id+1], most_bits[sig_id+1]+1)
            cross_check = set(bit_range_A).intersection(set(bit_range_B))
            if cross_check:
                sig_start_B = Act_least_bits[sig_id + 1]
                sig_end_B = most_bits[sig_id + 1]
                checking_entropy_B = signal_entropy[0][sig_start_B: (sig_end_B + 1)]
                if sum(checking_entropy) < sum(checking_entropy_B):
                    signals_conflicting = True
                else:
                    # remove the latter one
                    conflicting_nodes.append(sig_id + 1)

        if not 0:
        # if not signals_conflicting:
            diff_checking_entropy = np.subtract(checking_entropy[1:len(checking_entropy)], checking_entropy[0:len(checking_entropy) - 1])
            the_smallest_descending = max(diff_checking_entropy)
            if the_smallest_descending < (-threshold_beta):
                verified_least_bits.append(least_bits[sig_id])
                verified_most_bits.append(most_bits[sig_id])

    return verified_least_bits, verified_most_bits





def items_concatenation(PLChexs):

    itemskeys = list(PLChexs.keys())
    hex_example = PLChexs[itemskeys[0]]
    num_row, num_col = hex_example.shape
    item_hexs_total = np.zeros((num_row, 0))

    for item_id in PLChexs.keys():
        item_hexs = PLChexs[item_id]
        item_hexs_total = np.concatenate([item_hexs_total, item_hexs], axis=1)

    return item_hexs_total





def signals_translation(PLC_values, signal_starting_bits, signal_size, bigendain=True):
    num_row, num_col = PLC_values.shape
    tranlated_value = np.zeros((num_row, len(signal_starting_bits)))

    for i in range(len(signal_starting_bits)):
        signals_start = int(signal_starting_bits[i]/8)
        item_hexs_sample = PLC_values[0:, signals_start: signals_start + signal_size]
        item_real_sample = np.zeros([num_row, 1])

        for j in range(item_hexs_sample.shape[0]):
            hex_num = ''.join(item_hexs_sample[j])
            if signal_size == 2:
                if bigendain:
                    item_real_sample[j] = hex2int_big(hex_num)
                else:
                    item_real_sample[j] = hex2int_little(hex_num)
            elif signal_size == 4:
                if bigendain:
                    item_real_sample[j] = hex2float_big(hex_num)
                else:
                    item_real_sample[j] = hex2float_little(hex_num)

        tranlated_value[0:, i] = item_real_sample[0:, 0]

    return tranlated_value

def signals_correlation(PIIO_value, SCADA_tranlated_value):
    correlations = np.zeros((SCADA_tranlated_value.shape[1], PIIO_value.shape[1]))
    max_corr = np.zeros((1, PIIO_value.shape[1]))
    for j in range(PIIO_value.shape[1]):
        IO_value = PIIO_value[0:, j]
        for i in range(SCADA_tranlated_value.shape[1]):
            SCADA_value = SCADA_tranlated_value[0:, i]
            # MM = np.correlate(SCADA_value, IO_value)
            if not (np.isnan(SCADA_value).any() | np.isinf(SCADA_value).any()):
                correlations[i,j] = scipy.stats.pearsonr(SCADA_value, IO_value)[0]
            else:
                correlations[i,j] = 0
        if len(correlations[0:, j]) ==0:
            max_corr[0, j] = 0
        else:
            max_corr[0, j] = max(correlations[0:, j])


    if len(max_corr[0])==0:
        max_max_coor = 0
    else:
        max_max_coor = sum(max_corr[0]) / len(max_corr[0])

    return max_max_coor, correlations


def mat_saving(variables, filename):
    saving_variable = {}

    for i in range(len(variables)):
        saving_variable[""] = variables[i]
    savemat("./Matlab_data/" + filename, saving_variable)


def address_generation(verified_start_bits, PII=False, PIO=False, SCADA=False):
    memory_address = []
    memory_address_pure = []
    for i in range(len(verified_start_bits)):
        if PII:
            address_sample = "I({},2)".format(int(verified_start_bits[i] / 8))
            memory_address.append(address_sample)
            # print("signals in PII exist in {}".format(memory_address))
        elif PIO:
            address_sample = "O({},2)".format(int(verified_start_bits[i] / 8))
            memory_address.append(address_sample)
            # print("signals in PIO exist in {}".format(memory_address))
        elif SCADA:
            address_sample = "D({},4)".format(int(verified_start_bits[i] / 8))
            memory_address.append(address_sample)
            # print("signals in SCADA exist in {}".format(memory_address))
        
        memory_address_pure.append(int(verified_start_bits[i] / 8))
    print("signals exist in {}".format(memory_address))
    

    return memory_address, memory_address_pure



def performence_analysis(PII_address, PIO_address, SCADA_address):
    PII_address_ground = [88, 90, 92, 94, 96, 98, 100, 102, 104, 108, 110]
    PIO_address_ground = [70, 74]
    SCADA_address_ground = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 72, 108]
    # verify the PII signals
    correct_counts = 0
    for i in range(len(PII_address)):
        if PII_address[i] in PII_address_ground:
            correct_counts = correct_counts + 1
    # verify the PIO signals
    for i in range(len(PIO_address)):
        if PIO_address[i] in PIO_address_ground:
            correct_counts = correct_counts + 1
    # verify the SCADA signals
    for i in range(len(SCADA_address)):
        if SCADA_address[i] in SCADA_address_ground:
            correct_counts = correct_counts + 1

    if (len(PII_address) + len(PIO_address) + len(SCADA_address)) == 0:
        precision = 0
    else:
        precision = correct_counts / (len(PII_address) + len(PIO_address) + len(SCADA_address))
    recall = correct_counts / (len(PII_address_ground) + len(PIO_address_ground) + len(SCADA_address_ground))

    return precision, recall



def cyclic_procedures(PII_values, PIO_values, SCADA_values, alpha, threshold_beta):

    # for the MSB0 entropy series
    
    filename_BE = "comm_wincc_snap_20211116_MSB0_1.mat"
    # filename_BE = "comm_wincc_snap_20211223_MSB0_1.mat"
    
    data = loadmat("./comm-Yang/" + filename_BE)
    H_PII = data["I_1"]
    H_PIO = data["Q_1"]
    H_SCADA = np.hstack((data["SCADA_1"], data["SCADA_2"], data["SCADA_3"], data["SCADA_4"], data["SCADA_5"]))
    H_PII[0, 848:863] = 0
    H_PII[0, 896:] = 0
    H_PIO[0, 608:] = 0
    H_SCADA[0, 352:383] = 0

    # obtain the boundaries of signals in PII table
    PII_least_bits_MSB, PII_most_bits_MSB, Act_PII_least_bits_MSB = identify_boundary_MSB(H_PII, alpha, signal_size=2, PII=True)
    # obtain the boundaries of signals in PIO table
    PIO_least_bits_MSB, PIO_most_bits_MSB, Act_PIO_least_bits_MSB = identify_boundary_MSB(H_PIO, alpha, signal_size=2, PII=False)
    # obtain the boundaries of signals in SCADA traffic
    SCADA_least_bits_MSB, SCADA_most_bits_MSB, Act_SCADA_least_bits_MSB = identify_boundary_MSB(H_SCADA, alpha, signal_size=4, PII=True)
    # print("boundaries identified for MSB0\n")

    # continue for the Signal Plausibility verification
    verified_PII_least_bits_MSB, verified_PII_most_bits_MSB = boundary_verification_MSB(H_PII, PII_least_bits_MSB, PII_most_bits_MSB,  Act_PII_least_bits_MSB,  threshold_beta)
    verified_PIO_least_bits_MSB, verified_PIO_most_bits_MSB = boundary_verification_MSB(H_PIO, PIO_least_bits_MSB, PIO_most_bits_MSB,  Act_PIO_least_bits_MSB, threshold_beta)
    verified_SCADA_least_bits_MSB, verified_SCADA_most_bits_MSB = boundary_verification_MSB(H_SCADA, SCADA_least_bits_MSB, SCADA_most_bits_MSB, Act_SCADA_least_bits_MSB, threshold_beta)
    # print("boundaries verified for MSB0\n")

    # memory address allocation
    PII_memory_address_BE, PII_memory_address_BE_pure = address_generation(verified_PII_most_bits_MSB, PII=True)
    PIO_memory_address_BE, PIO_memory_address_BE_pure = address_generation(verified_PIO_most_bits_MSB, PIO=True)
    SCADA_memory_address_BE, SCADA_memory_address_BE_pure = address_generation(verified_SCADA_most_bits_MSB, SCADA=True)

    # tranlate the hex value to physical value
    PII_tranlated_value_BE = signals_translation(PII_values, verified_PII_most_bits_MSB, signal_size=2, bigendain=True)
    PIO_tranlated_value_BE = signals_translation(PIO_values, verified_PIO_most_bits_MSB, signal_size=2, bigendain=True)
    SCADA_tranlated_value_BE = signals_translation(SCADA_values, verified_SCADA_most_bits_MSB, signal_size=4, bigendain=True)
    # print("signals value translated finished for Big-Endian\n")

    # verify the correlation between PII/PIO values and SCADA values for the Big-Endian
    PIIO_value_BE = np.concatenate([PII_tranlated_value_BE, PIO_tranlated_value_BE], axis=1)
    max_max_coor_BE, correlations_BE = signals_correlation(PIIO_value_BE, SCADA_tranlated_value_BE)

    # # show the correlation heatmap
    # PIIO_address_BE = PII_memory_address_BE + PIO_memory_address_BE
    # correlation_heatmap_analysis(correlations_BE, tuple(SCADA_memory_address_BE), tuple(PIIO_address_BE))

    precision_BE, recall_BE = performence_analysis(PII_memory_address_BE_pure, PIO_memory_address_BE_pure, SCADA_memory_address_BE_pure)


    
    # for the LSB0 entropy series
    filename_LE = "comm_wincc_snap_20211116_MSB0_0.mat"
    
    
    data = loadmat("./comm-Yang/" + filename_LE)
    H_PII = data["I_1"]
    H_PIO = data["Q_1"]
    H_SCADA = np.hstack((data["SCADA_1"], data["SCADA_2"], data["SCADA_3"], data["SCADA_4"], data["SCADA_5"]))
    H_PII[0, 848:863] = 0
    H_PII[0, 896:] = 0
    H_PIO[0, 608:] = 0
    H_SCADA[0, 352:383] = 0

    # obtain the boundaries of signals in PII table
    PII_least_bits_LSB, PII_most_bits_LSB, Act_PII_least_bits_LSB = identify_boundary_LSB(H_PII, alpha, signal_size=2,  PII=True)
    # obtain the boundaries of signals in PIO table
    PIO_least_bits_LSB, PIO_most_bits_LSB, Act_PIO_least_bits_LSB = identify_boundary_LSB(H_PIO, alpha, signal_size=2, PII=False)
    # obtain the boundaries of signals in SCADA traffic
    SCADA_least_bits_LSB, SCADA_most_bits_LSB, Act_SCADA_least_bits_LSB = identify_boundary_LSB(H_SCADA, alpha, signal_size=4, PII=True)
    # print("boundaries identified for LSB)\n")

    # continue for the Signal Plausibility verification
    verified_PII_least_bits_LSB, verified_PII_most_bits_LSB = boundary_verification_LSB(H_PII, PII_least_bits_LSB, PII_most_bits_LSB, Act_PII_least_bits_LSB, threshold_beta)
    verified_PIO_least_bits_LSB, verified_PIO_most_bits_LSB = boundary_verification_LSB(H_PIO, PIO_least_bits_LSB, PIO_most_bits_LSB, Act_PIO_least_bits_LSB, threshold_beta)
    verified_SCADA_least_bits_LSB, verified_SCADA_most_bits_LSB = boundary_verification_LSB(H_SCADA, SCADA_least_bits_LSB, SCADA_most_bits_LSB, Act_SCADA_least_bits_LSB, threshold_beta)
    # print("boundaries verified for LSB0\n")

    # memory address allocation
    PII_memory_address_LE, PII_memory_address_LE_pure = address_generation(verified_PII_least_bits_LSB, PII=True)
    PIO_memory_address_LE, PIO_memory_address_LE_pure = address_generation(verified_PIO_least_bits_LSB, PIO=True)
    SCADA_memory_address_LE, SCADA_memory_address_LE_pure = address_generation(verified_SCADA_least_bits_LSB,  SCADA=True)

    # tranlate the hex value to physical value
    PII_tranlated_value_LE = signals_translation(PII_values, verified_PII_least_bits_LSB, signal_size=2, bigendain=False)
    PIO_tranlated_value_LE = signals_translation(PIO_values, verified_PIO_least_bits_LSB, signal_size=2, bigendain=False)
    SCADA_tranlated_value_LE = signals_translation(SCADA_values, verified_SCADA_least_bits_LSB, signal_size=4, bigendain=False)
    # print("signals value translated finished for Little-Endian\n")

    # verify the correlation between PII/PIO values and SCADA values for the Little-Endian
    PIIO_value_LE = np.concatenate([PII_tranlated_value_LE, PIO_tranlated_value_LE], axis=1)
    max_max_coor_LE, correlations_LE = signals_correlation(PIIO_value_LE, SCADA_tranlated_value_LE)

    

    precision_LE, recall_LE = performence_analysis(PII_memory_address_LE_pure, PIO_memory_address_LE_pure, SCADA_memory_address_LE_pure)

    PLC_data_real = {}
    if max_max_coor_BE >= max_max_coor_LE:
        PLC_data_real["SCADA_real"] = SCADA_tranlated_value_BE
        PLC_data_real["PIIO_real"] = PIIO_value_BE
    else:
        PLC_data_real["SCADA_real"] = SCADA_tranlated_value_LE
        PLC_data_real["PIIO_real"] = PIIO_value_LE
        
    savemat("./comm-Yang/PLCRealState.mat", PLC_data_real)


    return max_max_coor_BE, precision_BE, recall_BE, max_max_coor_LE, precision_LE, recall_LE



if __name__ == '__main__':

    # generate the translated signal values
    storepath = "./comm-Yang/"
    

    PLChexs_I = pickle.load(open(storepath + "comm_wincc_snap_20211116_SnapI_hex_MSB0_1.pickle", "rb"))
    PLChexs_Q = pickle.load(open(storepath + "comm_wincc_snap_20211116_SnapQ_hex_MSB0_1.pickle", "rb"))
    PLChexs_SCADA = pickle.load(open(storepath + "comm_wincc_snap_20211116_SCADA_hex_MSB0_1.pickle", "rb"))


    # concatenate items in network traffic
    PII_values = items_concatenation(PLChexs_I)
    PIO_values = items_concatenation(PLChexs_Q)
    SCADA_values = items_concatenation(PLChexs_SCADA)


    # the larger alpha, the higher recall
    # all alpha_list < 1, is because the entropy of the least bit of a signal is smaller than 1
    alpha_list = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # alpha_list = [0.3] # the parameter that achieve 100% precision and 100% recall
    
    
    # the smaller beta, the higher recall (TP/PP)
    # all beta_list < 0, is because of the measurement system noise
    beta_list = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1]
    # beta_list = [-0.7] # the parameter that achieve 100% precision and 100% recall
    
    


    Precision_Matrix = np.zeros((len(alpha_list), len(beta_list)))
    Recall_Matrix = np.zeros((len(alpha_list), len(beta_list)))

    for i in range(len(alpha_list)):
        alpha = alpha_list[i]

        for j in range(len(beta_list)):
            beta = beta_list[j]
            print("threshold alpha = {}".format(alpha))
            print("threshold beta = {}".format(beta))
            max_max_coor_BE, precision_BE, recall_BE, max_max_coor_LE, precision_LE, recall_LE = cyclic_procedures(PII_values, PIO_values, SCADA_values, alpha, beta)

            if max_max_coor_BE >= max_max_coor_LE:
                # analysis the identification accuracy
                precision = precision_BE
                recall = recall_BE
                print("The averaged correlation between values of PII/PIO and SCADA in Big-Endian order is {}".format(max_max_coor_BE))
                print("The averaged correlation between values of PII/PIO and SCADA in Little-Endian order is {}".format(max_max_coor_LE))
                print("The PLC has the Big-Endian byte order! \n")
                print("The identification Precision is {}".format(precision))
                print("The identification Recall is {}".format(recall))
            else:
                precision = 0
                recall = 0
                print("The averaged correlation between values of PII/PIO and SCADA in Big-Endian order is {}".format(max_max_coor_BE))
                print("The averaged correlation between values of PII/PIO and SCADA in Little-Endian order is {}".format(max_max_coor_LE))
                print("The PLC has the Little-Endian byte order! \n")
                print("The identification Precision is {}".format(precision))
                print("The identification Recall is {}".format(recall))

            Precision_Matrix[i, j] = precision
            Recall_Matrix[i, j] = recall
        print("wait")

    # correlation_heatmap_analysis(Precision_Matrix, tuple(alpha_list), tuple(beta_list), saving_name="/Users/magnolia/Library/CloudStorage/Dropbox/Zeyu/PLCSage/figures/M_Sig_Iden_Precision", xlabel_name="beta", ylabel_name="alpha")
    # correlation_heatmap_analysis(Recall_Matrix, tuple(alpha_list), tuple(beta_list), saving_name="/Users/magnolia/Library/CloudStorage/Dropbox/Zeyu/PLCSage/figures/M_Sig_Iden_Recall", xlabel_name="beta", ylabel_name="alpha")
    print("analysis of signals segmentation is finished!")

    identification_accurate = {}
    identification_accurate["Precision_Matrix"] = Precision_Matrix
    identification_accurate["Recall_Matrix"] = Recall_Matrix
    identification_accurate["alpha_list"] = np.array(alpha_list)
    identification_accurate["beta_list"] = np.array(beta_list)
