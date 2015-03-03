import re
import sys
def main():
    str = """<title>hello*#$</title>\nsal\nssl:_:_:_:_:.-,<abstract>firstr</abstract>.././,.,.m,<>salsalsal<>\n<><abstract>salam</abstract>"""
    match = re.findall(r'<title>\n*(.+)\n*</title>[\W\w\n]*<abstract>\n*(.+)</abstract>',str)
    if match:
        print match
    else:
        print 'Not found'
if __name__ == '__main__':
    main()