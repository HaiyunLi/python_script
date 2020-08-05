import os
import re
import traceback
import sys
import ctypes
from ctypes import *

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

class COORD(Structure):
	_fields_ = [('X', c_short), ('Y', c_short)]

class SMALL_RECT(Structure):
	_fields_ = [('Left', c_short),
				('Top', c_short),
				('Right', c_short),
				('Bottom', c_short),
				]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
	_fields_ = [('dwSize', COORD),
				('dwCursorPosition', COORD),
				('wAttributes', c_uint),
				('srWindow', SMALL_RECT),
				('dwMaximumWindowSize', COORD),
				]

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
csbiInfo = CONSOLE_SCREEN_BUFFER_INFO()
ctypes.windll.kernel32.GetConsoleScreenBufferInfo(std_out_handle, byref(csbiInfo));
wOldColorAttrs = csbiInfo.wAttributes;

def set_cmd_text_color(color, handle=std_out_handle):
	sys.stdout.flush()
	Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
	return Bool

#reset white
def resetColor(handle=std_out_handle):
	sys.stdout.flush()
	Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, wOldColorAttrs)
	return Bool

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
	key_list = []
	interval_flag = False
	interval_time = 0
	ticks_cur = 0
	ticks_prv = 0
	pr_nomagic = False
	pr_nofunc = False
	pr_noticks = False
	pr_verbose = False
	key_world = []
	key_str = []
	key_vlaue = [0xffff for col in range(20)]
	key_flag = False
	index = 0
	pr_str = ''
	pr_flag = False

	while idx < len(arg):
		if arg[idx] == "-m":
			magic_list = arg[idx+1].split("&")
			if len(magic_list) < 1:
				print("ERROR: magic_list parameter error !!! cnt:%d" % len(magic_list))
				return
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
		elif arg[idx] == "-k":
			key_list = arg[idx+1].split(",")
			if len(key_list) > 20:
				print("ERROR: key_list parameter error !!! cnt:%d" % len(key_list))
				return 
			idx = idx + 2
		else:
			print("ERROR:parameter error !!! arg[%d]:%s" % (idx,arg[idx]))
			return
	
	i = 0
	if len(key_list) > 0:
		key_flag = True
		for key in key_list:
			key_world = key.split("=")
			key_str.append(key_world[0])
			if len(key_world) > 1:
				key_vlaue[i] = int(key_world[1])
			i = i + 1

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
			if pr_flag == True:
				print("%s" % pr_str)

			pr_flag = False
			pr_str = ''

			if pr_noticks == False:
				if interval_flag == False:
					pr_str = pr_str + "<%s>"%field[0]
				else:
					ticks_cur = int(field[0]);
					if ticks_prv == 0:
						ticks_prv = ticks_cur
					interval_time = (ticks_cur - ticks_prv)*1000000/cpu_frequence
					pr_str = pr_str + "[%6dus]<%s>"%(interval_time,field[0])
					ticks_prv = ticks_cur

			if pr_nomagic == False:
				pr_str = pr_str + "m:%s"%field[4]
			if pr_nofunc == False:
				pr_str = pr_str + " f:%-20s"%field[2][-20:]
			pr_str = pr_str + "|"
			item_pr = item_pr + 1
			if key_flag != True:
				pr_flag = True
		elif item_pr < 7 and item_pr > 0:
			if key_flag == True:
				if field[2] in key_str:
					index = key_str.index(field[2])
					if (key_vlaue[index] == int(field[3])) or (key_vlaue[index] == 0xffff):
						pr_flag = True

			if pr_verbose == False:
				pr_str = pr_str + "%15s:%-10s|"%(field[2][-15:],field[3])
				item_pr = item_pr + 1
			else:
				pr_str = pr_str + " %s:%s |"%(field[2][-15:],field[3])

	if pr_flag == True:
		print("%s" % pr_str)
	file.close()
	return

def task_print(flag,bypassFlag,slot,ticks):
	idx = 0
	task_id =0

	print("\r\n---- slot:%-5d end_ticks:%ld -----------------" % (slot,ticks))
	print("idx  0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19",end="")
	for idx in range(0,2):
		print("\r\n %d " % idx,end="")
		for task_id in range(0,20):
			if flag[idx][task_id] == True:
				pr_temp = 'Y'
				set_cmd_text_color(FOREGROUND_GREEN|(wOldColorAttrs&0xf0))
				print(" %s" % pr_temp,end="")
				resetColor()
				print("/",end="")
				if bypassFlag[idx][task_id] == 1:
					set_cmd_text_color(FOREGROUND_RED|(wOldColorAttrs&0xf0))
				print("%d " % bypassFlag[idx][task_id],end="")
				resetColor()
			else:
				pr_temp = 'N'
				set_cmd_text_color(FOREGROUND_DARKGRAY|(wOldColorAttrs&0xf0))
				print(" %s/- " % pr_temp,end="")
				resetColor()
	print("")
	return

def task_prompt():
	set_cmd_text_color(FOREGROUND_RED|(wOldColorAttrs&0xf0))
	print("\r\nDL dependence:")
	resetColor()
	print("             |-->PDSCH_TB(1)")
	print(" CONFIG(0)-->|-->PDSCH_RS_GEN(4)    |-->PDSCH_SYMBOL_TX(3)|")
	print("             |-->CONTROL_CHANNELS(5)|-------------------->|-->DL_POST(18)")
	set_cmd_text_color(FOREGROUND_RED|(wOldColorAttrs&0xf0))
	print("\r\nUL dependence:")
	resetColor()
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
	set_cmd_text_color(FOREGROUND_RED|(wOldColorAttrs&0xf0))
	print('Confirm cmd:',end="")
	resetColor()
	print(' cat var.txt | grep "tasksf,[slot_id]" -B 2 -A 1 | grep "taskId\|bypassFlag"\r\n')
	return
	
def task_process(arg):
	item_start = False
	prompt_flag = False
	need_pr = False
	task_bypassFlag = [[0 for col in range(20)] for row in range(2)]
	#task_bypassFlag = [[0]*20]*2 不能这样用，见 https://www.cnblogs.com/woshare/p/5823303.html
	task_flag = [[False for col in range(20)] for row in range(2)]
	idx = [0 for col in range(20)]
	slot_list = []
	task_id = 0
	cur_slot = 0xffff
	pr_slot = 0xffff
	cur_ticks = 0xffff
	pr_ticks = 0xffff
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
		elif arg[i] == "-h":
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
	print('Magic world:0x10203040')
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
			idx[m] = 1
			for n in range(0,2):
				task_bypassFlag[n][m] = 0
				task_flag[n][m] = False

		for line in all_lines[-check_count:]:
			field = line.split(",")
			if len(field) != 6:
				continue
			if field[1] == "0" and field[4] in re_condition:
				cur_ticks = int(field[0])
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
						task_print(task_flag,task_bypassFlag,pr_slot,pr_ticks)
						need_pr = False
					item_start = False
				else:
					#print("--10- need_pr:%d cur_slot:%d pr_slot:%d idx[%d]:%d task_flag[%d][%d]:%d %d" % (need_pr,cur_slot,pr_slot,task_id,idx[task_id],idx[task_id],task_id,task_flag[idx[task_id]][task_id],task_flag[idx[task_id]^1][task_id]))
					idx[task_id] = idx[task_id]^1
					task_flag[idx[task_id]][task_id] = True
					#print("--1-- need_pr:%d cur_slot:%d pr_slot:%d idx[%d]:%d task_flag[%d][%d]:%d %d" % (need_pr,cur_slot,pr_slot,task_id,idx[task_id],idx[task_id],task_id,task_flag[idx[task_id]][task_id],task_flag[idx[task_id]^1][task_id]))
					need_pr = True
					pr_ticks = cur_ticks
					if pr_slot == 0xffff:
						pr_slot = int(field[3])
						max_slot = pr_slot
						min_slot = pr_slot
						stop_slot = pr_slot

				continue
			elif field[2] == 'bypassFlag':
				task_bypassFlag[idx[task_id]][task_id] = int(field[3])
				item_start = False
				if task_id == 19 and idx[task_id] == 1 and idx[18] == 1:
					#print("--2-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
					task_print(task_flag,task_bypassFlag,pr_slot,pr_ticks)
					need_pr = False

		if need_pr == True:
			#print("--3-- need_pr:%d cur_slot:%d pr_slot:%d task_id:%d" % (need_pr,cur_slot,pr_slot,task_id))
			task_print(task_flag,task_bypassFlag,pr_slot,pr_ticks)
			need_pr = False
	print("------------------------------------------------------")
	file.close()
	return

def sym_print(pr_nSlotIdx,pr_frame,pr_subframe,pr_slot,sym):
	nCellIdx = 0;

	for nCellIdx in range(0,2):
		print('|  %6d  | %5d |  %2d  |  %2d  |  %2d  |' % (pr_nSlotIdx,pr_frame,pr_subframe,pr_slot,nCellIdx),end="")
		for i in range(0,7):
			if sym[nCellIdx][i] == True:
				pr_temp = 'Y'
				set_cmd_text_color(FOREGROUND_GREEN|(wOldColorAttrs&0xf0))
				print("   %s   " % pr_temp,end="")
				resetColor()
			else:
				pr_temp = 'N'
				set_cmd_text_color(FOREGROUND_DARKGRAY|(wOldColorAttrs&0xf0))
				print("   %s   " % pr_temp,end="")
				resetColor()
			if i != 6:
				print(" ",end="")
		print("|")
	print('-------------------------------------------------------------------------------------------------')
	
	return

def sym_prompt():
	set_cmd_text_color(FOREGROUND_RED|(wOldColorAttrs&0xf0))
	print('Confirm cmd:',end="")
	resetColor()
	print(' cat var.txt |grep "0xBCBCBCBC" -A 7| grep "nCellIdx,[nCellIdx_id]" -A 6 | grep "nSlotIdx,[nSlotIdx_id]" -B 2 | grep "sym"\r\n')
	return

def sym_process(arg):
	item_start = False
	check_count = 0
	slot_list = []
	i = 1
	nCellIdx = 0
	frame = 0
	subframe = 0
	slot = 0
	nSlotIdx = 0xffff
	pr_frame = 0xffff
	pr_subframe = 0xffff
	pr_slot = 0xffff
	pr_nSlotIdx = 0xffff
	sym = [[False for col in range(7)] for row in range(2)]
	cur_sym = 0
	slot_flag = False

	while i < len(arg):
		if arg[i] == "-s":
			slot_list = arg[i+1].split("&")
			i = i + 2
			slot_flag = True
		elif arg[i] == "-n":
			check_count = int(arg[i+1])
			i = i + 2
		elif arg[i] == "-h":
			sym_prompt()
			return
		else:
			print("ERROR:parameter error !!! arg[%d]:%s" % (i,arg[i]))
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

	re_condition = '0xBCBCBCBC'
	print('Magic world:0xBCBCBCBC')
	print('-------------------------------------------------------------------------------------------------')
	print('| nSlotIdx | frame | subf | slot | cell | sym0  | sym2  | sym4  | sym6  | sym8  | sym10 | sym12 |')
	print('-------------------------------------------------------------------------------------------------')
	
	i = 0
	while True:
		if 0 == len(slot_list) and i == 1:
			break
		if i == len(slot_list) and slot_flag == True:
			break
		
		for line in all_lines[-check_count:]:
			field = line.split(",")
			if len(field) != 6:
				continue
			if field[1] == "0" and field[4] in re_condition:
				cur_ticks = int(field[0])
				item_start = True
			elif item_start != True:
				continue

			if field[2] == 'nCellIdx':
				nCellIdx = int(field[3])
				continue
			elif field[2] == 'frame':
				if pr_frame == 0xffff:
					pr_frame = frame
				frame = int(field[3])
				continue
			elif field[2] == 'subframe':
				if pr_subframe == 0xffff:
					pr_subframe = subframe
				subframe = int(field[3])
				continue
			elif field[2] == 'slot':
				if pr_slot == 0xffff:
					pr_slot = slot
				slot = int(field[3])
				continue
			elif field[2] == 'sym':
				cur_sym = int(field[3])
				continue
			elif field[2] == 'nSlotIdx':
				nSlotIdx = int(field[3])
				if pr_nSlotIdx == 0xffff:
					pr_nSlotIdx = nSlotIdx
				if slot_flag == True:
					if field[3] == slot_list[i]:
						pr_nSlotIdx = nSlotIdx
						pr_frame = frame
						pr_subframe = subframe
						pr_slot = slot
					else:
						continue
				if pr_nSlotIdx != nSlotIdx:
					sym_print(pr_nSlotIdx,pr_frame,pr_subframe,pr_slot,sym)
					pr_nSlotIdx = nSlotIdx
					pr_frame = frame
					pr_subframe = subframe
					pr_slot = slot
					
					#-------- 清空上一个slot标记 --------
					for m in range(0,7):
						for n in range(0,2):
							sym[n][m] = False

				sym[nCellIdx][int(cur_sym/2)] = True
				item_start = False
		i = i+1
		sym_print(pr_nSlotIdx,pr_frame,pr_subframe,pr_slot,sym)

		#-------- 清空上一个slot标记 --------
		for m in range(0,7):
			for n in range(0,2):
				sym[n][m] = False

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
	elif field[0] == 'sym':
		sym_process(field)
	elif field[0] == 'h':
		print("Usage:")
		print("---------------")
		print("<CMD>dma [-n] [count] [-s] [-nod]")
		print(" -s  : select slot to display")
		print(" -nod: don't display slot data")
		print("======")
		print("<CMD>loop [-n] [count] [-t]")
		print("======")
		print("<CMD>get -m magic_word [-n] [count] [-t] [-not] [-nom] [-nof] [-k] [key_world=walue,key_world=walue]")
		print(" -t  : display interval")
		print(" -not: don't display interval")
		print(" -nom: don't display magic world")
		print(" -nof: don't display function")
		print("   -k: select key world")
		print("======")
		print("<CMD>task [-n] [count] [-s] [slot num] [-h]")
		print(" -s  : display interval")
		print(" -h  : display prompt message")
		print("======")
		print("<CMD>sym [-n] [count] [-s] [slot num] [-h]")
		print(" -s  : display interval")
		print(" -h  : display prompt message")
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

