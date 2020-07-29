import os
import re
import traceback

cpu_frequence = 2194000000

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
	file.close()
	return

def dma_process(arg):
	line_cnt = 0
	pr_flag = False
	idx = 1
	check_count = 0
	slot_list = []
	slot_pr = False
	nodata_flag = False
	
	while idx < len(arg):
		if arg[idx] == "-n":
			check_count = int(arg[idx+1])
			idx = idx + 2
		elif arg[idx] == "-s":
			slot_list = arg[idx+1].split("&")
			slot_pr = True
			idx = idx + 2
		elif arg[idx] == "-nod":
			nodata_flag = True
			idx = idx + 1
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
			pr_flag = True
			line_cnt = 0
			continue
		elif field[1] == "0":
			pr_flag = False
			continue

		if pr_flag == True:
			if field[1] == "1":
				if slot_pr == True:
					if field[3] in slot_list:
						print("\n-------------- FhTx SlotIdx:%5s" % field[3],end="")
					else:
						pr_flag = False
						continue
				else:
					print("\n\n-------------- FhTx SlotIdx:%5s" % field[3],end="")
				continue
			elif field[1] == "2":
				print(" Sym:%2s" % field[3],end="")
				continue
			elif field[1] == "3":
				print(" Ant:%s ------------------------------------------------" % field[3])
				continue
			if nodata_flag == False:
				print("%02x %02x %02x %02x " % ((int(field[3]))&0xff,(int(field[3]) >> 8)&0xff,(int(field[3]) >> 16)&0xff,(int(field[3]) >> 24)&0xff),end="")
				line_cnt = line_cnt + 4
				if line_cnt % 32 == 0:
					print("")

	print("")
	file.close()
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
	pr_nomagic = False
	pr_nofunc = False
	pr_noticks = False
	pr_verbose = False
	
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
		elif arg[idx] == "-nof":
			idx = idx + 1
			pr_nofunc = True
		elif arg[idx] == "-nom":
			idx = idx + 1
			pr_nomagic = True
		elif arg[idx] == "-not":
			idx = idx + 1
			pr_noticks = True
		elif arg[idx] == "-v":
			idx = idx + 1
			pr_verbose = True
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
			if pr_noticks == False:
				if interval_flag == False:
					print("\n<%s>" % field[0],end="")
				else:
					ticks_cur = int(field[0]);
					if ticks_prv == 0:
						ticks_prv = ticks_cur
					interval_time = (ticks_cur - ticks_prv)*1000000/cpu_frequence
					print("\n[%6dus]<%s>" % (interval_time,field[0]),end="")
					ticks_prv = ticks_cur
			else:
				print("")
			if pr_nomagic == False:
				print("m:%s" % field[4],end="")
			if pr_nofunc == False:
				print(" f:%-20s" % field[2][-20:],end="")
			print("|",end="")
			item_pr = item_pr + 1
		elif item_pr < 7 and item_pr > 0:
			if pr_verbose == False:
				print("%15s:%-10s|" % (field[2][-15:],field[3]),end="")
				item_pr = item_pr + 1
			else:
				print(" %s:%s |" % (field[2][-15:],field[3]),end="")

	print("")
	file.close()
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
		print("---------------")
		print("<CMD>dma [-n] [count] [-s] [-nod]")
		print(" -s  : select slot to display")
		print(" -nod: don't display slot data")
		print("======")
		print("<CMD>loop [-n] [count] [-t]")
		print("======")
		print("<CMD>get -m magic_word [-n] [count] [-t] [-not] [-nom] [-nof]")
		print(" -t  : display interval")
		print(" -not: don't display interval")
		print(" -nom: don't display magic world")
		print(" -nof: don't display function")
		print("---------------")
		print("\r\nsuggestion:")
		print("---------------")
		print("loop start         :0x64720001")
		print("loop end           :0x6472000B")
		print("FhTxValid          :0x64720003")
		print("FhRxValid          :0x64721010")
		print("cpa_fh_rx_callback :0xBCBCBCBC")
		print("bbupool_onetask_gen:0x10203040")
		print("task_dl_config     :0xCCBBCCBB")
		print("---------------")

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

