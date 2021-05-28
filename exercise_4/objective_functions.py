import numpy

#favouring PSO, e-02 (from -5 to 10)
def rosenbrock(var):
    tmp = 0
    for i in range(len(var)-1):
        tmp += 100*numpy.power(var[i+1]-numpy.power(var[i],2),2)+numpy.power(var[i]-1,2)
    return tmp

#Original objective function from last class
def sphere(var):
    return numpy.sum(numpy.square(var))

def salomon(var):
    var = numpy.array(var)
    return 1.0 - numpy.cos(2.0*numpy.pi*numpy.sqrt(sum(var**2.0))) + 0.1*numpy.sqrt(sum(var**2.0))

#e-15 but no big change after generation 800
'''def ackley_v1(var):
    l = len(var)
    f = numpy.zeros ( l )
    a = 20.0
    b = 0.2
    c = 0.2
    for j in range ( 0, l ):
        f[j] = - a * numpy.exp ( - b * numpy.sqrt ( numpy.sum ( numpy.square(var) ) / float ( l ) ) ) \
        - numpy.exp ( numpy.sum ( numpy.cos ( c * numpy.pi * numpy.array(var) ) ) / float ( l ) ) \
        + a + numpy.exp ( 1.0 )
    return numpy.sum(f)

#e-15 but no big change after generation 800
def ackley_v2(var):
    length = len(var)
    tmp1 = 20.-20.*numpy.exp(-0.2*numpy.sqrt(1./length*numpy.sum(numpy.square(var))))
    tmp2 = numpy.e-numpy.exp(1./length*numpy.sum(numpy.cos(numpy.array(var)*2.*numpy.pi)))
    return tmp1+tmp2

#Uhh yes, what???? So random.
def DeJongsF4(var):
    tmp = 0
    for i in range(len(var)):
        tmp += (i+1)*numpy.power(var[i],4)
    return tmp + numpy.random.normal(0, 1)

#Something might be wrong here
def sineenvelope(var):
    tmp = 0
    for i in range(len(var) - 1):
        tmp += 0.5 + ((numpy.power(numpy.sin(numpy.sqrt(numpy.power(var[i+1],2) + numpy.power(var[i],2)) - 0.5), 2)) / (numpy.power(1 + 0.001*(numpy.power(var[i+1],2) + numpy.power(var[i],2)), 2)))
    return -tmp

#Too many local minima, very hard, range -10.24 to 10.24
def whitley(var):
    tmp = 0.
    for i in range(len(var)):
        for j in range(len(var)):
            tmp2 = 100*numpy.power(numpy.power(var[i],2)-var[j], 2) + numpy.power(1.0-var[j],2)
            tmp += 1. + (numpy.power(tmp2, 2)/4000) - numpy.cos(tmp2)
    return tmp

#Favouring both optimization. from -10.24 to 10.24
def whitley_easier(var):
    tmp = 0.0
    for i in range(len(var)):
        for j in range(len(var)):
            tmp2 = 100.0*(numpy.power(var[i],2)-var[j]) + numpy.power(1.0-var[j],2)
            tmp += (numpy.power(tmp2, 2)/4000.0) - numpy.cos(tmp) + 1.0
    return tmp

#Something might be wrong here. from -2 to 2
def rosenbrockmodified(var):
    tmp = 0
    for i in range(len(var) - 1):
        tmp += 74 + (100*numpy.power(var[i+1]-numpy.power(var[i],2),2)+numpy.power(var[i]-1,2)) - 400*numpy.exp(-1*(numpy.power(var[i]+1, 2)+numpy.power(var[i+1]+1, 2))/0.1)
    return tmp

#Too easy for DE, from -20 to 20
def xinsheyang03(var):
    beta = 15
    m = 3
    X = numpy.array(var)
    scores = numpy.exp( -numpy.sum( numpy.power(X / beta, 2 * m)) ) - \
            ( 2 * numpy.exp( -numpy.sum( numpy.power(X, 2)) ) * numpy.prod( numpy.power( numpy.cos(X), 2 )) )
    return scores

#Too easy
def powellsum(var):
    tmp = 0
    for i in range(len(var)):
        tmp += numpy.power(numpy.abs(var[i]), i+2)
    return tmp

#Too easy
def xinsheyang04(var):
    tmp = ( numpy.sum( numpy.power( numpy.sin(var), 2 )) - numpy.exp( -numpy.sum( numpy.power(var, 2)) ) ) * \
            numpy.exp( -numpy.sum( numpy.power( numpy.sin( numpy.sqrt( numpy.abs(var) ) ), 2 )) )
    return tmp

#Too easy
def xinsheyang02(var):
    tmp1 = 0
    tmp2 = 0
    for i in range(len(var)):
        tmp1 += numpy.absolute(var[i])
        tmp2 += numpy.sin(numpy.power(var[i],2))
    return tmp1*numpy.exp(-tmp2)

#Too easy
def schwefel(var):
    tmp = 0
    for i in range(len(var)):
        tmp += var[i]*numpy.sin(numpy.sqrt(numpy.absolute(var[i])))
    return -tmp

#Too easy, interesting function tho, optimum change according to dimension
def michalewicz(var):
    m = 10
    tmp1 = 0
    for i in range(len(var)):
        tmp1 += numpy.sin(var[i])*numpy.power(numpy.sin((i+1)*numpy.power(var[i],2)/numpy.pi),2*m)
    return -tmp1

#Too easy for DE from -600 to 600
def griewank(var):
    tmp1 = 0
    tmp2 = 1
    for i in range(len(var)):
        tmp1 += numpy.power(var[i],2)
        tmp2 = tmp2*numpy.cos(var[i]/numpy.sqrt(i+1))
    return tmp1/4000-tmp2+1

#Too easy for DE
def weightedsphere(var):
    tmp = 0
    for i in range(len(var)):
        tmp += (i+1)*numpy.power(var[i],2)
    return tmp

#Too easy for DE
def ktablet(var):
    tmp = 0
    k = int(len(var)/4)
    for i in range(k):
        tmp += var[i]

    for i in range(k,len(var)):
        tmp += numpy.power(100*var[i],2)
    return tmp

#Too easy for DE
def ellipsoid(var):
    length = len(var)
    tmp = 0
    for i in range(length):
        tmp += numpy.power(numpy.power(1000,i/(length))*var[i],2)
    return tmp

#too Easy for DE
def sumofpower(var):
    tmp = 0
    for i in range(len(var)):
        tmp += numpy.power(numpy.absolute(var[i]),i+2)
    return tmp

#Too easy for DE
def rastrigin(var):
    #return -(20 + var[0]**2 + var[1]**2 - 10*(numpy.cos(2*numpy.pi*var[0]) + numpy.cos(2*numpy.pi*var[1])))
    #return 10 + numpy.sum([(x**2 - 10 * numpy.cos(2 * math.pi * x)) for x in var])
    tmp1 = 10 * len(var)
    tmp2 = 0
    for i in range(len(var)):
        tmp2 += numpy.power(var[i],2)-10*numpy.cos(2*numpy.pi*var[i])
    return tmp1+tmp2

#DE is done by gen 700
def zakharov(var):
    tmp1 = 0
    tmp2 = 0
    for i in range(len(var)):
        tmp1 += var[i]**2
        tmp2 += (i+1)*0.5*var[i]
    return tmp1+numpy.power(1/2*tmp2,2)+numpy.power(1/2*tmp2,4)'''
