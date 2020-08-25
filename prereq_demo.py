import re
import bs4
from urllib.request import urlopen as uReq
import mechanicalsoup

def getHtmlContent(url):
    page = uReq(url)
    return page.read()

def getCourses(html):
    html = html.decode('utf-8')
    nameReg = re.compile(r'Prerequisite.*courses\/CSE341')
    courses = re.findall(nameReg,html)
    trimed_result = []
    for str in courses:
        str = (str.split('<br')[0]).split(':')[1].lstrip()
        if (str.find('.') != -1):
            str = str.split('.')[0]
    print(str)
    return str

def outputCourses(courses):
    f = open("courses.txt","w+")
    for c in courses:
        f.write("CSE " + c.split('>')[1].split('<')[0] + "\r\n")

def main():
    url = 'https://www.washington.edu/students/crscat/cse.html'
    html = getHtmlContent(url)
    courses = getCourses(html)
    #outputCourses(courses)

if __name__ == '__main__':
    main()
