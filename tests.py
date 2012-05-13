#!/usr/bin/env python

def rot13(text=''):
    r = []
    la=ord('a')
    lz=ord('z')+1
    ua=ord('A')-1
    uz=ord('Z')+1
    for c in text:
        ordi=ord(c)
        if ordi>=la and ordi<lz :
            # r.join()
            r.append(chr(((ordi-la+13)%26)+la))
            #print r
        elif ordi>=ua and ordi<uz :
            # r.join()
            r.append(chr(((ordi-ua+13)%26)+ua))
        elif c =='&':
            r.append('&amp;')
        elif c =='<':
            r.append('&lt;')
        elif c =='>':
            r.append('&gt;')
        elif c =='"':
            r.append('&quot;')
        else:
            r.append(c)

    return ''.join(r)



print rot13('hOlA    &')
print rot13(rot13('hOLfasf  e & T la<h> "hol"'))