def conParen():
    tupla = (1, 2, 3, 4, 5)
    print(tupla)
    print(type(tupla))

def sinParen():
    tupla = 1, 2, 3, 4, 5
    print(tupla)
    print(type(tupla))

def empty():
    tupla = ()
    print(tupla)
    print(type(tupla))

def tupOneElem():
    tupla = (1,)
    print(tupla)
    print(type(tupla))

def NestedTule():
    # Code for creating nested tuples
    tuple1 = (0, 1, 2, 3, 4)
    tuple2 = ('Python', 'C++', 'C#', 'F#', 'Haskell')
    tuple3 = (tuple1, tuple2)
    print(tuple3)

def exampleConcat():
    t1 = ('this', 'world', 'game')
    t2 = ('bit', 'code', 'terminal')
    t3 = t1 + t2
    print(t3)

def repeticion():
    tupla = ('Python',)*5
    print(tupla)

def testInmutableTupla():
    #code to test that tuples are immutable
    tupla = (-8, 1, 12, 3)
    tupla[1] = 2
    print(tupla)

def slicingExample1():
    tupla = (12, 3, 45, 4, 2.4, 2, 56, 90, 1)
    print(tupla[1:3])
    print(tupla[:4])
    print(tupla[3:])
    print(tupla[:])
    print(tupla[::2])
    print(tupla[-3:-1])

def eliminarTula():
    # Code for deleting a tuple
    tupla = (0, 1)
    del tupla
    print(tupla)

def accederElem():
    tupla = (1, 2, 3)
    print(tupla[1])

def distintosTipos():
    tupla = ("cat", 1, (1,2), "dog", 20.4)
    print(tupla)

def multOutput(n: int):
    if n%2 == 0:
        return 2*n, 3*n
    return n*n, n + n


conParen()
sinParen()
empty()
tupOneElem()
NestedTule()
exampleConcat()
repeticion()

slicingExample1()
# eliminarTula()
accederElem()
distintosTipos()

print(multOutput(5))
