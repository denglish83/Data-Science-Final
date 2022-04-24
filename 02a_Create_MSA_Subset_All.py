# Import Packages
import pandas as pd

col_names = ["Pool_id", "Fnma Ln", "Report month", "Channel", "Seller", "Servicer", "Master Servicer", "Orig Int Rate", "Curr Int Rate", "Orig UPB",
             "Issue UPB", "Curr UPB", "Orig Term", "Orig Dt", "Frst Pay Dt", "Age", "Mnth to Legal Mat", "Mnth to Mat", "Mat Dt", "Orig LTV",
             "Orig CLTV", "Brwr Cnt", "DTI", "Brwr Fico", "Cbrwr Fico", "FTMB", "Loan Purp", "Prop Typ", "Units", "Occ Stat",
             "State", "MSA", "Zip_3", "MI_PCT", "Amr Typ", "Prepayment Penalty Ind", "IO Ind", "IO Frst Pay Dt", "IO mnth to Amm", "Loan Del Stat",
             "Pmnt Hist", "Mod Flg", "MI Cancel", "Zero Balance Cd", "Zero Balance DT", "UPB At Liqd", "Repurchase Dt", "Scheduled Payment Amt", "Principal Payment", "Excess Principal",
             "Last Pay Dt", "Foreclosure Dt", "Disposition Dt", "Foreclosure Cost", "Propterty Repair Costs", "Asset Recovery Costs", "Misc Holding Expense", "Holding Tax", "Sales Proceed", "Credit Enhanced Proceed",
             "Make Whole Proceed", "Other Proceed", "NonInterest UPB", "Principal Forgiveness", "Orig List Dt", "Orig List Price", "Curr LIst Dt", "Curr List Price", "Brwr Issue Fico", "Cbrwr Issue Fico",
             "Brwr Fico Curr", "Cbrwr Fico Curr", "MI Type", "Servicer Change", "Curr Mod Loss Amt", "Cum Mod Loss Amt", "Curr Credit Gain Loss", "Cum Credit Gain Loss", "HomeReady", "Foreclose Writeoff Amt",
             "Relocation Mortgage Ind", "Zero Balance Code Change Dt", "Holdback Ind", "Holdback Dt", "Del Acrued Int", "Prop Val Method", "High Balance Loan", "ARM 5 Year Ind", "ARM Prod Type", "Fixed Rate Period",
             "Adjust Freq", "Next Adjust Date", "Next Pmnt Change Date", "Index", "ARM Cap Structure", "Int Cap Pct", "Period Cap Pct", "Life Cap Pct", "Margin", "Balloon Ind",
             "ARM Plan No", "Brwr Assist Plan", "HLTV Refi", "Deal Name", "Repurchase Make Whole Flg", "Alternative Deliquency", "Alternative Delinquency Cnt", "Total Defferal Amt"]

# Define Methods

def parsemonth(month, msa):
    print(f"Begining {month} for MSA {msa}")
    base = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{month}.csv", sep='|', header=None,
                       low_memory=False, nrows=1000000, names=col_names)
    subset_60 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '02')]
    subset_60 = subset_60.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    #print(subset_60.shape)
    subset_90 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '03')]
    subset_90 = subset_90.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    #print(subset_90.shape)
    subset_120 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '04')]
    subset_120 = subset_120.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    #rint(subset_120.shape)

    temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    msa_subset = temp.loc[temp['MSA'] == msa]
    #print(msa_subset.shape)

    for i in range(30):
        startpos = i*1000000
        base = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{month}.csv", sep='|', header=None,
                           low_memory=False, skiprows=startpos, nrows=1000000, names=col_names)

        temp_60 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '02')]
        temp_60 = temp_60.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
        temp_90 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '03')]
        temp_90 = temp_90.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
        temp_120 = base.loc[(base['MSA'] == msa) & (base["Loan Del Stat"] == '04')]
        temp_120 = temp_120.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")

        temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
        msa_subset2 = temp.loc[temp['MSA'] == msa]
        msa_subset = pd.concat([msa_subset, msa_subset2], ignore_index=True)
        subset_60 = pd.concat([subset_60, temp_60], ignore_index=True)
        subset_90 = pd.concat([subset_90, temp_90], ignore_index=True)
        subset_120 = pd.concat([subset_120, temp_120], ignore_index=True)
        #print(msa_subset.shape)

    print('parsing complete, dedupping')
    msa_subset = msa_subset.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    subset_60 = subset_60.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    subset_90 = subset_90.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    subset_120 = subset_120.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
    print('deduping complete')

    temp = subset_60[['Fnma Ln', 'Report month']].copy()
    temp.rename(columns={'Report month':'Month of First 60'}, inplace = True)
    #print(temp.head(5))
    join1 = pd.merge(msa_subset, temp, on='Fnma Ln', how='left')

    temp = subset_90[['Fnma Ln', 'Report month']].copy()
    temp.rename(columns={'Report month':'Month of First 90'}, inplace = True)
    join2 = pd.merge(join1, temp, on='Fnma Ln', how ='left')

    temp = subset_120[['Fnma Ln', 'Report month']].copy()
    temp.rename(columns={'Report month':'Month of First 120'}, inplace = True)
    join3 = pd.merge(join2, temp, on='Fnma Ln', how ='left')
    return join3

def parsemsa(msa):
    temp1 = parsemonth("2017Q1", msa)
    print(temp1.shape)
    temp2 = parsemonth("2017Q2", msa)
    print(temp2.shape)
    temp3 = parsemonth("2017Q3", msa)
    print(temp3.shape)
    temp4 = parsemonth("2017Q4", msa)
    print(temp4.shape)
    temp5 = parsemonth("2018Q1", msa)
    print(temp5.shape)
    temp6 = parsemonth("2018Q2", msa)
    print(temp6.shape)
    temp7 = parsemonth("2018Q3", msa)
    print(temp7.shape)
    temp8 = parsemonth("2018Q4", msa)
    print(temp8.shape)

    msa_subset = pd.concat([temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8], ignore_index=True)
    msa_subset.to_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_analysis_set.csv")
    print(f"File Created for MSA {msa}")

# Call Methods
#parsemsa(31080)
#parsemsa(19100)
#parsemsa(41860)

#parsemsa(12060)
#parsemsa(40140)
#parsemsa(40900) # Was in the set for 2015/16 but not for 2017/18

#parsemsa(42660)
#parsemsa(38060)
#parsemsa(19740)

parsemsa(26420) # Added in 2017/18 Set
parsemsa(19820) # Added in 2017/18 Set