import os
import re
import traceback

cpu_frequence = 2194000000

def save_data(filename, line):
	try:
		with open(filename, mode='a+', encoding='utf-8') as file:
			file.write(line)
			file.close()
	except Exception:
		print(traceback.format_exc())
		return

def get_fh_data(all_lines):
	loop_event = 0
	loops_list = []
	loop_start = False
	item_start = False
	fh_split = False

	re_condition = r'0x64730000'
	for line in all_lines:
		field = line.split(",")
		if len(field) != 6:
			continue
		if field[1] == "0" and field[4] in [re_condition]:
			loop_start = True
			loop_split = True
			loop_list = []
		else:
			loop_split = False

		if loop_split is True:
			loop_list = []
			loops_list.append(loop_list)

		if loop_start == True:
			if field[1] == "0":
				if field[4] in ["0x64730000","0x64730001"]:
					item_start = True
					split = True
				else:
					item_start = False
			else:
				split = False

			if split is True:
				item_dict = {}
				loop_list.append(item_dict)

			if item_start is True:
				item_dict[field[1]] = [field[0], field[3],field[4]]

	return loops_list

def get_data(all_lines):
	loop_event = 0
	loops_list = []
	loop_start = False
	item_start = False
	split = False

	re_condition = r'0x64720001'
	for line in all_lines:
		field = line.split(",")
		if len(field) != 6:
			continue
		if field[1] == "0" and field[4] in [re_condition]:
			loop_start = True
			loop_split = True
			loop_list = []
		else:
			loop_split = False

		if loop_split is True:
			loop_list = []
			loops_list.append(loop_list)

		if loop_start == True:
			if field[1] == "0":
				if field[4] in ["0x64720001","0x64720002","0x64720003","0x64720004","0x64720005","0x64720006","0x64720007","0x64720008","0x64720009","0x6472000A","0x6472000B","0x64721000","0x64721001",
								"0x64720010","0x64720011","0x64720012","0x64720013","0x64720014","0x64720015","0x64720016","0x64720017","0x64720018","0x64720019","0x6472001A","0x6472001B","0x6472001C",
								"0x6472001D","0x6472001E","0x6472001F","0x64720020","0x64720021","0x64720022","0x64720023","0x64720024","0x64720025","0x64730000","0x64730001"]:
					item_start = True
					split = True
				else:
					item_start = False
			else:
				split = False

			if split is True:
				item_dict = {}
				loop_list.append(item_dict)

			if item_start is True:
				item_dict[field[1]] = [field[0], field[3],field[4]]

	return loops_list

def data_process(cmd):
	loops_list = []
	fh_loops_list = []

	try:
		if(os.path.exists("drive.txt")):
			os.remove("drive.txt")
		with open("var.txt", mode='r', encoding='utf-8') as file:
			all_lines = file.readlines()
			file.close()
	except Exception:
		print(traceback.format_exc())
		return

	loops_list = get_data(all_lines)
	fh_loops_list = get_fh_data(all_lines)
	#print(loops_list[1])

	count = 0
	for loop_list in loops_list:
		loop_start_time = 0
		loop_end_time = 0
		fh_rx_dma_start = 0
		fh_rx_dma_end = 0
		fh_rx_callback_start = 0
		fh_rx_callback_end = 0
		fec_ping_tx_dma_encode_start = 0
		fec_ping_tx_dma_encode_end = 0
		fec_pong_tx_dma_encode_start = 0
		fec_pong_tx_dma_encode_end = 0
		fec_ping_tx_dma_decode_start = 0
		fec_ping_tx_dma_decode_end = 0
		fec_pong_tx_dma_decode_start = 0
		fec_pong_tx_dma_decode_end = 0
		fec_ping_rx_dma_encode_start = 0
		fec_ping_rx_dma_encode_end = 0
		fec_pong_rx_dma_encode_start = 0
		fec_pong_rx_dma_encode_end = 0
		fec_ping_rx_dma_decode_start = 0
		fec_ping_rx_dma_decode_end = 0
		fec_pong_rx_dma_decode_start = 0
		fec_pong_rx_dma_decode_end = 0
		fec_callback_start = 0
		fec_callback_end = 0
		store_str = ""

		with open("drive.txt", mode='a+', encoding='utf-8') as file:
			#print("--------------------------------------------------------------------------------------Drive Thread %d LOOP--------------------------------------------------------------------------------------\n" % count)
			file.write("--------------------------------------------------------------------------------------Drive Thread %d LOOP--------------------------------------------------------------------------------------\n" % count)
			#store_str = store_str + "------------------------------------------------Drive Thread %d LOOP------------------------------------------------\n" % count
			for item in loop_list:
				#print(item.keys())
				#print(item)
				if len(item) == 0:
					continue
				if item['0'][2] ==  '0x64720001':
					loop_start_time = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720002':
					fec_end_time = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC compelte time:        %sus" % (fec_end_time - loop_start_time))
					file.write("FEC compelte time:        %sus\n" % (fec_end_time - loop_start_time))
					#store_str = store_str + "FEC cost time: %sus\n" % (fec_end_time - loop_start_time)

				if item['0'][2] ==  '0x64720003':
					fh_tx_dma_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720004':
					fh_tx_dma_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH tx dma time cost:      %sus" % (fh_tx_dma_end - fh_tx_dma_start))
					file.write("FH tx dma time cost:      %sus\n" % (fh_tx_dma_end - fh_tx_dma_start))

				if item['0'][2] ==  '0x64720005':
					fh_rx_dma_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720006':
					fh_rx_dma_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH rx dma time cost:      %fus" % (fh_rx_dma_end - fh_rx_dma_start))
					#store_str = store_str + "FH rx dma cost time: %fus\n" % (fh_rx_dma_end - fh_rx_dma_start)
					file.write("FH rx dma time cost:      %fus\n" % (fh_rx_dma_end - fh_rx_dma_start))

				if item['0'][2] ==  '0x64720007':
					fh_prach_dma_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720008':
					fh_prach_dma_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH prach dma time cost:  %fus" % (fh_prach_dma_end - fh_prach_dma_start))
					#store_str = store_str + "FH rx dma cost time: %fus\n" % (fh_rx_dma_end - fh_rx_dma_start)
					file.write("FH prach dma time cost:  %fus\n" % (fh_prach_dma_end - fh_prach_dma_start))

				if item['0'][2] ==  '0x64720009':
					fh_rx_callback_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x6472000A':
					fh_rx_callback_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH rx callbcak time cost: %fus" % (fh_rx_callback_end - fh_rx_callback_start))
					#store_str = store_str + "FH rx callbcak cost time: %fus\n" % (fh_rx_callback_end - fh_rx_callback_start)
					file.write("FH rx callbcak time cost: %fus\n" % (fh_rx_callback_end - fh_rx_callback_start))

				if item['0'][2] ==  '0x6472000B':
					loop_end_time = int(item['0'][0])*1000000/cpu_frequence
					#print("Loop time cost:           %fus" % (loop_end_time - loop_start_time))
					file.write("Loop time cost:           %fus\n" % (loop_end_time - loop_start_time))

				if item['0'][2] ==  '0x64720010':
					fec_ping_tx_dma_encode_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720011':
					fec_ping_tx_dma_encode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PING: encode tx dma time cost:  %fus" % (fec_ping_tx_dma_encode_end - fec_ping_tx_dma_encode_start))
					file.write("FEC PING: encode tx dma time cost:  %fus\n" % (fec_ping_tx_dma_encode_end - fec_ping_tx_dma_encode_start))

				if item['0'][2] ==  '0x64720012':
					fec_pong_tx_dma_encode_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720013':
					fec_pong_tx_dma_encode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PONG: encode tx dma time cost:  %fus" % (fec_pong_tx_dma_encode_end - fec_pong_tx_dma_encode_start))
					file.write("FEC PONG: encode tx dma time cost:  %fus\n" % (fec_pong_tx_dma_encode_end - fec_pong_tx_dma_encode_start))

				if item['0'][2] ==  '0x64720014':
					fec_ping_tx_dma_decode_start = int(item['0'][0])*1000000/cpu_frequence

				if item['0'][2] ==  '0x64720015':
					fec_ping_tx_dma_decode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PING: decode tx dma time cost:  %fus" % (fec_ping_tx_dma_decode_end - fec_ping_tx_dma_decode_start))
					file.write("FEC PING: decode tx dma time cost:  %fus\n" % (fec_ping_tx_dma_decode_end - fec_ping_tx_dma_decode_start))

				if item['0'][2] ==  '0x64720016':
					fec_pong_tx_dma_decode_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x64720017':
					fec_pong_tx_dma_decode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PONG: encode tx dma time cost:  %fus" % (fec_pong_tx_dma_decode_end - fec_pong_tx_dma_decode_start))
					file.write("FEC PONG: encode tx dma time cost:  %fus\n" % (fec_pong_tx_dma_decode_end - fec_pong_tx_dma_decode_start))
	
				if item['0'][2] ==  '0x64720018':
					fec_ping_rx_dma_encode_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x64720019':
					fec_ping_rx_dma_encode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PING: encode rx dma time cost:  %fus" % (fec_ping_rx_dma_encode_end - fec_ping_rx_dma_encode_start))
					file.write("FEC PING: encode rx dma time cost:  %fus\n" % (fec_ping_rx_dma_encode_end - fec_ping_rx_dma_encode_start))
	
				if item['0'][2] ==  '0x6472001A':
					fec_pong_rx_dma_encode_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x6472001B':
					fec_pong_rx_dma_encode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PONG: encode rx dma time cost:  %fus" % (fec_pong_rx_dma_encode_end - fec_rx_pong_dma_encode_start))
					file.write("FEC PONG: encode rx dma time cost:  %fus\n" % (fec_pong_rx_dma_encode_end - fec_rx_pong_dma_encode_start))
	
				if item['0'][2] ==  '0x6472001C':
					fec_ping_rx_dma_decode_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x6472001D':
					fec_ping_rx_dma_decode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PING: decode rx dma time cost:  %fus" % (fec_ping_rx_dma_decode_end - fec_ping_rx_dma_decode_start))
					file.write("FEC PING: decode rx dma time cost:  %fus\n" % (fec_ping_rx_dma_decode_end - fec_ping_rx_dma_decode_start))
	
				if item['0'][2] ==  '0x6472001E':
					fec_pong_rx_dma_decode_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x6472001F':
					fec_pong_rx_dma_decode_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC PONG: encode rx dma time cost:  %fus" % (fec_pong_rx_dma_decode_end - fec_pong_rx_dma_decode_start))
					file.write("FEC PONG: encode rx dma time cost:  %fus\n" % (fec_pong_rx_dma_decode_end - fec_pong_rx_dma_decode_start))
	
				if item['0'][2] ==  '0x64720020':
					fec_callback_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x64720021':
					fec_callback_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH rx callbcak time cost: %fus" % (fec_callback_end - fec_allback_start))
					file.write("FH rx callbcak time cost: %fus\n" % (fec_callback_end - fec_callback_start))
	
				if item['0'][2] ==  '0x64720022':
					dm_schedule_fth_rd_descriptors_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x64720023':
					dm_schedule_fth_rd_descriptors_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH rx callbcak time cost: %fus" % (fec_callback_end - fec_allback_start))
					file.write("FH rd descriptors time cost: %fus\n" % (dm_schedule_fth_rd_descriptors_end - dm_schedule_fth_rd_descriptors_start))
	
				if item['0'][2] ==  '0x64720024':
					dm_schedule_fth_rd_descriptors_start = int(item['0'][0])*1000000/cpu_frequence
	
				if item['0'][2] ==  '0x64720025':
					dm_schedule_fth_rd_descriptors_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FH rx callbcak time cost: %fus" % (fec_callback_end - fec_allback_start))
					file.write("FH rd descriptors time cost: %fus\n" % (dm_schedule_fth_rd_descriptors_end - dm_schedule_fth_rd_descriptors_start))
	
				if item['0'][2] ==  '0x64721000':
					txtime_reg = int(item['1'][1])
					prachflag= (txtime_reg>>31) & 0x00000001
					nGpsLock = (txtime_reg>>30) & 0x00000001
					txtime_valid = (txtime_reg>>28) & 0x00000001
					nPingFlag = (txtime_reg>>26) & 0x00000001
					nPongFlag = (txtime_reg>>25) & 0x00000001
					txtime_sym = (txtime_reg>>21) & 0x0000000f
					txtime_frame = (txtime_reg>>11) & 0x0000003ff
					txtime_subframe = (txtime_reg>>5) & 0x0000003f
					txtime_slot = txtime_reg & 0x0000001f
					time = int(item['0'][0])*1000000/cpu_frequence
					#print("txtime[0-99]:    %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus" %
					#                                                                                                             (item['1'][2],
					#                                                                                                              prachflag,
					#                                                                                                              nGpsLock,
					#                                                                                                              nPingFlag,
					#                                                                                                              nPongFlag,
					#                                                                                                              txtime_valid,
					#                                                                                                              txtime_frame,
					#                                                                                                              txtime_subframe,
					#                                                                                                              txtime_slot,
					#                                                                                                              txtime_sym,
					#                                                                                                              txtime_frame*20+txtime_subframe*2+txtime_slot,
					#                                                                                                              time))
					file.write("txtime[0-99]:    %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus\n" %
																																	(item['1'][2],
																																	prachflag,
																																	nGpsLock,
																																	nPingFlag,
																																	nPongFlag,
																																	txtime_valid,
																																	txtime_frame,
																																	txtime_subframe,
																																	txtime_slot,
																																	txtime_sym,
																																	txtime_frame*20+txtime_subframe*2+txtime_slot,
																																	time))
					''' 
					#store_str = store_str + "txtime[0-99]:    %s valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d time = %sus\n" % \
					#                                                                                                             (item['1'][2],
					#                                                                                                              txtime_valid,
					#                                                                                                              txtime_frame,
					#                                                                                                              txtime_subframe,
					#                                                                                                              txtime_slot,
					#                                                                                                              txtime_sym,
					#                                                                                                              time)
					
					txtime_reg = int(item['2'][1])
					prachflag= (txtime_reg>>31) & 0x00000001
					nGpsLock = (txtime_reg>>30) & 0x00000001
					txtime_valid = (txtime_reg>>28) & 0x00000001
					nPingFlag = (txtime_reg>>26) & 0x00000001
					nPongFlag = (txtime_reg>>25) & 0x00000001
					txtime_sym = (txtime_reg>>21) & 0x0000000f
					txtime_frame = (txtime_reg>>11) & 0x0000003ff
					txtime_subframe = (txtime_reg>>5) & 0x0000003f
					txtime_slot = txtime_reg & 0x0000001f
					time = int(item['0'][0])*1000000/cpu_frequence
					#print("txtime[0-1023]:  %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus" %
					#                                                                                                             (item['2'][2],
					#                                                                                                              prachflag,
					#                                                                                                              nGpsLock,
					#                                                                                                              nPingFlag,
					#                                                                                                              nPongFlag,
					#                                                                                                              txtime_valid,
					#                                                                                                              txtime_frame,
					#                                                                                                              txtime_subframe,
					#                                                                                                              txtime_slot,
					#                                                                                                              txtime_sym,
					#                                                                                                              txtime_frame*20+txtime_subframe*2+txtime_slot,
					#                                                                                                              time))
					file.write("txtime[0-1023]:  %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus\n" %
																																	(item['2'][2],
																																	prachflag,
																																	nGpsLock,
																																	nPingFlag,
																																	nPongFlag,
																																	txtime_valid,
																																	txtime_frame,
																																	txtime_subframe,
																																	txtime_slot,
																																	txtime_sym,
																																	txtime_frame*20+txtime_subframe*2+txtime_slot,
																																	time))
				'''
				if item['0'][2] ==  '0x64721001':
					rxtime_reg = int(item['1'][1])
					prachflag= (rxtime_reg>>31) & 0x00000001
					nGpsLock = (rxtime_reg>>30) & 0x00000001
					rxtime_valid = (rxtime_reg>>28) & 0x00000001
					nPingFlag = (rxtime_reg>>26) & 0x00000001
					nPongFlag = (rxtime_reg>>25) & 0x00000001
					rxtime_sym = (rxtime_reg>>21) & 0x0000000f
					rxtime_frame = (rxtime_reg>>11) & 0x0000003ff
					rxtime_subframe = (rxtime_reg>>5) & 0x0000003f
					rxtime_slot = rxtime_reg & 0x0000001f
					time = int(item['0'][0])*1000000/cpu_frequence
					#print("rxtime[0-99]:    %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus" %
					#                                                                                                             (item['1'][2],
					#                                                                                                              prachflag,
					#                                                                                                              nGpsLock,
					#                                                                                                              nPingFlag,
					#                                                                                                              nPongFlag,
					#                                                                                                              rxtime_valid,
					#                                                                                                              rxtime_frame,
					#                                                                                                              rxtime_subframe,
					#                                                                                                              rxtime_slot,
					#                                                                                                              rxtime_sym,
					#                                                                                                              rxtime_frame*20+rxtime_subframe*2+rxtime_slot,
					#                                                                                                              time))
					file.write("rxtime[0-99]:    %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus\n" %
																																	(item['1'][2],
																																	prachflag,
																																	nGpsLock,
																																	nPingFlag,
																																	nPongFlag,
																																	rxtime_valid,
																																	rxtime_frame,
																																	rxtime_subframe,
																																	rxtime_slot,
																																	rxtime_sym,
																																	rxtime_frame*20+rxtime_subframe*2+rxtime_slot,
																																	time))
					#store_str = store_str + "rxtime[0-99]:    %s valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d time = %sus\n" % \
					#                                                                                                             (item['1'][2],
					#                                                                                                              rxtime_valid,
					#                                                                                                              rxtime_frame,
					#                                                                                                              rxtime_subframe,
					#                                                                                                              rxtime_slot,
					#                                                                                                              rxtime_sym,
					#                                                                                                              time)
					'''
					rxtime_reg = int(item['2'][1])
					prachflag= (rxtime_reg>>31) & 0x00000001
					nGpsLock = (rxtime_reg>>30) & 0x00000001
					rxtime_valid = (rxtime_reg>>28) & 0x00000001
					nPingFlag = (rxtime_reg>>26) & 0x00000001
					nPongFlag = (rxtime_reg>>25) & 0x00000001
					rxtime_sym = (rxtime_reg>>21) & 0x0000000f
					rxtime_frame = (rxtime_reg>>11) & 0x0000003ff
					rxtime_subframe = (rxtime_reg>>5) & 0x0000003f
					rxtime_slot = rxtime_reg & 0x0000001f
					time = int(item['0'][0])*1000000/cpu_frequence
					#print("rxtime[0-1023]:  %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus" %
					#                                                                                                             (item['2'][2],
					#                                                                                                              prachflag,
					#                                                                                                              nGpsLock,
					#                                                                                                              nPingFlag,
					#                                                                                                              nPongFlag,
					#                                                                                                              rxtime_valid,
					#                                                                                                              rxtime_frame,
					#                                                                                                              rxtime_subframe,
					#                                                                                                              rxtime_slot,
					#                                                                                                              rxtime_sym,
					#                                                                                                              rxtime_frame*20+rxtime_subframe*2+rxtime_slot,
					#                                                                                                              time))
					file.write("rxtime[0-1023]:  %s prachflag = %-2d nGpsLock = %-2d nPingFlag = %-2d nPongFlag = %-2d valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d sfidx = %-6d time = %sus\n" %
																																	(item['2'][2],
																																	prachflag,
																																	nGpsLock,
																																	nPingFlag,
																																	nPongFlag,
																																	rxtime_valid,
																																	rxtime_frame,
																																	rxtime_subframe,
																																	rxtime_slot,
																																	rxtime_sym,
																																	rxtime_frame*20+rxtime_subframe*2+rxtime_slot,
																																	time))
					#store_str = store_str + "rxtime[0-1023]:  %s valid = %-2d frame = %-6d subframe = %-4d slot = %-2d sym = %-2d time = %sus\n" % \
					#                                                                                                             (item['1'][2],
					#                                                                                                              rxtime_valid,
					#                                                                                                              rxtime_frame,
					#                                                                                                              rxtime_subframe,
					#                                                                                                              rxtime_slot,
					#                                                                                                              rxtime_sym,
					#                                                                                                              time)
					'''
			#save_data("drive.txt", store_str)
			count = count + 1
		file.close()
	
	count = 0    
	for fh_loop_list in fh_loops_list:
		gnb_fh_thread_start = 0
		gnb_fh_thread_end = 0
		with open("drive.txt", mode='a+', encoding='utf-8') as file:
			#print("--------------------------------------------------------------------------------------Drive Thread %d LOOP--------------------------------------------------------------------------------------\n" % count)
			file.write("--------------------------------------------------------------------------------------gnb FH Thread %d LOOP--------------------------------------------------------------------------------------\n" % count)
			#store_str = store_str + "------------------------------------------------Drive Thread %d LOOP------------------------------------------------\n" % count
			for item in fh_loop_list:
				#print(item.keys())
				#print(item)
				if len(item) == 0:
					continue
				if item['0'][2] ==  '0x64730000':
					gnb_fh_thread_start = int(item['0'][0])*1000000/cpu_frequence
				
				if item['0'][2] ==  '0x64730001':
					gnb_fh_thread_end = int(item['0'][0])*1000000/cpu_frequence
					#print("FEC compelte time:        %sus" % (fec_end_time - loop_start_time))
					file.write("gnb fh thread cost time:        %sus\n" % (gnb_fh_thread_end - gnb_fh_thread_start))
					#store_str = store_str + "FEC cost time: %sus\n" % (fec_end_time - loop_start_time)
			count = count + 1
		file.close()

def loop_process(arg):
	loop_flag = False
	count = 0
	item_start = False
	item_pr = 6
	check_count = 0
	idx = 1
	interval_flag = False
	interval_time = 0
	ticks_cur = 0
	ticks_prv = 0
	
	while idx < len(arg):
		if arg[idx] == "-n":
			check_count = int(arg[idx+1])
			idx = idx + 2
		elif arg[idx] == "-t":
			idx = idx + 1
			interval_flag = True
		elif len(arg) > 1:
			print("ERROR:parameter error !!!")
			return

	re_condition = r'0x64720001'
	try:
		if(os.path.exists("drive.txt")):
			os.remove("drive.txt")
		with open("var.txt", mode='r', encoding='utf-8') as file:
			all_lines = file.readlines()
			file.close()
	except Exception:
		print(traceback.format_exc())
		return

	if check_count > len(all_lines) or check_count == 0:
		check_count = len(all_lines)

	for line in all_lines[-check_count:]:
		field = line.split(",")
		if len(field) != 6:
			continue
		if field[1] == "0":
			if field[4] in [re_condition]:
				loop_flag = True
			item_start = True
		else:
			item_start = False

		if item_start == True:
			while item_pr < 6:
				print("%15s:%-10s|" % ("",""),end="")
				item_pr = item_pr + 1
			item_pr = 0
			if loop_flag == True:
				print("\n\n--------------------------------------------------------------------------------------Drive Thread %d LOOP--------------------------------------------------------------------------------------" % count,end="")
				count = count + 1
				loop_flag = False

			if interval_flag == False:
				print("\n<%s>m:%s f:%-20s|" % (field[0],field[4],field[2][-20:]),end="")
			else:
				ticks_cur = int(field[0]);
				if ticks_prv == 0:
					ticks_prv = ticks_cur
				interval_time = (ticks_cur - ticks_prv)*1000000/cpu_frequence
				print("\n[%6dus]<%s>m:%s f:%-20s|" % (interval_time,field[0],field[4],field[2][-20:]),end="")
				ticks_prv = ticks_cur
		elif item_pr < 6:
			print("%15s:%-10s|" % (field[2][-15:],field[3]),end="")
			item_pr = item_pr + 1

		if count == 20:
			break

	print("\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
	return

def dma_process(arg):
	line_cnt = 0
	pr_flag = False
	idx = 1
	check_count = 0
	
	while idx < len(arg):
		if arg[idx] == "-n":
			check_count = int(arg[idx+1])
			idx = idx + 2
		else:
			print("ERROR:parameter error !!!")
			return

	re_condition = '0x78594766'
	try:
		with open("var.txt", mode='r', encoding='utf-8') as file:
			all_lines = file.readlines()
			file.close()
	except Exception:
		print(traceback.format_exc())
		return

	if check_count > len(all_lines) or check_count == 0:
		check_count = len(all_lines)

	for line in all_lines[-check_count:]:
		field = line.split(",")
		if len(field) != 6:
			continue
		if field[1] == "0" and field[4] in [re_condition]:
			print("\n\n-------------- FhTx",end="")
			pr_flag = True
			line_cnt = 0
			continue
		elif field[1] == "0":
			pr_flag = False
			continue

		if pr_flag == True:
			if field[1] == "1":
				print(" SlotIdx:%5s" % field[3],end="")
				continue
			elif field[1] == "2":
				print(" Sym:%2s" % field[3],end="")
				continue
			elif field[1] == "3":
				print(" Ant:%s ------------------------------------------------" % field[3])
				continue

			print("%02x %02x %02x %02x " % ((int(field[3]))&0xff,(int(field[3]) >> 8)&0xff,(int(field[3]) >> 16)&0xff,(int(field[3]) >> 24)&0xff),end="")
			line_cnt = line_cnt + 4
			if line_cnt % 32 == 0:
				print("")

	print("")
	return

def get_process(arg):
	item_start = False
	item_pr = 0
	check_count = 0
	idx = 1
	magic_list = []
	interval_flag = False
	interval_time = 0
	ticks_cur = 0
	ticks_prv = 0
	
	while idx < len(arg):
		if arg[idx] == "-m":
			magic_list = arg[idx+1].split("&")
			idx = idx + 2
		elif arg[idx] == "-n":
			check_count = int(arg[idx+1])
			idx = idx + 2
		elif arg[idx] == "-t":
			idx = idx + 1
			interval_flag = True
		else:
			print("ERROR:parameter error !!! arg[%d]:%s" % (idx,arg[idx]))
			return

	if len(magic_list) < 1:
		print("ERROR:parameter error !!! cnt:%d" % len(magic_list))
		return

	try:
		if(os.path.exists("drive.txt")):
			os.remove("drive.txt")
		with open("var.txt", mode='r', encoding='utf-8') as file:
			all_lines = file.readlines()
			file.close()
	except Exception:
		print(traceback.format_exc())
		return
		
	if check_count > len(all_lines) or check_count == 0:
		check_count = len(all_lines)
	
	for line in all_lines[-check_count:]:
		field = line.split(",")
		if len(field) != 6:
			continue
		if field[1] == "0" and field[4] in magic_list:
			item_start = True
			item_pr = 0
		elif field[1] == "0":
			item_pr = 0
			item_start = False
		else:
			item_start = False

		if item_start == True:
			if interval_flag == False:
				print("\n<%s>m:%s f:%-20s|" % (field[0],field[4],field[2][-20:]),end="")
			else:
				ticks_cur = int(field[0]);
				if ticks_prv == 0:
					ticks_prv = ticks_cur
				interval_time = (ticks_cur - ticks_prv)*1000000/cpu_frequence
				print("\n[%6dus]<%s>m:%s f:%-20s|" % (interval_time,field[0],field[4],field[2][-20:]),end="")
				ticks_prv = ticks_cur
			item_pr = item_pr + 1
		elif item_pr < 7 and item_pr > 0:
			print("%15s:%-10s|" % (field[2][-15:],field[3]),end="")
			item_pr = item_pr + 1

	print("")
	return

def cmd_parse(cmd):
	field = cmd.split(" ")
	idx = 0
	
	while True:    #消除空格
		try:
			idx = field.index('')
		except:
			break
		field.pop(idx)

	if len(field) < 1:
		return

	if field[0] == 'loop':
		loop_process(field)
	elif field[0] == 'dma':
		dma_process(field)
	elif field[0] == 'get':
		get_process(field)
	elif field[0] == 'h':
		print("Usage:")
		print("dma [-n] [count]")
		print("loop [-n] [count] [-t]")
		print("get -m magic_word [-n] [count] [-t]")

	return

def main():
	while True:
		str = input("<cmd>")
		try:
			cmd_parse(str)
		except Exception:
			print(traceback.format_exc())  

if __name__ == '__main__':
	main()

