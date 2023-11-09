mylist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
removelist = []

for e in mylist:
	if e%3 == 0:
		removelist.append(e)

for e in removelist:
	mylist.remove(e)

print(mylist)