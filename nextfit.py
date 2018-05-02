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
	i = find_start(pos, mem)
	j = i
	while j < 256:
		if(mem[j] != '.'):
			break
		j += 1
	if j - i >= p.size:
		pos = i
	else:
		pass
	return pos

def find_next_free(mem, p, idx=0):
	mem_idx = -1
	unalloc_space = 0
	for i in range(256):
		check_index = (i + idx) % 256
		unalloc_space = get_unalloc_mem_size(mem, check_index)
		if p.size <= unalloc_space:
			mem_idx = check_index
			break
	return mem_idx, unalloc_space

def get_unalloc_mem_size(mem, idx=0):
	'''
	get size of free memory from index onward
	:param idx: index in memory
	:param memory: character array memory
	:return: size of free frame after idx
	'''
	len_unalloc = 0
	for i in range(idx, len(mem)):
		if mem[i] != '.':
			return len_unalloc
		len_unalloc += 1
	return len_unalloc

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
					else:
						pos = find_next_free(mem, p, pos)[0]
						if(pos == -1):
							print("time " + str(t) + "ms: Cannot place process " + p.id + " -- starting defragmentation")
							defrag_time, moved, movedlist = defragmentation(mem)
							update_time(plist, t, defrag_time)
							t += defrag_time
							print("time " + str(t) + "ms: Defragmentation complete (moved " + str(moved) + " frames: " + print_movedlist(movedlist) + ")")
							printmem(mem)
							pos = find_next_free(mem, p, pos)[0]
						queue.append(p.id)
						add(mem, p, pos)
						print("time " + str(t) + "ms: Placed process " + p.id + ":")
						pos += p.size
						if(pos >= 256):
							pos -= 256
						printmem(mem)
		t += 1
	print("time " + str(t - 1) + "ms: Simulator ended (Contiguous -- Next-Fit)\n")

def update_time(plist, t, defrag_time):
	for p in plist:
		for i in range(len(p.arrival)):
			if p.arrival[i] >= t:
				p.arrival[i] += defrag_time
				p.depart[i] += defrag_time
			elif p.depart[i] >= t:
				p.depart[i] += defrag_time
			else:
				continue

def print_movedlist(movedlist):
	string = ""
	for i in movedlist:
		string += i + ", "
	string = string[:-2]
	return string

def defragmentation(mem):
	defrag_time = 0
	moved = 0
	movedlist = []
	start = find_start(0, mem)
	end = find_end(start, mem)
	while end < len(mem):
		if end > 0 and start >= 0 and mem[end]!='.' and end > start:
			if mem[end] not in movedlist:
				movedlist.append(mem[end])
			mem[start] = mem[end]
			mem[end] = '.'
			start = find_start(start+1,mem)
			defrag_time +=1
			moved+=1
		end+=1
	return defrag_time, moved,movedlist

def find_start(s, mem):
	idx_start = -1
	for i in range(s, 256):
		if mem[i]=='.':
			idx_start = i
			return idx_start
	return idx_start

def find_end(idx_start, mem):
	idx_end = -1
	if idx_start!=-1:
		for idx_end in range(idx_start+1, 256):
			if mem[idx_end]!='.':
				return idx_end
	return idx_end

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
