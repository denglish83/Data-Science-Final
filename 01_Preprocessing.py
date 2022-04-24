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

#File is too large to load all at one, so load in million row chunks

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, nrows=1000000, names=col_names)
#print(base.head())
dedup = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")

#print(dedup.head())
print("First Million")
print(base.shape)
print(dedup.shape)
print(dedup.head())

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=1000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Second Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=2000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Third Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=3000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Fourth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=4000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Fifth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=5000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Sixth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=6000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Seventh Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=7000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Eighth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=8000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Ninth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=9000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Tenth Million")
print(dedup.shape)
print(dedup.tail())

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=10000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Eleventh Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=11000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twelfth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=12000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Thirteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=13000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Fourteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=14000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Fifteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=15000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Sixteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=16000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Seventeenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=17000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Eighteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=18000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Nineteenth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=190000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentith Million")
print(dedup.shape)
print(dedup.tail())

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=20000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentifirst Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=21000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentisecond Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=22000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentithird Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=23000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentifourth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=24000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentififth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=25000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentisixth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=26000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentiseventh Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=27000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentieighth Million")
print(dedup.shape)

base = pd.read_csv('/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/2018Q1.csv', sep='|', header=None, low_memory=False, skiprows=28000000, nrows=1000000, names=col_names)
temp = base.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")
dedup = pd.concat([dedup, temp], ignore_index=True)
print("Twentininth Million")
print(dedup.shape)

#Dedup final set one last time to remove cases that had rows on either side of the 1 million slices

dedup = dedup.sort_values(by=['Report month']).drop_duplicates(subset=["Fnma Ln"], keep="first")

state_per_msa = dedup.groupby('MSA').agg({"State":"nunique"})
#print(state_per_msa)
zip_per_msa = dedup.groupby('MSA').agg({"Zip_3":"nunique"})
#print(zip_per_msa)
loan_per_msa = dedup.groupby('MSA').agg({"Fnma Ln":"nunique"})

msa_merge1 = state_per_msa.merge(zip_per_msa, how = 'inner', on = 'MSA')
msa_merge = msa_merge1.merge(loan_per_msa, how = 'inner', on = 'MSA')
#print(msa_merge)
msa_merge.reset_index(inplace = True)
#print(msa_merge)

msa_subset = msa_merge.loc[(msa_merge['State'] == 1) & (msa_merge['MSA'] > 0)]
msa_subset.sort_values(by = ['Zip_3', 'Fnma Ln'], inplace=True)
print(msa_subset.tail(15))
msa_subset.sort_values(by = ['Fnma Ln'], inplace=True)
print(msa_subset.tail(15))