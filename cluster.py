import networkx as nx
in_file_name = 'simulate.trj'
out_file_name = 'reax_interface_npt.lammpstrj'
atom_number = 576
case_a = 0
case_b = 1
case_c = 2
case_b_threshold = 6

case = case_c    # editable
bond_dist = 0.1  # editable
if (case == case_a):
    file_a = "cluster_casea.lammpstrj"
elif (case == case_b):
    file_a = "cluster_caseb.lammpstrj"
elif (case == case_c):
    file_a = "cluster_casec.lammpstrj"

f = open(in_file_name, 'r')
fout_in = open(out_file_name, 'r')
fout_out = open(file_a, 'w')
cluster_out = "cluster_result.out"
fout_result = open(cluster_out, 'w')
line_stack = []

f.readlines(38)
arr_f = f.readlines(atom_number-1)
oxygen_label = [0 for _ in range(0, atom_number)]
count = 0
for item in arr_f:
    a = item.split()
    if a[1] == '1':
        oxygen_label[count] = 1
    else:
        oxygen_label[count] = 0
    count += 1

fix_mode = False

def readandwrite(timestamp, arr):
	global fix_mode
	while True:
		tmp_position = fout_in.tell()
		line = fout_in.readline()
		print line, timestamp
		if line == 'ITEM: TIMESTEP\n':
		    fout_out.writelines(line)
		    fout_out.writelines(line_stack)
		    #print 'write', line_stack
		    line_stack[:]=[]
		    fix_mode = False
		    return ;
		elif line.strip() == timestamp:
		    line_stack.append(line)
		    fix_mode = False
		elif line.strip() == 'ITEM: ATOMS id type xs ys zs vx vy vz ix iy iz':
		    line_stack.append(line)
		    fix_mode=True
		elif fix_mode:
		    words = str(line).split()
		    if words[0] in arr:
		        #if words[1] == '2':
		        words[1]='3'
		        line_stack.append(' '.join(words)+'\n')
		    else:
		        line_stack.append(line)
		else:
		    line_stack.append(line)
safe_start = True
start_line = False
cnt = 0
num = 0
timestamp = 81884000
def initGraph(case):
    if case<2:
        return nx.Graph()
    else:
        return nx.DiGraph()
try:
   readandwrite(timestamp, [])
   arr =[]
   G=initGraph(case)
   while True:
       line = str(f.readline())
       num += 1
       #print str(num)
       if line[0]!=' ':
           if line.split()[0]=='step:':
               #print 'step', line.split()[1]
               timestamp = line.split()[1]
               #print 'readed timestamp', timestamp
               safe_start = False
               #raw_input()
           if safe_start:
               continue
           if not start_line:
               pass
           else:
               start_line = False
               cnt+=1
               #print cnt
           Conn = nx.connected
           if(len(G.nodes())!=0):
               if case==case_a:
                   threshold = len(max(Conn.connected_components(G), key=len))
               elif case==case_b:
                   threshold = case_b_threshold
               elif case==case_c:
                   threshold_val = len(max(nx.simple_cycles(G), key=len))
                   threshold = max(threshold_val, 3)
               if (case < 2): max_length = len(max(Conn.connected_components(G), key=len))
               else: max_length = len(max(nx.simple_cycles(G), key=len))
               cluster_length = str(timestamp) + ' ' + str(max_length) + '\n'
               fout_result.write(cluster_length)
               tmp=[]
               if (case < 2):
                   for item in Conn.connected_components(G):
                       if len(item)>=threshold:
                           tmp.extend(item)
               else:
                   for item in nx.simple_cycles(G):
                       if len(item)>=threshold:
                           tmp.extend(item)
               #print len(tmp)
               #print tmp
               readandwrite(timestamp, list(set(tmp)))
           G=initGraph(case)
           arr=[]
       else:
           #print line
           if not start_line:
               start_line = True
           else:
               pass
           item = line.split()
           try:
               if float(item[3])>bond_dist:
                   arr.append({"src":item[0], "dest":item[1]})
                   G.add_edge(item[0], item[1])
                   G.add_edge(item[1], item[0])
           except IndexError as e:
               print e.message
except EOFError as e:
   print e.message
except IndexError as e:
   print e.message
except KeyboardInterrupt as e:
   fout_out.close()
   print 'saved'
finally:
   print len(arr)
