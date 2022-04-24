#import stuff
import pandas as pd
import numpy as np

#Analysis Macro
#Vars To Calculate - Mean and Median FICO, Occupancy Distribution, Purchase/Refi Split, Mean and Median DTI and LTV, Mean and Median Interest Rate, Mean and Median UPB, 60/90/120 Rates, Brwr Cnt
def analyze(msa):
    base = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_analysis_set.csv")
    base['fico'] = np.where(base['Cbrwr Fico'].isnull(), base['Brwr Fico'], np.where(base['Brwr Fico'].isnull(), base['Cbrwr Fico'], np.where(base['Brwr Fico'] > base['Cbrwr Fico'], base['Cbrwr Fico'], base['Brwr Fico'])))

    base['ever 60'] = np.where(base['Month of First 60'].isnull(), 0, 1)
    base['ever 90'] = np.where(base['Month of First 90'].isnull(), 0, 1)
    base['ever 120'] = np.where(base['Month of First 120'].isnull(), 0, 1)

    base['year'] = base['Orig Dt'].astype(str).str[-4:].astype(int)
    base['month'] = base['Orig Dt'].astype(str).str.split(pat='20',expand=True)[0].astype(int)
    base['mnth_cnt'] = 12*base['year']+base['month']

    base['year'] = base['Month of First 60'].astype(str).str[-6:].astype(float)
    base['month'] = base['Month of First 60'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    base['mnth_cnt_frst'] = 12*base['year']+base['month']
    base['60 in 24'] = np.where((base['mnth_cnt_frst'] > base['mnth_cnt']) & (base['mnth_cnt_frst'] <= base['mnth_cnt'] + 24), 1, 0)
    base['year'] = base['Month of First 90'].astype(str).str[-6:].astype(float)
    base['month'] = base['Month of First 90'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    base['mnth_cnt_frst'] = 12*base['year']+base['month']
    base['90 in 24'] = np.where((base['mnth_cnt_frst'] > base['mnth_cnt']) & (base['mnth_cnt_frst'] <= base['mnth_cnt'] + 24), 1, 0)
    base['year'] = base['Month of First 120'].astype(str).str[-6:].astype(float)
    base['month'] = base['Month of First 120'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    base['mnth_cnt_frst'] = 12*base['year']+base['month']
    base['120 in 24'] = np.where((base['mnth_cnt_frst'] > base['mnth_cnt']) & (base['mnth_cnt_frst'] <= base['mnth_cnt'] + 24), 1, 0)

    fico_mean = base['fico'].mean()
    fico_median = base['fico'].median()
    dti_mean = base['DTI'].mean()
    dti_median = base['DTI'].median()
    ltv_mean = base['Orig CLTV'].mean()
    ltv_median = base['Orig CLTV'].median()
    interest_mean = base['Orig Int Rate'].mean()
    interest_median = base['Orig Int Rate'].median()
    upb_mean = base['Orig UPB'].mean()
    upb_median = base['Orig UPB'].median()

    brwr_dist = base['Brwr Cnt'].value_counts()
    purp_dist = base['Loan Purp'].value_counts()
    prop_dist = base['Prop Typ'].value_counts()
    occ_dist = base['Occ Stat'].value_counts()

    six_dist = base['ever 60'].value_counts()
    six_24_dist = base['60 in 24'].value_counts()
    nine_dist = base['ever 90'].value_counts()
    nine_24_dist = base['90 in 24'].value_counts()
    onetwenty_dist = base['ever 120'].value_counts()
    onetwenty_24_dist = base['120 in 24'].value_counts()

    print(f"Output for MSA {msa}")
    print(f"Mean FICO is {fico_mean}, Median FICO is {fico_median}")
    print(f"Mean DTI is {dti_mean}, Median DTI is {dti_median}")
    print(f"Mean CLTV is {ltv_mean}, Median CLTV is {ltv_median}")
    print(f"Mean Int Rate is {interest_mean}, Median Int Rate is {interest_median}")
    print(f"Mean UPB is {upb_mean}, Median UPB is {upb_median}")

    print(f"Borrower Count ditribution is {brwr_dist}")
    print(f"Loan Purpose ditribution is {purp_dist}")
    print(f"Property Type ditribution is {prop_dist}")
    print(f"Occupancy ditribution is {occ_dist}")

    print(f"Ever 60 rate is {six_dist}")
    print(f"60 in 24 rate is {six_24_dist}")
    print(f"Ever 90 rate is {nine_dist}")
    print(f"90 in 24 rate is {nine_24_dist}")
    print(f"Ever 120 rate is {onetwenty_dist}")
    print(f"120 in 24 rate is {onetwenty_24_dist}")

#Call Macro For Each MSA

#analyze(31080)
#analyze(19100)
#analyze(12060)

#analyze(38060)
#analyze(41860)
#analyze(19740)

#analyze(26420)
#analyze(40140)
#analyze(19820)

analyze(42660)
