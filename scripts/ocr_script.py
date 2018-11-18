import pytesseract
import re
from PIL import Image
import spacy_lib

from nesFun import isKeyWord, push, isEmpty, isPincode, printList, rearrageList, insertIntoDB
import pyreceipt

def check_keyword_limit(line, keyWords):
    counter = 0
    for word in keyWords:
        word = word.rstrip()
        if counter > 1:
            return True
        if word in line:
            counter += 1

    return False

def process_data(lines, keyWords):
    for line in lines:
        if check_keyword_limit(line, keyWords) == True:
            lines.remove(line)
            obj = spacy_lib.split_entity(line)
            lines += obj
            return obj
    
    return None



def mainFun(path):
    slist = []
    keyWords = []
    with open('keyword.txt', 'r') as fp:
        keyWords = (fp.readlines())
    
    lines = pyreceipt.call_tessaract(path)

    print('*******************LINES*******************')
    print(lines)

    new_lines = process_data(lines, keyWords)
    print('*******************NEW LINES*******************')
    print(new_lines)
    i = 0
    if new_lines != None:
        lines = new_lines

    while i < len(lines):

        word = re.split(":|-|~|#", lines[i])
        if isKeyWord(keyWords, word[0]):
            if (isEmpty(word[1])):
                i += 1
                while (i < len(lines)):
                    flag = False
                    word[1] += " " + lines[i]
                    str = lines[i].split(", ")
                    for fu in str:
                        if (isPincode(fu)):
                            flag = True
                            break

                    if flag:
                        break

                    i += 1
            push(slist, word)
        i += 1
    
    # lines = rearrageList(slist)

    return {'tessaract_output': lines,'data': slist}

