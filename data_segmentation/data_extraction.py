import numpy as np
import os, json, pickle
import re

from utils import *
import matplotlib.pyplot as plt

from scipy.io import savemat


def my_obj_pairs_hook(lst):
    # if the .json file has replicated keys, this my_obj_pairs_hook will substitute them
    result = {}
    count = {}
    for key, val in lst:
        if key in count:
            count[key] = 1 + count[key]
        else:
            count[key] = 1
        if key in result:
            if count[key] > 2:
                # change the name of key, and add the result
                # result[key].append(val)
                keyname = key + str(count[key])
                result[keyname] = val
            else:
                keyname = key + str(count[key])
                result[keyname] = val
        else:
            result[key] = val
    return result

def packet_reading(filepath):
    with open(filepath, 'r') as json_file:
        data = json_file.read()
        result = json.loads(data, object_pairs_hook=my_obj_pairs_hook)
    return result



def datasets_construction(packets_dict):
    # obtain the data field from the communication packets, which is organized as:
    # BytesData (dict) --> data_item (list) --> value_of_instant (str)

    PLCBytedata_SCADA = {}
    PLCBytedata_I = {}
    PLCBytedata_Q = {}
    recorded_num = 0

    for p_id in range(len(packets_dict)):

        s7headers = packets_dict[p_id]['_source']['layers']['s7comm']['s7comm.header']

        # "rosctr" == "3" means Ack_Data
        if s7headers["s7comm.header.rosctr"] == "3":
            s7items = packets_dict[p_id]['_source']['layers']['s7comm']['s7comm.data']

            if s7headers["s7comm.header.datlg"] == "124":
                recorded_num = 1
                # I address value: customized
                item_id = 1
                for key_id in s7items:
                    key_matchObj = re.match('s7comm.data.item', key_id)
                    if key_matchObj:
                        rawdata = s7items[key_id]['s7comm.resp.data']
                        rawdata = re.sub(r':', "", rawdata)
                        if str(item_id) in PLCBytedata_I.keys():
                            PLCdata = PLCBytedata_I[str(item_id)]
                            PLCdata.append(rawdata)
                            PLCBytedata_I[str(item_id)] = PLCdata
                            item_id = item_id + 1
                        else:
                            PLCdata = []
                            PLCdata.append(rawdata)
                            PLCBytedata_I[str(item_id)] = PLCdata
                            item_id = item_id + 1


            elif s7headers["s7comm.header.datlg"] == "86":
                recorded_num = recorded_num + 1
                # Q address value: customized
                item_id = 1
                for key_id in s7items:
                    key_matchObj = re.match('s7comm.data.item', key_id)
                    if key_matchObj:
                        rawdata = s7items[key_id]['s7comm.resp.data']
                        rawdata = re.sub(r':', "", rawdata)
                        if str(item_id) in PLCBytedata_Q.keys():
                            PLCdata = PLCBytedata_Q[str(item_id)]
                            PLCdata.append(rawdata)
                            PLCBytedata_Q[str(item_id)] = PLCdata
                            item_id = item_id + 1
                        else:
                            PLCdata = []
                            PLCdata.append(rawdata)
                            PLCBytedata_Q[str(item_id)] = PLCdata
                            item_id = item_id + 1


        # "rosctr" == "7" means userdata
        elif s7headers["s7comm.header.rosctr"] == "7":
            if recorded_num == 2:
                recorded_num = 0
                s7params = packets_dict[p_id]['_source']['layers']['s7comm']['s7comm.param']
                # "s7comm.param.userdata.seq_num" == "12": the data the was logged by WinCC database
                if s7params["s7comm.param.userdata.seq_num"] == "2":
                    s7items = packets_dict[p_id]['_source']['layers']['s7comm']['s7comm.data']
                    item_id = 1
                    for key_id in s7items:
                        key_matchObj = re.match('s7comm.data.item', key_id)
                        if key_matchObj:
                            rawdata = s7items[key_id]['s7comm.resp.data']
                            rawdata = re.sub(r':', "", rawdata)
                            if str(item_id) in PLCBytedata_SCADA.keys():
                                PLCdata = PLCBytedata_SCADA[str(item_id)]
                                PLCdata.append(rawdata)
                                PLCBytedata_SCADA[str(item_id)] = PLCdata
                                item_id = item_id + 1
                            else:
                                PLCdata = []
                                PLCdata.append(rawdata)
                                PLCBytedata_SCADA[str(item_id)] = PLCdata
                                item_id = item_id + 1

            else:
                print("Snap7 not recoreded yet!")
        else:
            print("No data was transported!")
    if len(PLCBytedata_I["1"]) > len(PLCBytedata_Q["1"]):
        PLCBytedata_I["1"] = PLCBytedata_I["1"][0:-1]



    return PLCBytedata_SCADA, PLCBytedata_I, PLCBytedata_Q




def binaries_construction(PLCdata_dict, LSB=False):
    # try binary to classify the data

    PLChexs = {}
    PLCbins = {}
    # PLCints = {}

    for item_id in PLCdata_dict.keys():
        if item_id == "6" or item_id == "7":
            continue

        cyclic_data = np.array(PLCdata_dict[item_id])
        bytes_num = int(len(cyclic_data[0]) / 2)
        data_num = len(cyclic_data)

        hexs_item = []
        bins_item = []
        # ints_item = []
        # float_item = []

        for data_id in range(data_num):
            data_sample = cyclic_data[data_id]
            hexs_num = []
            bins_num = []
            # ints_num = []
            # float_num = []

            for bytes_id in range(bytes_num):
                bytes = data_sample[bytes_id * 2: bytes_id * 2 + 2]
                # obtain the hex data
                hexs_num.append(bytes)
                
                # obtain the bin data, 16 means the hex
                byte2binaries = bin(int(bytes, 16))[2:]
                byte2binaries = format(byte2binaries, '0>{}'.format(8))  # append the higher bits
                if not LSB:
                    byte2binaries = byte2binaries[::-1]
                    for bin_id in range(len(byte2binaries)):
                        bins_num.append(int(byte2binaries[bin_id]))
                else:
                    byte2binaries = byte2binaries
                    for bin_id in range(len(byte2binaries)):
                        bins_num.append(int(byte2binaries[bin_id]))
            
            hexs_item.append(hexs_num)
            bins_item.append(bins_num)

        PLChexs[item_id] = np.array(hexs_item)
        PLCbins[item_id] = np.array(bins_item)
        

    return PLChexs, PLCbins




def data_filtering(PLChexs, window=10, SCADA=False, LSB=False):
    
    PLChexs_filtered = {}
    PLCbins_filtered = {}

    for item_id in PLChexs.keys():
        
        hex_num = PLChexs[item_id]
        hexs_total = []
        bins_total = []
        
        for sample_id in range(window, hex_num.shape[0]):
        
            hex_filtered = []
            bin_filtered = []
            hexsamples = hex_num[sample_id-window : sample_id+window+1, :]

            for bin_id in range(hex_num.shape[1]):
                hex_sample_list = hexsamples[:, bin_id:bin_id + 1] 
                filtered_hex_value = hex_filtering_user(hex_sample_list[0])

                hex_filtered.append(filtered_hex_value)

                # obtain the bin data, 16 means the hex
                byte2binaries = bin(int(filtered_hex_value, 16))[2:]
                byte2binaries = format(byte2binaries, '0>{}'.format(8))  # append the higher bits

                if not LSB:
                    byte2binaries = byte2binaries[::-1]
                    for bin_id in range(len(byte2binaries)):
                        bin_filtered.append(int(byte2binaries[bin_id]))
                else:
                    byte2binaries = byte2binaries
                    for bin_id in range(len(byte2binaries)):
                        bin_filtered.append(int(byte2binaries[bin_id]))
            
            hexs_total.append(hex_filtered)
            bins_total.append(bin_filtered)
                
        PLChexs_filtered[item_id] = np.array(hexs_total)
        PLCbins_filtered[item_id] = np.array(bins_total)
    
    return PLChexs_filtered, PLCbins_filtered





def data_difference(PLCbins):
    
    PLCbins_differed = {}

    for item_id in PLCbins.keys():
        binaries = PLCbins[item_id]

        binaries_diff = np.zeros([binaries.shape[0]-1, binaries.shape[1]])
        for i in range(1, binaries.shape[0]):
            binaries_diff[i-1] = abs(binaries[i, :] - binaries[i-1, :])
        
        PLCbins_differed[item_id] = binaries_diff
        
    return PLCbins_differed


def data_translation(PLChexs, SCADA_record=True, bigend=True):
    # generate the integer or the float time series for plot
    # first test the given specified length, the advanced version should be given arbitary length

    if SCADA_record:
        seg_length = 4  # bytes number
    else:
        seg_length = 2  # bytes number

    # obtain the hex data
    # items_hexs_num = {}
    # ints_item_num = {}
    # float_item_num = {}
    packet_real = {}

    for key_id in PLChexs.keys():

        item_hexs = PLChexs[key_id]
        if item_hexs.shape[1] < seg_length:
            continue

        # # translate to the int data
        # ints_item = np.zeros([item_hexs.shape[0], xxx])
        # # translate to the float data
        # float_item = np.zeros([item_hexs.shape[0], xxx])

        # start_pos = 0
        start_pos = 0
        end_pos = 0
        item_real = np.zeros([item_hexs.shape[0], round(item_hexs.shape[1]/seg_length)])

        count = 0
        while (start_pos <= item_hexs.shape[1]-1) & (end_pos <= item_hexs.shape[1]):
            end_pos = start_pos + seg_length
            item_hexs_sample = item_hexs[0:, start_pos: end_pos]
            item_real_sample = np.zeros([item_hexs.shape[0], 1])

            for i in range(item_hexs_sample.shape[0]):
                hex_num = ''.join(item_hexs_sample[i])
                if seg_length == 2:
                    if bigend:
                        item_real_sample[i] = hex2int_big(hex_num)
                    else:
                        item_real_sample[i] = hex2int_little(hex_num)
                elif seg_length == 4:
                    if bigend:
                        item_real_sample[i] = hex2float_big(hex_num)
                    else:
                        item_real_sample[i] = hex2float_little(hex_num)

            item_real[0:, count] = item_real_sample[0:, 0]

            start_pos = start_pos + seg_length
            end_pos = start_pos + seg_length
            count = count+1

        packet_real[key_id] = item_real
        # plt.plot(item_real[0:, 0])
        # plt.show()
        # plt.plot(item_real[0:, 7])
        # plt.show()
    return packet_real



def data_segmentation_new(PLCbins, start_post=0):

    PLC_entropy = {}
    for item_id in PLCbins.keys():
        # obtain the entropy of each bit
        bins_item_num = PLCbins[item_id]
        bins_entropy = np.zeros([1, bins_item_num.shape[1]])
        samples = bins_item_num.shape[0]
        for bin_id in range(bins_item_num.shape[1]):
            variances = sum(bins_item_num[start_post:, bin_id:bin_id + 1])
            if variances < samples/2:
                bins_entropy[0, bin_id] = entropy_user(bins_item_num[start_post:, bin_id:bin_id + 1])
            else:
                bins_entropy[0, bin_id] = 1


            # non_zeros_ratio
            # entropy_user
        PLC_entropy[item_id] = bins_entropy
    
    return PLC_entropy

def data_segmentation(PLCbins_SCADA, PLCbins_I, PLCbins_Q, start_post=0):

    # use 4 to segment SCADA variables, as the IEEE754 standard specifies the float number using 4 bytes
    
    SCADA_entropy = {}
    for item_id in PLCbins_SCADA.keys():
        # obtain the entropy of each bit
        bins_item_num = PLCbins_SCADA[item_id]
        bins_entropy_SCADA = np.zeros([1, bins_item_num.shape[1]])
        
        for bin_id in range(bins_item_num.shape[1]):
            bins_entropy_SCADA[0, bin_id] = entropy_user(bins_item_num[start_post:, bin_id:bin_id + 1])


        SCADA_entropy[item_id] = bins_entropy_SCADA


    # use 2 to segment I variables, as the input/output module receive the analog signal using 2 bytes
    
    I_entropy = {}
    for item_id in PLCbins_I.keys():
        # obtain the entropy of each bit
        bins_item_num = PLCbins_I[item_id]
        bins_entropy_I = np.zeros([1, bins_item_num.shape[1]])
        for bin_id in range(bins_item_num.shape[1]):
            bins_entropy_I[0, bin_id] = entropy_user(bins_item_num[start_post:, bin_id:bin_id + 1])

        I_entropy[item_id] = bins_entropy_I


    # use 2 to segment Q variables, as the input/output module receive the analog signal using 2 bytes
    Q_entropy = {}
    for item_id in PLCbins_Q.keys():
        # obtain the entropy of each bit
        bins_item_num = PLCbins_Q[item_id]
        bins_entropy_Q = np.zeros([1, bins_item_num.shape[1]])
        for bin_id in range(bins_item_num.shape[1]):
            bins_entropy_Q[0, bin_id] = entropy_user(bins_item_num[start_post:, bin_id:bin_id + 1])

        Q_entropy[item_id] = bins_entropy_Q

    return SCADA_entropy, I_entropy, Q_entropy


if __name__ == '__main__':


    storepath = "./comm-Yang/"
    file_name = "comm_wincc_snap_20211116"
    # file_name = "comm_wincc_snap_20211223"
    
    filepath = storepath + file_name + ".json"

    if not os.path.exists(storepath + "comm_SCADA_20211116.pickle"):
    # if not os.path.exists(storepath + "comm_SCADA_20211223.pickle"):
        # open the json file
        packets_diction = packet_reading(filepath)
        # extract the data from comminications
        PLCBytedata_SCADA, PLCBytedata_I, PLCBytedata_Q = datasets_construction(packets_diction)

        with open(storepath +  "comm_SCADA_20211116.pickle", "wb") as fp:
            pickle.dump(PLCBytedata_SCADA, fp)
        with open(storepath +  "comm_PII_20211116.pickle", "wb") as fp:
            pickle.dump(PLCBytedata_I, fp)
        with open(storepath +  "comm_PIO_20211116.pickle", "wb") as fp:
            pickle.dump(PLCBytedata_Q, fp)
        # with open(storepath +  "comm_SCADA_20211223.pickle", "wb") as fp:
        #     pickle.dump(PLCBytedata_SCADA, fp)
        # with open(storepath +  "comm_PII_20211223.pickle", "wb") as fp:
        #     pickle.dump(PLCBytedata_I, fp)
        # with open(storepath +  "comm_PIO_20211223.pickle", "wb") as fp:
        #     pickle.dump(PLCBytedata_Q, fp)
    else:
        PLCBytedata_SCADA = pickle.load(open(storepath + "comm_SCADA_20211116.pickle", "rb"))
        PLCBytedata_I = pickle.load(open(storepath + "comm_PII_20211116.pickle", "rb"))
        PLCBytedata_Q = pickle.load(open(storepath + "comm_PIO_20211116.pickle", "rb"))
        # PLCBytedata_SCADA = pickle.load(open(storepath + "comm_SCADA_20211223.pickle", "rb"))
        # PLCBytedata_I = pickle.load(open(storepath + "comm_PII_20211223.pickle", "rb"))
        # PLCBytedata_Q = pickle.load(open(storepath + "comm_PIO_20211223.pickle", "rb"))
        


    MSBend = [0, 1]
    BigEnd = [0, 1]
    # MSBend = [1]
    # BigEnd = [1]
    for i in range(len(MSBend)):
        MSBtest = MSBend[i]
        BigEndtest = BigEnd[i]
        
        # segment the data as variables in MSB0
        PLChexs_SCADA, PLCbins_SCADA = binaries_construction(PLCBytedata_SCADA, LSB=MSBtest)
        PLChexs_I, PLCbins_I = binaries_construction(PLCBytedata_I, LSB=MSBtest)
        PLChexs_Q, PLCbins_Q = binaries_construction(PLCBytedata_Q, LSB=MSBtest)

        # # sliding window filtering, inputs: PLChexs_XXX, window_size
        # PLChexs_SCADA_filtered, PLCbins_SCADA_filtered = data_filtering(PLChexs_SCADA, LSB=MSBtest, window=0)
        # PLChexs_I_filtered, PLCbins_I_filtered = data_filtering(PLChexs_I, LSB=MSBtest, window=0)
        # PLChexs_Q_filtered, PLCbins_Q_filtered = data_filtering(PLChexs_Q, LSB=MSBtest, window=0)
        

        with open(storepath + file_name + "_SCADA_hex_MSB0_{}.pickle".format(MSBtest), "wb") as fp:
            pickle.dump(PLChexs_SCADA, fp)
        # with open(storepath + file_name + "comm_SCADA_20211116_bins_little.pickle", "wb") as fp:
        #     pickle.dump(PLCbins_SCADA, fp)
        
        with open(storepath + file_name + "_SnapI_hex_MSB0_{}.pickle".format(MSBtest), "wb") as fp:
            pickle.dump(PLChexs_I, fp)
        # with open(storepath + file_name + "comm_SnapI_20211116_bins_little.pickle", "wb") as fp:
        #     pickle.dump(PLCbins_I, fp)
        
        with open(storepath + file_name + "_SnapQ_hex_MSB0_{}.pickle".format(MSBtest), "wb") as fp:
            pickle.dump(PLChexs_Q, fp)
        # with open(storepath + file_name + "comm_SnapQ_20211116_bins_little.pickle", "wb") as fp:
        #     pickle.dump(PLCbins_Q, fp)


        # obtain the varying difference 
        PLCbins_differed_SCADA = data_difference(PLCbins_SCADA)
        PLCbins_differed_I = data_difference(PLCbins_I)
        PLCbins_differed_Q = data_difference(PLCbins_Q)


        # segment variables in SCADA (I/O) commnunication
        # SCADA_entropy, I_entropy, Q_entropy = data_segmentation(PLCbins_SCADA, PLCbins_I, PLCbins_Q, start_post=1200)
        # SCADA_entropy, I_entropy, Q_entropy = data_segmentation(PLCbins_differed_SCADA, PLCbins_differed_I, PLCbins_differed_Q, start_post=0)

        SCADA_entropy = data_segmentation_new(PLCbins_differed_SCADA, start_post=0)
        I_entropy = data_segmentation_new(PLCbins_differed_I, start_post=0)
        Q_entropy = data_segmentation_new(PLCbins_differed_Q, start_post=0)

        # the following is for generating data in mat, for matplot
        PLC_data = {}
        for key_id in SCADA_entropy.keys():
            PLC_data["SCADA_"+key_id] = SCADA_entropy[key_id]

        for key_id in I_entropy.keys():
            PLC_data["I_"+key_id] = np.array(I_entropy[key_id])

        for key_id in Q_entropy.keys():
            PLC_data["Q_"+key_id] = np.array(Q_entropy[key_id])

        savemat(storepath + file_name + "_MSB0_{}.mat".format(MSBtest), PLC_data)



    print("finished")

    # map variables in I/Q with variables in SCADA, metric: coorcoef

    # train the scaling function
