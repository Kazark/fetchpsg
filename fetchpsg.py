#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Kazark
Created: July 29 09
Modified: Sept 7 10
Version: 0.2.8
Purpose: To extract verses from a text file from UnboundBibles.com
'''

## Python
from codecs import open
## Pinson
from configfile import readcfg

SRC_TXTS_CFG = "srctxts.cfg"

class fpDataNode:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
    def __unicode__(self):
        return unicode(self.parent[0].data)
    def __eq__(self, other):
        return self.data == other
        
class fpListNode(list):
    def __init__(self, iterable):
        list.__init__(self)
        for i in iterable:
            self.append(fpDataNode(self, i))


# TODO add apocryphal books
_books = [('Genesis', 'Gen', 'Gn', '01O'),
         ('Exodus', 'Ex', '02O'),
         ('Leviticus', 'Lev', 'Lv', '03O'),
         ('Numbers', 'Num', '04O'),
         ('Deuteronomy', 'Deut', 'Dt', '05O'),
         ('Joshua', 'Josh', 'Jsh', '06O'),
         ('Judges', 'Jdg', '07O'),
         ('Ruth', '08O'),
         ('1 Samuel', '1 Sam', '1 Sa', '09O'),
         ('2 Samuel', '2 Sam', '2 Sa', '10O'),
         ('1 Kings', '1 Ki', '11O'),
         ('2 Kings', '2 Ki', '12O'),
         ('1 Chronicles', '1 Chr', '1 Ch', '13O'),
         ('2 Chronicles', '2 Chr', '2 Ch', '14O'),
         ('Ezra', 'Ezr', '15O'),
         ('Nehemiah', 'Ne', '16O'),
         ('Esther', 'Es', '17O'),
         ('Job', '18O'),
         ('Psalms', 'Ps', '19O'),
         ('Proverbs', 'Prov', '20O'),
         ('Ecclesiastes', 'Ec', 'Eccl', '21O'),
         ('Song of Solomon', 'SoS', 'SS', '22O'),
         ('Isaiah', 'Is', '23O'),
         ('Jeremiah', 'Jer', '24O'),
         ('Lamentations', 'Lam', '25O'),
         ('Ezekiel', 'Eze', '26O'),
         ('Daniel', 'Dan', '27O'),
         ('Hosea', 'Hos', '28O'),
         ('Joel', '29O'),
         ('Amos', '30O'),
         ('Obadiah', '31O'),
         ('Jonah', '32O'),
         ('Micah', '33O'),
         ('Habakkuk', 'Hab', '34O'),
         # TODO fix book numbers
         ('Zechariah', 'Zch', '38O'),
         # TODO fill in missing books!
         ('Matthew', 'Matt', 'Mt', '40N'), 
         ('Mark', 'Mk', '41N'), 
         ('Luke', 'Lk', '42N'), 
         (u'Κατά Ἰωάννην', 'John', 'Jn', '43N'), 
         ('Acts', '44N'), 
         ('Romans', 'Rom', '45N'), 
         ('1 Corinthians', '1 Cor', '1 Co', '46N'), 
         ('2 Corinithinas', '2 Cor', '2 Co', '47N'), 
         ('Galatians', 'Gal', '48N'),
         ('Ephesians', 'Eph', '49N'),
         ('Philippians', 'Phil', 'Phlp', '50N'),
         ('Colossians', 'Col', '51N'),
         ('1 Thessalonians', '1 Th', '1 Thess', '52N'),
         ('2 Thessalonians', '2 Th', '2 Thess', '53N'),
         ('1 Timothy', '1 Ti', '1 Tim', '54N'),
         ('2 Timothy', '2 Ti', '2 Tim', '55N'),
         ('Titus', 'Ti', '56N'),
         ('Philemon', 'Phlm', '57N'),
         ('Hebrews', 'Heb', '58N'),
         ('James', 'Jas', 'Jms', '59N'),
         ('1 Peter', '1 Pet', '1 Pt', '60N'),
         ('2 Peter', '2 Pet', '2 Pt', '61N'),
         ('1 John', '1 Jn', '62N'),
         ('2 John', '2 Jn', '63N'),
         ('3 John', '3 Jn', '64N'),
         ('Jude', 'Jud', '65N'),
         ('Revelation', 'Rev', '66N')]

books = []
for b in _books:
    for n in fpListNode(b):
        books.append(n)
del _books

superscript = {'1': u'¹', '2': u'²', '3': u'³', '4': u'⁴', '5': u'⁵', 
               '6': u'⁶', '7': u'⁷', '8': u'⁸', '9': u'⁹', '0': u'⁰'}

def _cmpvv(v1, v2):
    x = cmp(v1[0], v2[0])
    if x != 0:
        return x
    x = cmp(int(v1[1]), int(v2[1]))
    if len(v1) == 2 or x != 0:
       return x
    return cmp(int(v1[2]), int(v2[2]))
    

def getvv(fpath, v1, v2=None):
    try:
        ix = books.index(v1[0])
    except ValueError:
        raise ValueError, 'invalid book name.'
    v1[0] = books[ix].parent[-1].data # WARNING - cheaty code!
    del ix
    if v2 == None:
        v2 = v1
    else:
        try:
            ix = books.index(v2[0])
        except ValueError:
            raise ValueError, "invalid book name."
        v2[0] = books[ix].parent[-1].data # WARNING - cheaty code!
        del ix
    f = open(fpath, 'r', 'utf8')
    lastl = ['', '', '', '', '', '']
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\t')

        if _cmpvv(line[:len(v2)], v2) == 1:
            break
        elif _cmpvv(line[:len(v1)], v1) >= 0:
            ## book or chapter change
            if lastl[0] != line[0] or lastl[1] != line[1]:
                yield u'%s %s\n' % (books[books.index(line[0])], line[1])
            ## superscripted verse number + verse text
            yield u''.join([superscript[c] for c in line[2]]) + line[5]
            lastl = line
    return
        
def main(src, v1, v2=None):
    v1 = v1.split(':')
    if v2 != None:
        v2 = v2.split(':')
        # TODO Should check for bogus inputs...

    f = file(SRC_TXTS_CFG)
    fpath = readcfg(f)[src]
    f.close()

    for line in getvv(fpath, v1, v2):
        print line,
        
if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
