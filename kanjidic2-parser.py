import xml.etree.ElementTree as ET
import sys
import os
from pprint import pprint as pp
import senddata

class Accumulator: pass


def print_element(el, index, acc=None, parent="TOP", depth=0, preds=""):
    if acc == None:
        acc = []
    children = el.getchildren()
    triple = {}
    if children:
        # print("    " * depth, el.tag, "has children.")
        depth = depth + 1
        parent = el.tag
        preds += "/" + parent
        for child in children:
            print_element(child, index, acc, parent, depth, preds)
    else:
        preds += "/" + el.tag
        triple["subject"] = index
        triple["predicate"] = preds
        triple["object"] = el.text
        acc.append(triple)
        # print("    " * depth, "Triple: ", triple)

def main():
    # file = "./kanjidic2/kanjidic2.xml.gz"
    file = "./jmdict/JMdict_e.gz"
    f = open(file, "r")
    tree = ET.parse(f)
    root = tree.getroot()
    print("Dictionary has %s entries" % len(root))
    # for index, value in enumerate(root):
    for index, value in enumerate(root):
        result = []
        print_element(value, index, acc=result)
        senddata.send_data(result)
        pp("Successfully inserted index %s" % index)
        # pp(result)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)