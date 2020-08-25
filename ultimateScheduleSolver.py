"""
MATH 381 PROJECT 1: SCHEDULE FINDING
Jan 2020
This is the python script that generates the input
for the LP solver for the purpose of generating a
schedule solver.
"""
import os

N = 12 # number of total quarters
MAXCREDIT = 15 # maximum credit per quarter
APCREDITS = 20 # credit student bring to college from highscool
GRADCREDIT = 180
SMARTNESS = 7 - int(APCREDITS / 10)
allQuarters = range(1, N+1) # adjusted range for Python
fullCourseList = [] # list of course names
coursePrereqMap = {} # course name => list of course names
courseCrtMap = {} # course name => integer
courseCrtTypeMap = {} # course name => credit type
courseOfferingMap = {} # course name => list of booleans
creditTypes = ["VLPA", "QSR", "W", "CSELECTIVE", "MELECTIVE"] # all credits types
creditRequirement = {} # credit requirement of each credit type

def main():
    output = open("scheSolve.txt","w+")
    loadAllCourses()
    loadGradRequirement()
    objectiveF(output)
    constraint1(output)
    constraint2(output)
    constraint3(output)
    constraint4(output)
    constraint5(output)
    constraint6(output)
    constraint7(output)
    constraint8(output)
    constraint9(output)
    constraint10(output)
    constraint11(output)
    loadVaribles(output)
    output.close()
    # This command only works if you have lp_solve installed in the terminal
    print("Solving...")
    os.system("lp_solve -s scheSolve.txt > scheSolution.txt")
    getSolution()

# Add unnamed VLPA, QSR, W credits
def loadAllCourses():
    loadCoreCourses()
    for cr in range(1,6):
        for type in creditTypes[:-2]:
            for suffix in ["A", "B", "C", "D"]:
                name = type + str(cr) + suffix
                fullCourseList.append(name)
                courseCrtMap[name] = cr
                courseCrtTypeMap[name] = type
    # Currently we assume that all courses are offered every quarter
    for course in fullCourseList:
        courseOfferingMap[course] = [True, True, True]

# Load all CSE Core courses we consider
# Prerequisite map is not loaded yet
def loadCoreCourses():
    fileInput = open("courseCrtInfo.txt", "r")
    lines = fileInput.readlines()
    for line in lines:
        line = line.split("|")
        fullCourseList.append(line[0])
        if (len(line) > 2):
            courseCrtTypeMap[line[0]] = line[2][:-1]
            courseCrtMap[line[0]] = line[1]
        else:
            courseCrtMap[line[0]] = line[1][:-1]
    fileInput.close()

# Load the credit requirement for graduation
def loadGradRequirement():
    creditRequirement["VLPA"] = 20;
    creditRequirement["QSR"] = 5;
    creditRequirement["W"] = 10;
    creditRequirement["CSELECTIVE"] = 33;
    creditRequirement["MELECTIVE"] = 18;

# Objective Function
def objectiveF(f):
    objFun = ""
    for q in allQuarters:
        objFun += "y_%d + " % q
    f.write("min: " + objFun[:-3] + ";\n")

# Constraint 1
# Each quarter must be taken if and only if at least one
# credit is taken with some courses
def constraint1(f):
    for q in allQuarters:
        line = ""
        for c in fullCourseList:
            line += "x_%d_%s + " % (q, c)
        f.write(line[:-3] + " <= 20 y_%d;\n" % q)
        f.write("y_%d <= " % q + line[:-3] + ";\n")

# Constraint 2
# For each course, match with a variable indicating
# whether the course has been taken or not
def constraint2(f):
    for c in fullCourseList:
        line = ""
        for q in allQuarters:
            line += "x_%d_%s + " % (q, c)
        f.write(line[:-3] + " <= 20 z_%s;\n" % c)
        f.write("z_%s <= " % c + line[:-3] + ";\n")

# Constraint 3
# Each quarter must be used in order
def constraint3(f):
    for q in allQuarters[1:]:
        f.write("y_%d <= y_%d;\n" % (q, q-1))

# Constraint 4
# For each course, make sure that each course can only
# be taken if and only if it's offered in that particular
# quarter
def constraint4(f):
    for c in fullCourseList:
        for q in allQuarters:
            if (courseOfferingMap[c][(q-1) % 3]):
                f.write("r: x_%d_%s <= %d;\n" % (q, c, 1))
            else:
                f.write("r: x_%d_%s <= %d;\n" % (q, c, 0))

# Constraint 5
# For each course, make sure that each course can only
# be taken once (assuming student does not fail any courses)
def constraint5(f):
    for c in fullCourseList:
        line = ""
        for q in allQuarters:
            line += "x_%d_%s + " % (q, c)
        f.write(line[:-3] + " <= %d;\n" % 1)

# Constraint 6
# TODO: Prerequisite
def constraint6(f):
    fileInput = open("prereqLPInput.txt", "r")
    lines = fileInput.readlines()
    fileInput.close()
    for info in lines:
        info = info.split("|")
        course = info[0]
        prereqs = info[1][:-1]
        # Any course with a prereq cannot be taken in the first quarter
        f.write("r: x_%d_%s <= %d" % (1, course, 0) + ";\n")
        if "+" in prereqs:
            prereqs = prereqs.split("+")
            for q2 in allQuarters[1:]:
                line = "x_%d_%s <= " % (q2, course)
                for c in prereqs:
                    for q1 in allQuarters[:q2-1]:
                        line += "x_%d_%s + " % (q1, c)
                f.write(line[:-3] + ";\n")
        else:
            prereqs = prereqs.split(";")
            for q2 in allQuarters[1:]:
                for c in prereqs:
                    line = "x_%d_%s <= " % (q2, course)
                    for q1 in allQuarters[:q2-1]:
                        line += "x_%d_%s + " % (q1, c)
                    f.write(line[:-3] + ";\n")

# Constraint 7
# For each quarter, all courses cannot exceed the credit limit
def constraint7(f):
    for q in allQuarters:
        line = ""
        for c in fullCourseList:
            line += "%s x_%d_%s + " % (courseCrtMap[c], q, c)
        f.write(line[:-3] + " <= %d;\n" % MAXCREDIT)

# Constraint 8
# Each credit type requirement for graduation should be satisfied
# To do so we count credits from every course
def constraint8(f):
    for crtType in creditRequirement:
        line = ""
        for c in fullCourseList:
            if (c in courseCrtTypeMap and courseCrtTypeMap[c] == crtType):
                line += "%s z_%s + " % (courseCrtMap[c], c)
        f.write(line[:-3] + " >= %d;\n" % creditRequirement[crtType])
    line = ""
    for c in fullCourseList:
        line += "%s z_%s + " % (courseCrtMap[c], c)
    f.write(line[:-3] + " >= %d;\n" % (GRADCREDIT-APCREDITS))

# Constraint 9
# CSE MAJOR REQUIREMENT
# For the CSE major, you must take core courses
# TODO
def constraint9(f):
    fileInput = open("coreRequirement.txt", "r")
    lines = fileInput.readlines()
    for line in lines:
        line = line[:-1]
        f.write("r: z_%s" % line + " = %d;\n" % 1)
    fileInput.close()

# Constraint 10
# A student is not expected to take 400 level classes in freshman year
# unless his smartness is really good
def constraint10(f):
    for q in allQuarters[:SMARTNESS]:
        line = ""
        for c in fullCourseList:
            if (c.startswith("CSE4")):
                f.write("r: x_%d_%s = 0;\n" % (q, c))

# Constraint 11
# A student should not take more than 3 CSE courses each quarter
# A student should not take more than 5 courses in total each quarter
def constraint11(f):
    for q in allQuarters:
        line1 = ""
        line2 = ""
        for c in fullCourseList:
            line2 += "x_%d_%s + " % (q, c)
            if (c.startswith("CSE")):
                line1 += "x_%d_%s + " % (q, c)
        f.write(line1[:-3] + " <= 3;\n")
        f.write(line2[:-3] + " <= 5;\n")

# Load all variables in LP format
def loadVaribles(f):
    f.write("bin ")
    for q in allQuarters:
        for c in fullCourseList:
            f.write("x_%d_%s, " % (q, c))
    for c in fullCourseList:
        f.write("z_%s, " % c)
    str = ""
    for q in allQuarters:
        str += "y_%d, " % q
    f.write(str[:-2] + ";\n")

# This function only works if you have lp_solve installed in the terminal
def getSolution():
    usedQuarters = []
    classSchedule = []
    takenClasses = []
    f = open("scheSolution.txt","r")
    lines = f.readlines()
    if (len(lines) == 1):
        print("Problem is infeasible.")
        return
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
    print("\nStudent with %d AP credits graduated in %d quarters" % (APCREDITS, len(usedQuarters)))
    totalCredit = APCREDITS
    for q in allQuarters[:len(usedQuarters)]:
        currClass = ""
        if totalCredit < 45:
            currClass = "Freshman"
        elif totalCredit < 90:
            currClass = "Sophomore"
        elif totalCredit < 135:
            currClass = "Junior"
        else:
            currClass = "Senior"
        print("\nQuarter", q, currClass)
        credit = 0
        for c in classSchedule[q-1]:
            credit += int(courseCrtMap[c])
            print("%7s cr:" % c, courseCrtMap[c])
            #print("%7s" % c)
        totalCredit += credit
        print("Quarter credit: %d" % credit)
        print("Total credit: %d" % totalCredit)

if __name__ == "__main__":
    main()
