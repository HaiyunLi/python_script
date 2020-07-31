import os
import re
import traceback
import ctypes,sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.

# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_DARKBLUE = 0x10 # dark blue.
BACKGROUND_DARKGREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

cpu_frequence = 2194000000

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
	Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
	return Bool

#reset white
def resetColor():
	set_cmd_text_color(FOREGROUND_WHITE|BACKGROUND_DARKSKYBLUE)

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

def task_print(flag,bypassFlag,slot):
	idx = 0
	task_id =0

	print("\r\n---- slot:%-5d ----------------------------" % slot)
	print("idx  0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19",end="")
	for idx in range(0,2):
		print("\r\n %d " % idx,end="")
		for task_id in range(0,20):
			if flag[idx][task_id] == 1:
				pr_temp = 'Y'
				sys.stdout.flush()
				set_cmd_text_color(FOREGROUND_RED|BACKGROUND_DARKSKYBLUE)
				print(" %s" % pr_temp,end="")
				sys.stdout.flush()
				resetColor()
				print("/%d " % bypassFlag[idx][task_id],end="")
			else:
				pr_temp = 'N'
				sys.stdout.flush()
				set_cmd_text_color(FOREGROUND_DARKGRAY|BACKGROUND_DARKSKYBLUE)
				print(" %s" % pr_temp,end="")
				sys.stdout.flush()
				resetColor()
				print("/%d " % bypassFlag[idx][task_id],end="")
	print("")
	return

def task_prompt():
	print("\r\nDL dependence:")
	print("             |-->PDSCH_TB(1)")
	print(" CONFIG(0)-->|-->PDSCH_RS_GEN(4)    |-->PDSCH_SYMBOL_TX(3)|")
	print("             |-->CONTROL_CHANNELS(5)|-------------------->|-->DL_POST(18)")
	print("\r\nUL dependence:")
	print("CONFIG(6)        |")
	print("PUSCH_TB(14)     |")
	print("PUCCH_RX(15)     |-->UL_POST(19)")
	print("PRACH_PROCESS(16)|")
	print("SRS_RX(17)       |")
	print("\r\n               |-->PUSCH_MMSE0(9)-->|PUSCH_SYMBOL_0_RX(11)-->|")
	print("PUSCH_CE0(7)-->|                    |PUSCH_SYMBOL_7_RX(12)-->|-->PUSCH_LLR_RX(13) gen PUSCH_TB(14)")
	print("               |-->PUSCH_MMSE7(10)----^")
	print("PUSCH_CE1(8)--------^\r\n")
	print("|------------------------------|")
	print("| --> | <auto generate>        |")
	print("|------------------------------|")
	print("| gen | <initiactive generate> |")
	print("|------------------------------|\r\n")
	return
	
def task_process(arg):
	item_start = False
	prompt_flag = False
	need_pr = False
	#task_bypassFlag = [[0 for col in range(2)] for row in range(20)]
	task_bypassFlag = [[0]*20]*2
	#task_flag = [[False for col in range(2)] for row in range(20)]
	task_flag = [[0]*20]*2
	#task_seq = [[0 for col in range(2)] for row in range(20)]
	task_seq = [[0]*20]*2
	idx = [0]*20
	slot_list = []
	task_id = 0
	cur_slot = 0xffff
	pr_slot = 0xffff
	max_slot = 0xffff
	min_slot = 0xffff
	stop_slot = 0xffff
	analyze_slot = 0
	i = 1
	check_count = 0

	while i < len(arg):
		if arg[i] == "-s":
			slot_list = arg[i+1].split("&")
			i = i + 2
		elif arg[i] == "-n":
			check_count = int(arg[i+1])
			i = i + 2
		elif arg[i] == "-p":
			prompt_flag = True
			break
		else:
			print("ERROR:parameter error !!! arg[%d]:%s" % (i,arg[i]))
			return

	if prompt_flag == True:
		task_prompt()
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

	i = 0
	re_condition = '0x10203040'
	while True:
		if len(slot_list) > 0:
			if(i == len(slot_list)):
				break
			pr_slot = int(slot_list[i])
			i = i + 1
		else:
			if stop_slot == 0xffff and pr_slot != 0xffff:
				if pr_slot != min_slot:
					stop_slot = pr_slot

			if pr_slot != 0xffff:
				pr_slot = pr_slot +1
				if pr_slot > max_slot:
					pr_slot = min_slot
			if pr_slot == stop_slot and stop_slot != 0xffff:
				break
		
		for m in range(0,20):  #清空上一个slot标记
			idx[m] = 0
			for n in range(0,2):
				task_bypassFlag[n][m] = 0
				task_flag[n][m] = 0
				task_seq[n][m] = 0
	
		for line in all_lines[-check_count:]:
			field = line.split(",")
			if len(field) != 6:
				continue
			if field[1] == "0" and field[4] in re_condition:
				item_start = True
			elif item_start != True:
				continue

			if field[2] == 'taskId':
				task_id = int(field[3])
				continue
			elif field[2] == 'tasksf':
				cur_slot = int(field[3])
				if max_slot != 0xffff:
					if cur_slot > max_slot:
						max_slot = cur_slot
					if cur_slot < min_slot:
						min_slot = cur_slot
				
				if pr_slot != cur_slot and pr_slot != 0xffff:
					if (need_pr == True) and ((pr_slot < cur_slot and cur_slot > pr_slot + 10) or (pr_slot > cur_slot and pr_slot > cur_slot+10)):
						#print("--0-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
						task_print(task_flag,task_bypassFlag,pr_slot)
						need_pr = False
					item_start = False
				else:
					#print("--1-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
					idx[task_id] = idx[task_id]^1
					task_flag[idx[task_id]][task_id] = True
					need_pr = True
					if pr_slot == 0xffff:
						pr_slot = int(field[3])
						max_slot = pr_slot
						min_slot = pr_slot
						stop_slot = pr_slot

				continue
			elif field[2] == 'bypassFlag':
				task_bypassFlag[0][task_id] = int(field[3])
				item_start = False
				if task_id == 19 and idx[task_id] == 0 and idx[18] == 0:
					#print("--2-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
					task_print(task_flag,task_bypassFlag,pr_slot)
					need_pr = False

		if need_pr == True:
			#print("--3-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
			task_print(task_flag,task_bypassFlag,pr_slot)
			need_pr = False
	print("--------------------------------------------")
	file.close()
	return

def cmd_welcome():
	print("|-----------------------------------------------|")
	print("|                                               |")
	print("|              ,%%%%%%%%,                       |")
	print("|            ,%%/\%%%%/\%%                      |")
	print("|           ,%%%\c \"\" J/%%%                     |")
	print("|  %.       %%%%/ o  o \%%%                     |")
	print("|  `%%.     %%%%    _  |%%%                     |")
	print("|   `%%     `%%%%(__Y__)%%'                     |")
	print("|   //       ;%%%%`\-/%%%'                      |")
	print("|  ((       /  `%%%%%%%'                        |")
	print("|   \\\\    .'          |                         |")
	print("|    \\\\  /       \  | |                         |")
	print("|     \\\\/         ) | |                         |")
	print("|      \         /_ | |__                       |")
	print("|      (___________)))))))一个不会写BUG的攻城湿 |")
	print("|                                               |")
	print("|-----------------------------------------------|")
	print("")
	
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
	elif field[0] == 'task':
		task_process(field)
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
		print("======")
		print("<CMD>task [-s] [slot num] [-p]")
		print(" -s  : display interval")
		print(" -p  : display prompt message")
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
	#cmd_welcome()
	while True:
		str = input("<cmd>")
		try:
			cmd_parse(str)
		except Exception:
			print(traceback.format_exc())  

if __name__ == '__main__':
	main()

