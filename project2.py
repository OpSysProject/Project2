'''
Zhiying Jiang, jiangz6
Tianyi Zhang, zhangt17
'''

import sys
import os


class Process:
	def __init__(self, id, size, arrival):
		self.id = str(id)
		self.size = int(size)
		self.times = len(arrival)
		self.arrival = [0] * len(arrival)
		self.depart = [0] * len(arrival)
		for i in range(len(arrival)):
			pair = arrival[i].split('/')
			self.arrival[i] = int(pair[0])
			self.depart[i] = int(pair[0]) + int(pair[1])

def printmem(mem):
	print("================================")
	for i in range(0, 8):
		for j in range(0, 32):
			print(mem[i * 32 + j], end = '')
		print()
	print("================================")

def room(mem):
	count = 0
	for i in range(256):
		if(mem[i] == '.'):
			count += 1
	return count

def add(mem, p, pos):
	i = 0
	while i < p.size:
		mem[pos + i] = p.id
		i += 1

def remove(mem, p):
	for i in range(256):
		if(mem[i] == p.id):
			mem[i] = '.'

def search_first_place(mem, p, pos):
	return pos

def next_fit(mem, plist):
	t = 0
	print("time " + str(t) + "ms: Simulator started (Contiguous -- Next-Fit)")
	done = 0
	count =0
	queue = []
	for p in plist:
		count += p.times
	pos = 0
	while done < count:
		for p in plist:
			for time in p.depart:
				if t == time and p.id in queue:
					remove(mem, p)
					done += 1
					queue.remove(p.id)
					print("time " + str(t) + "ms: Process " + p.id + " removed:")
					printmem(mem)
		for p in plist:
			for time in p.arrival:
				if t == time:
					print("time " + str(t) + "ms: Process " + p.id + " arrived (requires " + str(p.size) + " frames)")
					if(room(mem) < p.size):
						print("time "+ str(t) + "ms: Cannot place process " + p.id + " -- skipped!")
						done += 1
					elif(pos + p.size <256 and mem[pos + p.size] != '.'):
						pos = search_first_place(mem, p, pos)
						if pos == -1:
							print("time " + str(t) + "ms: Cannot place process " + p.id + " -- starting defragmentation")
							move_frame, move_process = defragmentation(mem, plist)
							for temp in plist:
								for a in temp.arrival:
									if a >= t:
										temp.arrival += move_frame
										temp.depart += move_frame
							t += move_frame
							print("time " + str(t) + "ms: Defragmentation complete (moved " + move_frame + " frames: " + move_process + ")")
						pos = search_first_place(mem, p, pos)
						queue.append(p.id)
						add(mem, p, pos)
						pos += p.size
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						printmem(mem)
					elif(pos + p.size >= 256):
						pos = search_first_place(mem, p, 0)
						if pos == -1:
							print("time " + str(t) + "ms: Cannot place process " + p.id + " -- starting defragmentation")
							move_frame, move_process = defragmentation(mem, plist)
							for temp in plist:
								for a in temp.arrival:
									if a >= t:
										temp.arrival += move_frame
										temp.depart += move_frame
							t += move_frame
							print("time " + str(t) + "ms: Defragmentation complete (moved " + move_frame + " frames: " + move_process + ")")
						pos = search_first_place(mem, p, pos)
						queue.append(p.id)
						add(mem, p, pos)
						pos += p.size
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						printmem(mem)
					else:
						queue.append(p.id)
						add(mem, p, pos)
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						pos += p.size
						if(pos >= 256):
							pos -= 256
						printmem(mem)
		t += 1
	t -= 1
	print("time " + str(t) + "ms: Simulator ended (Contiguous -- Next-Fit)\n")

def best_fit(mem, plist):
	t = 0
	print("time " + str(t) + "ms: Simulator started (Contiguous -- Best-Fit)")
	done = 0
	count =0
	queue = []
	for p in plist:
		count += p.times
	pos = 0
	while done < count:
		for p in plist:
			for time in p.depart:
				if t == time and p.id in queue:
					remove(mem, p)
					done += 1
					queue.remove(p.id)
					print("time " + str(t) + "ms: Process " + p.id + " removed:")
					printmem(mem)
		for p in plist:
			for time in p.arrival:
				if t == time:
					print("time " + str(t) + "ms: Process " + p.id + " arrived (requires " + str(p.size) + " frames)")
					if(room(mem) < p.size):
						print("time "+ str(t) + "ms: Cannot place process " + p.id + " -- skipped!")
						done += 1
					elif(pos + p.size <256 and mem[pos + p.size] != '.'):
						pos = search_first_place(mem, p, pos)
						if pos == -1:
							print("time " + str(t) + "ms: Cannot place process " + p.id + " -- starting defragmentation")
							move_frame, move_process = defragmentation(mem, plist)
							for temp in plist:
								for a in temp.arrival:
									if a >= t:
										temp.arrival += move_frame
										temp.depart += move_frame
							t += move_frame
							print("time " + str(t) + "ms: Defragmentation complete (moved " + move_frame + " frames: " + move_process + ")")
						pos = search_first_place(mem, p, pos)
						queue.append(p.id)
						add(mem, p, pos)
						pos += p.size
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						printmem(mem)
					elif(pos + p.size >= 256):
						pos = search_first_place(mem, p, 0)
						if pos == -1:
							print("time " + str(t) + "ms: Cannot place process " + p.id + " -- starting defragmentation")
							move_frame, move_process = defragmentation(mem, plist)
							for temp in plist:
								for a in temp.arrival:
									if a >= t:
										temp.arrival += move_frame
										temp.depart += move_frame
							t += move_frame
							print("time " + str(t) + "ms: Defragmentation complete (moved " + move_frame + " frames: " + move_process + ")")
						pos = search_first_place(mem, p, pos)
						queue.append(p.id)
						add(mem, p, pos)
						pos += p.size
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						printmem(mem)
					else:
						queue.append(p.id)
						add(mem, p, pos)
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						pos += p.size
						if(pos >= 256):
							pos -= 256
						printmem(mem)
		t += 1
	t -= 1
	print("time " + str(t) + "ms: Simulator ended (Contiguous -- Best-Fit)\n")

def defragmentation(mem):
	for i in range(256):
		if mem[i] == '.':
			pass

if __name__ == "__main__":
	if len(sys.argv)!=2:
		sys.exit("ERROR: Invalid arguments\nUsage: ./a.out <input-file>")
	plist = []
	input_file = os.getcwd()+'/'+sys.argv[1]
	try:
		f = open(input_file, 'r')
		for line in f:
			line = line.strip()
			if line and not line.startswith('#'):
				ele = line.split(' ')
				id = ele[0]
				size = ele[1]
				arrival = ele[2:]
				p = Process(id, size, arrival)
				plist.append(p)
		f.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")
	mem = []
	for i in range(256):
		mem.append('.')
	next_fit(mem, plist)
	best_fit(mem, plist)
