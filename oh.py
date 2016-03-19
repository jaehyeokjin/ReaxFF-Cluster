f=open('simulate.trj','r')
f.readlines(38)
arr = f.readlines(575)
for item in arr:
    a = item.split()
    if a[1]=='1':
        print 'O'
    else:
        print 'H'
