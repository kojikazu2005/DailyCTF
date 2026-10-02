a = 0
b = 0
c = 0
d = 0
e = 0
f = 0

for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                for e in range(10):
                     for f in range(10):
                        if (a-b>0 and c-d>0 and e-f>0):
                            if(a-3*a*b-b+c-3*c*d-d == e-3*e*f-f):
                                print(a,b,c,d,e,f) 
                                break
