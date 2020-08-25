import re
import bs4
from urllib.request import urlopen as uReq
import mechanicalsoup

def getHtmlContent(url):
    page = uReq(url)
    return page.read()

def getCoursePrereq(html, num):
    html = html.decode('utf-8')
    nameReg = re.compile(r'Prerequisite.*courses\/CSE' + num)
    courseInfo = re.findall(nameReg,html)
    result = "";
    if (len(courseInfo) == 0):
        result = "MANUAL|CSE" + num + " NOT FOUND"
    for str in courseInfo:
        str = (str.split('<br')[0]).split(':')[1].lstrip()
        if (str.find('minimum') != -1):
            str = str.split('in ')[1]
        if (str.find('.') != -1):
            str = str.split('.')[0]
        if (len(str) == 7 or len(str) == 16):
            result = "CSE " + num + "|" + str
        else:
            result = "MANUAL|CSE " + num + "|" + str
    print(result)
    return result

def main():
    url = 'https://www.washington.edu/students/crscat/cse.html'
    input = open("courses.txt", "r")
    output1 = open("crtAutoRead.txt","w+")
    output2 = open("crtManualRead.txt","w+")
    courseName = input.readlines()
    html = getHtmlContent(url)
    for name in courseName:
        info = getCoursePrereq(html, name.split()[1])
        if (not info.startswith("MANUAL")):
            output1.write(info + "\n")
        else:
            output2.write(info + "\n")

if __name__ == '__main__':
    main()
