
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import math


  
# function that takes a rate and a time i and return the discount factor to time i
def d(i,rate):
  ## your code here ##
  di=(1/(1+rate)**i)
  ####################
  return di



"""Let's use our discount factors to present value, or "pv" a set of cash flows."""

def pv(cf,dcf):
  ## your code here
  pv=0
  for flow,discount in zip(cf,dcf):
    pv=pv+flow*discount
  ##
  return pv


# Function that if given rate to time i, and time i+1, and i, will cacluate the 
# forward disctount rate from time i to i+1
def fwd(i,ratei,rateiplus):  
  ## your code here. #########
  ## remember fwd0=rate[1]. ##
  if i==0:
     fwdi=rateiplus
  else:
    fwdi=((1+rateiplus)**(i+1))*((1+ratei)**-i)-1
  ############################
  return fwdi


## given rates and time t's get forwards ##
def rates2fwds(yc):
  tData={"t":yc['t']-1}
  fwds=pd.DataFrame(tData)

  # make a copy of our yc and define some values we can loop over 
  yc1=yc.copy()
  yc1['fwd']=''  
  yc1['rate1'] = yc1['rate'].shift(1)
  yc1['rate2'] = yc1['rate']

  for index, rates in yc1.iterrows():
    yc1['fwd'][index]=fwd(index,rates['rate1'],rates['rate2'])

  fwds['rate']=yc1['fwd']  
  return fwds



## given forwards generate correpsonding dcf's  ##
def fwds2dcf(fwds):
  tData={"t":fwds['t']+1}
  dcfs=pd.DataFrame(tData)

  dcfs['dcf']=[0]*10
  dcfDummy=1
  for index, fwd2 in fwds.iterrows():
    dcfDummy=dcfDummy/(1+fwd2['rate'])
    dcfs['dcf'][index]=dcfDummy
 
  return dcfs




"""Thios is what we call a dv01, change in value due to a .01% change in interest rates up. Notivce the value change is negative, which is what we expect for increasing rates.

If we have a standard trading instruments, say a $1MM par swaps at current market rates, all the way out for each year, we can generate the forwars sensitities for our basis instruments and compare them against
"""

## Get the discount curves that correspond to each indpependently perturbed 
## forward rate at each time step
def dDCF(fwds):
  delta=.0001
  fwdsC=fwds.copy()
  dDCF=fwds2dcf(fwdsC)
  dDCF['dDCF0']=fwds2dcf(fwds)['dcf']
  fwdsC['rate'][1]=fwdsC['rate'][1]+delta
  dDCF['dDCF1']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][2]=fwdsC['rate'][2]+delta
  dDCF['dDCF2']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][3]=fwdsC['rate'][3]+delta
  dDCF['dDCF3']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][4]=fwdsC['rate'][4]+delta
  dDCF['dDCF4']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][5]=fwdsC['rate'][5]+delta
  dDCF['dDCF5']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][6]=fwdsC['rate'][6]+delta
  dDCF['dDCF6']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][7]=fwdsC['rate'][7]+delta
  dDCF['dDCF7']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][8]=fwdsC['rate'][8]+delta
  dDCF['dDCF8']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][9]=fwdsC['rate'][9]+delta
  dDCF['dDCF9']=fwds2dcf(fwdsC)['dcf']

  #dDCF=pd.DataFrame({base,dDCF0})
  return dDCF


## using perturbed discount curves calculate the change in cashflow value pv() for each forward rate
def dFWDS(cashflows,ddcf):
  dFWD=ddcf[['t']]-1
  baseVal=pv(cashflows,ddcf['dcf'])
  dFWD1=[]
  dFWD1.append(pv(cashflows,ddcf['dDCF0'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF1'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF2'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF3'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF4'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF5'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF6'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF7'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF8'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF9'])-baseVal)

  dFWD['dFWD']=dFWD1


  #dFWD['dd']=ddcf['dDCF0']
   

  return dFWD

