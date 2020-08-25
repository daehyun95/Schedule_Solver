
N = 12 # number of total quarters
MAXCREDIT = 15 # maximum credit per quarter
GRADCREDIT = 180
allQuarters = range(1, N+1) # adjusted range for Python
usedQuarters = []
classSchedule = []
takenClasses = []

f = open("scheSolution.txt","r")
lines = f.readlines()
for q in allQuarters:
    classSchedule.append([])
for line in lines:
    line = line.split()
    if(len(line) > 1 and line[1] == "1"):
        if(line[0].startswith("y")):
            usedQuarters.append(line[0].split("_")[1])
        elif(line[0].startswith("x")):
            data = line[0].split("_")
            classSchedule[int(data[1]) - 1].append(data[2])
        elif(line[0].startswith("z")):
            takenClasses.append(line[0].split("_")[1])
f.close()
print("Used quarters: ", usedQuarters)
for q in allQuarters:
    print("Quarter: ", q)
    for c in classSchedule[q-1]:
        print(c, " ")
    print("\n")
#print(takenClasses)
