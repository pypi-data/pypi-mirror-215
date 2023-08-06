#!/usr/bin/env python3

from fire import Fire
import math

import numpy as np
import matplotlib.pyplot as plt


# https://en.wikipedia.org/wiki/Erlang_distribution#/media/File:Erlang_dist_cdf.svg
#num = input("Enter a number: ")
#print("The factorial of ", num, " is : ")
#print(math.factorial(int(num)))



# considerations
"""
 RUN 0057   1st minute -----------------------
 -  fit erlang exponential:
    1.07839e+01   ; slope    -8.96373e-02 +- 4.88916e-05
    TF1 *fa1 = new TF1("fa1","exp(1.07845e+01 -x*8.96373e-02)",0,40);

  from erlang:
   8.96946e+04 = 89 694 +- 49
   real is 85292, but if i multiply by unseen: 1.036*  => 88400 ... pretty close
   theory 51.9%DT;  caen gives 49.5%; 53.08 from adding


   RUN57 last minute ------------------

   observed rate 21546.1   theoretical from fit 21727.8 +- 38

 FCN=1199.32 FROM MIGRAD    STATUS=CONVERGED      47 CALLS          48 TOTAL
                     EDM=1.98023e-09    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     7.94577e+00   1.63577e-03   1.62246e-05   6.53063e-02
   2  Slope       -2.17278e-02   3.84162e-05   3.81054e-07   2.09419e+00

   the observed rate 21546 compensated on 0.986% of erlangblind = 21758.44356 - 21728 = 30...well in 1 sigma
  16.18% caen;   17.169 % from sum of 3


  a/  it seems i know rates, HOWEVER, here is a problem with double zeroes..maybe the peak
  b/  but if i do 1.5 - 4.48us window,
    - erlang says 6.021%,
    - root 6.16%
    - root with erlang 1.009 compensation ... 6.11%  PERFECT!
  THE PEAK....

"""



# probability density function   k==1 for my case
def erlang_pdf(x,rate,k=1):

    # lambda ^k    x^k-1   exp(-lambda x)
    res = np.power(rate,k )* np.power(x, k-1 )* np.exp(-rate*x)
    res = res/ math.factorial( int(k-1) )
    return res





# cumulative distribution function
def erlang_cdf(x,rate,k=1):
    return erlang_cum(x,rate,k=1)

def erlang_cum(x,rate,k=1):
    # in the test - i supply:   1/mu == rate
    res = 0
    for n in range(k):
        res+=1/math.factorial(int(n)) * np.exp(-rate*x)*np.power(x*rate,n)
        #print(f"                 n={n},  {res}")
        #res=math.exp(-rate*x)
    return 1 - res




#======================================== main ====== test
def main():
    print("Erlang_cum for rate 85000 at 8us:", erlang_cum(8e-6, 85000, 1) ," " )
    print("Erlang_cum for rate 85000 at 4.5us:", erlang_cum(4.5e-6, 85000, 1) ," " )
    print("Erlang_cum for rate 85000 at 0.4us:", erlang_cum(0.4e-6, 85000, 1) ," " )


    print("Erlang test image")
    x = np.linspace(0,20,50)

    y = erlang_cum( x, 1/2, 1 )    # mu in image == lambda here; k==k
    plt.plot(x,y,'r-')

    y = erlang_cum( x, 1/1, 9 )
    plt.plot(x,y,'b-')

    y = erlang_cum( x, 1/1, 1 )
    plt.plot(x,y,'m-')

    y = erlang_cum( x, 1/0.5, 7 )
    plt.plot(x,y,'k-')

    y = erlang_cum( x, 1/2, 3 )
    plt.plot(x,y,'y-')

    y = erlang_cum( x, 1/1, 5 )
    plt.plot(x,y,'g-')

    y = erlang_cum( x, 1/2, 2 )
    plt.plot(x,y,'-', color='orange')






    y = erlang_pdf( x, 1/2, 1 )    # mu in image == lambda here; k==k
    plt.plot(x,y,'r:')

    y = erlang_pdf( x, 1/1, 1 )
    plt.plot(x,y,'m:')

    y = erlang_pdf( x, 1/0.5, 7 )
    plt.plot(x,y,'k:')

    y = erlang_pdf( x, 1/2, 2 )
    plt.plot(x,y,':', color='orange')

    plt.margins(0.005, tight=True)
    plt.grid(True)
    plt.show()


    # for x in np.arange(0, 1.2,  0.2):
    #     print(f"{x:.1f}  (rate={rate})", erlang(x,rate))

if __name__=="__main__":
    Fire(main)
