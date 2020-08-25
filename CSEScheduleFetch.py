import re
import bs4
from urllib.request import urlopen as uReq
import mechanicalsoup

# 根据url获取网页html内容
def getHtmlContent(url):
    page = uReq(url)
    return page.read()

# 从html中解析
def getCourses(html):
    html = html.decode('windows-1252')
    # 正则
    nameReg = re.compile(r'xl\d*093.*[1234]\d{2}.*<\/td>')
    # 解析出jpg的url列表
    courses = re.findall(nameReg,html)
    return courses

# 批量下载图片，默认保存到当前目录下
def outputCourses(courses):
    f = open("courses.txt","w+")
    for c in courses:
        f.write("CSE" + c.split('>')[1].split('<')[0] + "\r\n")

def main():
    url = 'https://s3-us-west-2.amazonaws.com/www-cse-public/education/time-sched/teaching2019-2020.html'
    html = getHtmlContent(url)
    courses = getCourses(html)
    outputCourses(courses)

if __name__ == '__main__':
    main()
