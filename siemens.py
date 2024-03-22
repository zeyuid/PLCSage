#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File:     siemens.py
# Brief:    Siemens PLC class used to communicate between PC and PLC (snap7).

import snap7
from datetime import datetime
import struct
import sys


class SIEMENSPLC(object):
    def __init__(self, ip_address, plc_name, rack=0, slot=2, port=102):
        self.plc_name = plc_name
        # (ip, rack, slot, port) for TCP connection (default is for S7-1200 series).
        self.ip_address = ip_address
        self.rack = rack
        self.slot = slot
        self.port = port

        self.client = snap7.client.Client()
        self.is_connect = False

        self.data = None

        # test data
        self.td = None

    def plc_connect(self):
        try:
            self.client.connect(self.ip_address, self.rack, self.slot, self.port)
            self.is_connect = self.check_connection()
        except Exception as e:
            print(e)

    def check_connection(self):
        return self.client.get_connected()

    def plc_disconnect(self):
        self.client.disconnect()
        self.client.destroy()

    def plc_read_data(self, I_param, Q_param, DB_read_param):
        # read_area(area, dbnumber, start, size: number of bytes)
        I_data, Q_data, DB_data = [], [], []

        # read I signal
        for param in I_param:
            I_data.append([param[0], self.client.read_area(snap7.types.Areas.PE, 0, param[1], param[2])])
        # read Q signal
        for param in Q_param:
            Q_data.append([param[0], self.client.read_area(snap7.types.Areas.PA, 0, param[1], param[2])])

        if len(DB_read_param) != 0:
            for param in DB_read_param:
                # print(param)
                DB_data.append([param[0], self.client.read_area(snap7.types.Areas.DB, param[0], param[1], param[2])])
                # print(self.client.read_area(snap7.types.Areas.DB, param[1], param[2], param[3]))

        # data_lst = ["I " + ",".join([(each[0] + str(struct.unpack('B'*len(each[1]), each[1]))) for each in I_dat`a]),
        #             "Q " + ",".join([(each[0] + str(struct.unpack('B'*len(each[1]), each[1]))) for each in Q_data]),
        #             "DB " + ",".join([(each[0] + str(struct.unpack('>h', each[1]))) for each in DB_data])]
        # self.data = "|".join(data_lst)
        data_dict = {}
        # print("For test IW94: ", I_data)
        data_dict["I"] = [struct.unpack('>h', each[1]) for each in I_data]
        # print("For test IW94: ", data_dict["I"])
        data_dict["Q"] = [struct.unpack('>h', each[1]) for each in Q_data]
        data_dict["DB"] = [struct.unpack('>f', each[1]) for each in DB_data]
        return data_dict


    def plc_read_data_noparsing(self, I_param, Q_param, DB_read_param):
        # read_area(area, dbnumber, start, size: number of bytes)
        I_data, Q_data, DB_data = [], [], []

        # read I signal
        for param in I_param:
            I_data.append([param[0], self.client.read_area(snap7.types.Areas.PE, 0, param[1], param[2])])
        # read Q signal
        for param in Q_param:
            Q_data.append([param[0], self.client.read_area(snap7.types.Areas.PA, 0, param[1], param[2])])

        if len(DB_read_param) != 0:
            for param in DB_read_param:
                # print(param)
                DB_data.append([param[0], self.client.read_area(snap7.types.Areas.DB, param[0], param[1], param[2])])
                # print(self.client.read_area(snap7.types.Areas.DB, param[1], param[2], param[3]))

        # data_lst = ["I " + ",".join([(each[0] + str(struct.unpack('B'*len(each[1]), each[1]))) for each in I_dat`a]),
        #             "Q " + ",".join([(each[0] + str(struct.unpack('B'*len(each[1]), each[1]))) for each in Q_data]),
        #             "DB " + ",".join([(each[0] + str(struct.unpack('>h', each[1]))) for each in DB_data])]
        # self.data = "|".join(data_lst)
        data_dict = {}
        # print("For test IW94: ", I_data)
        data_dict["I"] = I_data 
        # print("For test IW94: ", data_dict["I"])
        data_dict["Q"] = Q_data
        data_dict["DB"] = DB_data
        return data_dict

    # def plc_write_data(self, DB_param):
        # command_str = ''
        # for param in DB_param:
        #     if len(param) != 3:
        #         print("Error PLC write param: {}".format(param))
        #         pass
        #     db_number, start_index, data = param
        #     # print(param)
        #     self.client.write_area(snap7.types.Areas.DB, db_number, start_index, struct.pack('>I', data))
        #     # self.client.as_db_write(db_number, start_index, size, data)
        #     command_str += str([db_number, start_index, data]) + ' '
        # self.data += "|send" + command_str

    def plc_write_data(self, I_param, Q_param, DB_param):
        for param in I_param:
            self.client.write_area(snap7.types.Areas.PE, param[0], param[1], struct.pack('>h', param[2]))
        for param in Q_param:
            self.client.write_area(snap7.types.Areas.PA, param[0], param[1], struct.pack('>h', param[2]))
        for param in DB_param:
            db_number, start_index, data = param
            # some problems here for '>h' and '>I'
            self.client.write_area(snap7.types.Areas.DB, db_number, start_index, struct.pack('>I', data))
        

    def plc_send_command(self, I_param, Q_param, DB_read_param, DB_param):
        self.plc_read_data(I_param, Q_param, DB_read_param)
        if len(DB_param) != 0:
            self.plc_write_data(DB_param)

    def test_data(self):
        # print(a, b)
        print(str(datetime.now().strftime("%H:%M:%S.%f"))+"PLC")
        self.td = str(datetime.now().strftime("%H:%M:%S.%f"))+"PLC"


if __name__ == "__main__":
    plc = SIEMENSPLC('192.168.0.222', 'distillation tower')
    plc.plc_connect()
    if not plc.check_connection():
        print("ERROR with connection, exiting the program")
        sys.exit()
    data = plc.client.read_area(snap7.types.Areas.DB, 11, 12, 2)
    print(data)
    # print(data)
    print(struct.unpack('>h', data))
    plc.client.write_area(snap7.types.Areas.DB, 11, 12, struct.pack('>h', 17498))
    # print(struct.pack('>I', 500))
    # plc.client.write_area(snap7.types.Areas.DB, 3, 1840, struct.pack('>I', 100))
    # data = plc.client.read_area(snap7.types.Areas.DB, 3, 1836, 4)
    # print(struct.unpack('>I', data))
    # plc.plc_read_data([], [['QB111', 111, 1]])
    # print(plc.data)
    plc.plc_disconnect()

   
   
   
   
   
   
   
    # \xaa\x00 -> Byte: 170, 0 (e.g. IB101, IB102)
    # \xaa\x00 -> Word: 170 (e.g. IW100 实际是100,102双字节）
    # print(struct.pack('H', 170))
    # print(struct.pack('b', -86))
    # print(struct.unpack(struct.pack('B', 170)+struct.pack('B', 0)))
    # b = struct.pack('B', 170)+struct.pack('B', 0)
    # print(b)
    # print(type(b))
    # print(struct.unpack('H', b))

# def plc_test(ip_address):
#     plc = snap7.client.Client()
#     plc.connect(ip_address, 0, 0)
#     print(plc.get_connected())
#     data = plc.read_area(snap7.types.Areas.PA, 0, 0, 1)
#     print(data)
#     snap7.util.set_bool(data, 0, 2, False)
#     print(data)
#     plc.write_area(snap7.types.Areas.PA, 0, 0, data)
#     c = plc.read_area(snap7.types.Areas.PA, 0, 0, 1)
#     print(c)
#     plc.disconnect()
#     print(plc.get_connected())
#     plc.destroy()

# plc_test("192.168.1.10")
