import networkx as nx
in_file_name = 'simulate.trj'
out_file_name = 'reax_interface_npt.lammpstrj'
file_a = out_file_name+".out"
f = open(in_file_name, 'r')
fout_in = open(out_file_name, 'r')
fout_out = open(file_a, 'w')
line_stack = []

case_a = 0
case_b = 1
case_b_threshold = 6

case = case_a   # editable
bond_dist = 0.5 # editable

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
               if words[1] == '2': # Considering only the oxygen atom
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
timestamp = 81884000 # Doesn't matter
try:
   readandwrite(timestamp, [])
   arr =[]
   G=nx.Graph()
   while True:
       line = str(f.readline())
       num += 1
       #print str(num)
       if line[0]!=' ':
           if line.split()[0]=='step:':
               #print 'step', line.split()[1]
               timestamp = line.split()[1]
               #print 'readed timestamp', timestamp
               safe_start=False
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

               tmp=[]
               for item in Conn.connected_components(G):
                   if len(item)>=threshold:
                       tmp.extend(item)
               #print len(tmp)
               #print tmp
               readandwrite(timestamp, list(set(tmp)))
           G=nx.Graph()
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
