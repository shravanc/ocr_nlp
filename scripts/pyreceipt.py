from pyreceipts.receipt import Receipt
import sys


def read_recepipt(file_name):
    receipt = Receipt(file_name)
    text = receipt.read()
    receipt.delete_tmp_file()

    lines = []
    for s in text.split("\n"):
        if s:
            lines.append(s)


    print(lines)
    return lines
    return ''
    return text



def call_tessaract(image_path):
    lines = read_recepipt(image_path)
    return lines

"""
if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print(ValueError('No filename provided'))
    else:
        lines = read_recepipt(sys.argv[1])
        print(lines)
        return lines
"""
