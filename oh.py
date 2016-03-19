f = open('simulate.trj', 'r')
f.readlines(38)
arr = f.readlines(575)
oxygen_label = [0 for _ in range(0, 576)]
count = 0
for item in arr:
    a = item.split()
    if a[1] == '1':
        oxygen_label[count] = 1
    else:
        oxygen_label[count] = 0
    count += 1
