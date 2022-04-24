# Import Stuff #

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

pd.set_option('display.max_columns', None)

# Start Macro
def model(msa):
    print(f"Modeling MSA {msa}")

    # Make Base Data Set

    base = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_analysis_set.csv")
    base['fico'] = np.where(base['Cbrwr Fico'].isnull(), base['Brwr Fico'], np.where(base['Brwr Fico'].isnull(), base['Cbrwr Fico'], np.where(base['Brwr Fico'] > base['Cbrwr Fico'], base['Cbrwr Fico'], base['Brwr Fico'])))

    base['year'] = base['Orig Dt'].astype(str).str[-4:].astype(int)
    base['month'] = base['Orig Dt'].astype(str).str.split(pat='20',expand=True)[0].astype(int)
    base['mnth_cnt'] = 12*base['year']+base['month']

    # Fit Model

    model_subset = base[["Fnma Ln", "Zip_3", "Orig Int Rate", "Orig CLTV", "Brwr Cnt", "DTI", "fico", "FTMB",
                          "Loan Purp", "Prop Typ", "Occ Stat",
                          "Orig Dt", "Month of First 60", "mnth_cnt"]].copy()


    model_subset['year'] = model_subset['Month of First 60'].astype(str).str[-6:].astype(float)
    model_subset['month'] = model_subset['Month of First 60'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    model_subset['mnth_cnt_frst'] = 12*model_subset['year']+model_subset['month']
    model_subset['60 in 24'] = np.where((model_subset['mnth_cnt_frst'] > model_subset['mnth_cnt']) & (model_subset['mnth_cnt_frst'] <= model_subset['mnth_cnt'] + 24), 1, 0)
    #print(model_subset['60 in 24'].value_counts())

    model_subset['ever 60'] = np.where(base['Month of First 60'].isnull(), 0, 1)
    model_subset['constant'] = 1
    model_subset['fico_bin'] = np.where(model_subset['fico'] < 640, '0',
                                        np.where(model_subset['fico'] < 660, '1',
                                                 np.where(model_subset['fico'] < 680, '2',
                                                          np.where(model_subset['fico'] < 700, '3',
                                                                   np.where(model_subset['fico'] < 720, '4',
                                                                            np.where(model_subset['fico'] < 740, '5','6')
                                                                            )
                                                                   )
                                                          )
                                                 )
                                        )
    model_subset = model_subset.dropna(subset=['fico', 'DTI'])

    x = model_subset[["Fnma Ln", "Orig Int Rate", "Brwr Cnt", "DTI", "FTMB",'Orig CLTV', 'fico_bin',
                          "Loan Purp", "Occ Stat", 'constant']].copy()
    dummies = pd.get_dummies(x[["FTMB", "Loan Purp", "Occ Stat", 'fico_bin']], drop_first=True)
    x = pd.concat([x.drop(["FTMB", "Loan Purp", "Occ Stat", 'fico_bin'], axis=1), dummies], axis=1)
    y = model_subset[['60 in 24']].copy()
    x_train_w_ln, x_test_w_ln, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=1221)

    x_train = x_train_w_ln.copy()
    x_train.drop(['Fnma Ln'], axis = 1, inplace = True)

    x_test = x_test_w_ln.copy()
    x_test.drop(['Fnma Ln'], axis = 1, inplace = True)

    smote = SMOTE(random_state = 1221)
    smote_x_train, smote_y_train = smote.fit_resample(x_train, y_train)
    model = sm.Logit(smote_y_train, smote_x_train).fit()
    print(model.summary())

    cut_off = .5

    y_pred = model.predict(x_test)

    y_pred2 = np.where(y_pred > cut_off, 1, 0)
    print("Test Classification")
    print(classification_report(y_test, y_pred2))

    x.drop(['Fnma Ln'], axis = 1, inplace = True)
    y_pred = model.predict(x)
    #print(y_pred.head())
    model_subset['Orig Pred'] = y_pred
    #print("Model Data With Base Prediction")
    #print(model_subset.head())

    np_model_subset = model_subset.to_numpy()

    # Convert To Monthly
    monthly = []

    for obs in np_model_subset:
        for i in range(25):
            temp = []
            #print(obs)
            temp.append(obs[0])                             #Fnma Ln
            temp.append(obs[1])                             #Zip Code
            temp.append(obs[21])                            #Origination Default Probability
            temp.append(obs[13] + i)                        #Current Month
            temp.append(i)                                  #Months without a deliquency
            if temp[3] == obs[16]:
                temp.append(1)
            else:
                temp.append(0)                              #is this the first deliquency month
            #print(temp)
            if (obs[16] < temp[3]) & (obs[16] > 0):
                break
            monthly.append(temp)
        #print(monthly)
        #break

    monthly_pd = pd.DataFrame(monthly, columns = ['Fnma Ln', 'Zip_3', 'Orig Def Prob', 'mnth_cnt', 'payments', 'del'])
    #print("Data Transformed to Monthly")
    #print(monthly_pd.head())

    #print('Checking Delinquency Numbers')
    #print(monthly_pd['del'].value_counts())

    # Calculate Monthly Zip/MSA Defaults

    delinq = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_delinquency_set.csv")

    delinq['year'] = delinq['Month of First 60'].astype(str).str[-4:].astype(int)
    delinq['month'] = delinq['Month of First 60'].astype(str).str.split(pat='20', expand=True)[0].astype(int)
    delinq['mnth_cnt_60'] = 12 * delinq['year'] + delinq['month']
    delinq['year'] = delinq['Month of First 90'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of First 90'].astype(str).str.split(pat='20', expand=True)[0].astype(float)
    delinq['mnth_cnt_90'] = 12 * delinq['year'] + delinq['month']
    delinq['year'] = delinq['Month of First 120'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of First 120'].astype(str).str.split(pat='20', expand=True)[0].astype(float)
    delinq['mnth_cnt_120'] = 12 * delinq['year'] + delinq['month']
    delinq['year'] = delinq['Month of Default'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of Default'].astype(str).str.split(pat='20', expand=True)[0].astype(float)
    delinq['mnth_cnt_def'] = 12 * delinq['year'] + delinq['month']

    for i in range(36):
        mnth_cnt = 2016*12+i+1
        mnth_subset_120_1 = delinq[(delinq['mnth_cnt_120'] == mnth_cnt)]
        mnth_subset_120_3 = delinq[(delinq['mnth_cnt_120'] + 1 < mnth_cnt) & (delinq['mnth_cnt_120'] + 3 >= mnth_cnt)]
        mnth_subset_120_6 = delinq[(delinq['mnth_cnt_120'] + 3 < mnth_cnt) & (delinq['mnth_cnt_120'] + 6 >= mnth_cnt)]
        mnth_subset_120_12 = delinq[(delinq['mnth_cnt_120'] + 6 < mnth_cnt) & (delinq['mnth_cnt_120'] + 12 >= mnth_cnt)]
        mnth_subset_def = delinq[(delinq['mnth_cnt_def'] == mnth_cnt)]

        list = [[mnth_cnt, mnth_subset_120_1.shape[0], mnth_subset_120_3.shape[0], mnth_subset_120_6.shape[0],  mnth_subset_120_12.shape[0],mnth_subset_def.shape[0]]]
        if i == 0:
            del_cnts = pd.DataFrame(list, columns = ['mnth_cnt', 'cnt_1', 'cnt_3', 'cnt_6', 'cnt_12', 'cnt_def'])
        else:
            del_cnts = pd.concat([del_cnts, pd.DataFrame(list, columns = ['mnth_cnt', 'cnt_1', 'cnt_3', 'cnt_6', 'cnt_12', 'cnt_def'])], ignore_index = True)

    zip_list = base['Zip_3'].unique()
    first = 1

    for i in range(36):
        mnth_cnt = 2016*12+i+1
        for zip in zip_list:
            mnth_subset_120_1 = delinq[(delinq['mnth_cnt_120'] == mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_120_3 = delinq[(delinq['mnth_cnt_120'] + 1 < mnth_cnt) & (delinq['mnth_cnt_120'] + 3 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_120_6 = delinq[(delinq['mnth_cnt_120'] + 3 < mnth_cnt) & (delinq['mnth_cnt_120'] + 6 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_120_12 = delinq[(delinq['mnth_cnt_120'] + 6 < mnth_cnt) & (delinq['mnth_cnt_120'] + 12 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_def = delinq[(delinq['mnth_cnt_def'] == mnth_cnt) & (delinq['Zip_3'] == zip)]

            list = [[mnth_cnt, zip, mnth_subset_120_1.shape[0], mnth_subset_120_3.shape[0], mnth_subset_120_6.shape[0],  mnth_subset_120_12.shape[0],mnth_subset_def.shape[0]]]
            if first == 1:
                del_cnts_zip = pd.DataFrame(list, columns = ['mnth_cnt', 'Zip_3', 'cnt_1', 'cnt_3', 'cnt_6', 'cnt_12', 'cnt_def'])
                first = 0
            else:
                del_cnts_zip = pd.concat([del_cnts_zip, pd.DataFrame(list, columns = ['mnth_cnt', 'Zip_3', 'cnt_1', 'cnt_3', 'cnt_6', 'cnt_12', 'cnt_def'])], ignore_index=True)

    #print(del_cnts)
    #print(del_cnts_zip)

    # Merge Onto Monthly Set

    join1 = pd.merge(monthly_pd, del_cnts, how = 'left', on = 'mnth_cnt')
    join2 = pd.merge(join1, del_cnts_zip, how = 'left', on = ['mnth_cnt', 'Zip_3'], suffixes=['_msa', '_zip'])
    join2['constant'] = 1

    join2["cnt_1_msa"] = join2["cnt_1_msa"].fillna(0)
    join2["cnt_3_msa"] = join2["cnt_3_msa"].fillna(0)
    join2["cnt_6_msa"] = join2["cnt_6_msa"].fillna(0)
    join2["cnt_12_msa"] = join2["cnt_12_msa"].fillna(0)
    join2["cnt_1_zip"] = join2["cnt_1_zip"].fillna(0)
    join2["cnt_3_zip"] = join2["cnt_3_zip"].fillna(0)
    join2["cnt_6_zip"] = join2["cnt_6_zip"].fillna(0)
    join2["cnt_12_zip"] = join2["cnt_12_zip"].fillna(0)

    join2['Log Odds'] = np.log2(join2['Orig Def Prob'])
    join2['Log Odds 2'] = join2['Orig Def Prob']/(1 - join2['Orig Def Prob'])

    join2.drop(['cnt_def_msa', 'cnt_def_zip'], axis = 1, inplace = True)

    join2 = join2[(join2.payments != 1) & (join2.payments != 2)]

    #print("Data monthly regression ")
    #print(join2.head())

    missing = join2[join2.isna().any(axis=1)]
    #print("Rows Missing Vars")
    #print(missing.head())

    #def_set = join2[join2['del'] == 1]
    #def_pd = pd.DataFrame(def_set["payments"].value_counts()).sort_index()
    #print(def_pd)

    # Time Series Model
    train = pd.merge(join2, x_train_w_ln[['Fnma Ln']], how = 'inner')

    #print("After Merge")
    #print(train.head())

    test = pd.merge(join2, x_test_w_ln[['Fnma Ln']], how = 'inner')

    x_train = train.copy()
    x_train["payments"] = x_train["payments"].map(str)
    dummies = pd.get_dummies(x_train[["payments"]], drop_first=True)
    x_train = pd.concat([x_train.drop(["payments"], axis=1), dummies], axis=1)

    x_train['payments_3'] = x_train['payments_3']*x_train['Orig Def Prob']
    x_train['payments_4'] = x_train['payments_4']*x_train['Orig Def Prob']
    x_train['payments_5'] = x_train['payments_5']*x_train['Orig Def Prob']
    x_train['payments_6'] = x_train['payments_6']*x_train['Orig Def Prob']
    x_train['payments_7'] = x_train['payments_7']*x_train['Orig Def Prob']
    x_train['payments_8'] = x_train['payments_8']*x_train['Orig Def Prob']
    x_train['payments_9'] = x_train['payments_9']*x_train['Orig Def Prob']
    x_train['payments_10'] = x_train['payments_10']*x_train['Orig Def Prob']
    x_train['payments_11'] = x_train['payments_11']*x_train['Orig Def Prob']
    x_train['payments_12'] = x_train['payments_12']*x_train['Orig Def Prob']
    x_train['payments_13'] = x_train['payments_13']*x_train['Orig Def Prob']
    x_train['payments_14'] = x_train['payments_14']*x_train['Orig Def Prob']
    x_train['payments_15'] = x_train['payments_15']*x_train['Orig Def Prob']
    x_train['payments_16'] = x_train['payments_16']*x_train['Orig Def Prob']
    x_train['payments_17'] = x_train['payments_17']*x_train['Orig Def Prob']
    x_train['payments_18'] = x_train['payments_18']*x_train['Orig Def Prob']
    x_train['payments_19'] = x_train['payments_19']*x_train['Orig Def Prob']
    x_train['payments_20'] = x_train['payments_20']*x_train['Orig Def Prob']
    x_train['payments_21'] = x_train['payments_21']*x_train['Orig Def Prob']
    x_train['payments_22'] = x_train['payments_22']*x_train['Orig Def Prob']
    x_train['payments_23'] = x_train['payments_23']*x_train['Orig Def Prob']
    x_train['payments_24'] = x_train['payments_24']*x_train['Orig Def Prob']

    #x_train['zip_1_1'] = np.where(x_train['cnt_1_zip'] >= 1, 1, 0)
    #x_train['zip_1_2'] = np.where(x_train['cnt_1_zip'] >= 2, 1, 0)
    #x_train['zip_1_3'] = np.where(x_train['cnt_1_zip'] >= 3, x_train['cnt_1_zip'] - 2, 0)

    #x_train['zip_3_1'] = np.where(x_train['cnt_3_zip'] <= 3, x_train['cnt_3_zip'], 3)
    #x_train['zip_3_2'] = np.where(x_train['cnt_3_zip'] >= 3, np.where(x_train['cnt_3_zip'] >= 6, x_train['cnt_3_zip'] - 3, 3), 0)
    #x_train['zip_3_3'] = np.where(x_train['cnt_3_zip'] >= 6, x_train['cnt_3_zip'] - 6, 0)

    #x_train['zip_6_1'] = np.where(x_train['cnt_6_zip'] <= 3, x_train['cnt_6_zip'], 3)
    #x_train['zip_6_2'] = np.where(x_train['cnt_6_zip'] >= 3, np.where(x_train['cnt_6_zip'] >= 6, x_train['cnt_6_zip'] - 3, 3), 0)
    #x_train['zip_6_3'] = np.where(x_train['cnt_6_zip'] >= 6, x_train['cnt_6_zip'] - 6, 0)

    #x_train['zip_12_1'] = np.where(x_train['cnt_12_zip'] <= 3, x_train['cnt_12_zip'], 3)
    #x_train['zip_12_2'] = np.where(x_train['cnt_12_zip'] >= 3, np.where(x_train['cnt_12_zip'] >= 6, x_train['cnt_12_zip'] - 3, 3), 0)
    #x_train['zip_12_3'] = np.where(x_train['cnt_12_zip'] >= 6, x_train['cnt_12_zip'] - 6, 0)


    x_train.drop(['Fnma Ln', 'Zip_3', 'del', "mnth_cnt", 'Orig Def Prob', 'Log Odds', 'Log Odds 2'], axis = 1, inplace = True)
    y_train = train['del']

    x_test = test.copy()
    x_test["payments"] = x_test["payments"].map(str)
    dummies = pd.get_dummies(x_test[["payments"]], drop_first=True)
    x_test = pd.concat([x_test.drop(["payments"], axis=1), dummies], axis=1)

    x_test['payments_3'] = x_test['payments_3']*x_test['Orig Def Prob']
    x_test['payments_4'] = x_test['payments_4']*x_test['Orig Def Prob']
    x_test['payments_5'] = x_test['payments_5']*x_test['Orig Def Prob']
    x_test['payments_6'] = x_test['payments_6']*x_test['Orig Def Prob']
    x_test['payments_7'] = x_test['payments_7']*x_test['Orig Def Prob']
    x_test['payments_8'] = x_test['payments_8']*x_test['Orig Def Prob']
    x_test['payments_9'] = x_test['payments_9']*x_test['Orig Def Prob']
    x_test['payments_10'] = x_test['payments_10']*x_test['Orig Def Prob']
    x_test['payments_11'] = x_test['payments_11']*x_test['Orig Def Prob']
    x_test['payments_12'] = x_test['payments_12']*x_test['Orig Def Prob']
    x_test['payments_13'] = x_test['payments_13']*x_test['Orig Def Prob']
    x_test['payments_14'] = x_test['payments_14']*x_test['Orig Def Prob']
    x_test['payments_15'] = x_test['payments_15']*x_test['Orig Def Prob']
    x_test['payments_16'] = x_test['payments_16']*x_test['Orig Def Prob']
    x_test['payments_17'] = x_test['payments_17']*x_test['Orig Def Prob']
    x_test['payments_18'] = x_test['payments_18']*x_test['Orig Def Prob']
    x_test['payments_19'] = x_test['payments_19']*x_test['Orig Def Prob']
    x_test['payments_20'] = x_test['payments_20']*x_test['Orig Def Prob']
    x_test['payments_21'] = x_test['payments_21']*x_test['Orig Def Prob']
    x_test['payments_22'] = x_test['payments_22']*x_test['Orig Def Prob']
    x_test['payments_23'] = x_test['payments_23']*x_test['Orig Def Prob']
    x_test['payments_24'] = x_test['payments_24']*x_test['Orig Def Prob']

    #x_test['zip_1_1'] = np.where(x_test['cnt_1_zip'] >= 1, 1, 0)
    #x_test['zip_1_2'] = np.where(x_test['cnt_1_zip'] >= 2, 1, 0)
    #x_test['zip_1_3'] = np.where(x_test['cnt_1_zip'] >= 3, x_test['cnt_1_zip'] - 2, 0)

    #x_test['zip_3_1'] = np.where(x_test['cnt_3_zip'] <= 3, x_test['cnt_3_zip'], 3)
    #x_test['zip_3_2'] = np.where(x_test['cnt_3_zip'] >= 3, np.where(x_test['cnt_3_zip'] >= 6, x_test['cnt_3_zip'] - 3, 3), 0)
    #x_test['zip_3_3'] = np.where(x_test['cnt_3_zip'] >= 6, x_test['cnt_3_zip'] - 6, 0)

    #x_test['zip_6_1'] = np.where(x_test['cnt_6_zip'] <= 3, x_test['cnt_6_zip'], 3)
    #x_test['zip_6_2'] = np.where(x_test['cnt_6_zip'] >= 3, np.where(x_test['cnt_6_zip'] >= 6, x_test['cnt_6_zip'] - 3, 3), 0)
    #x_test['zip_6_3'] = np.where(x_test['cnt_6_zip'] >= 6, x_test['cnt_6_zip'] - 6, 0)

    #x_test['zip_12_1'] = np.where(x_test['cnt_12_zip'] <= 3, x_test['cnt_12_zip'], 3)
    #x_test['zip_12_2'] = np.where(x_test['cnt_12_zip'] >= 3, np.where(x_test['cnt_12_zip'] >= 6, x_test['cnt_12_zip'] - 3, 3), 0)
    #x_test['zip_12_3'] = np.where(x_test['cnt_12_zip'] >= 6, x_test['cnt_12_zip'] - 6, 0)



    x_test.drop(['Fnma Ln', 'Zip_3', 'del', "mnth_cnt", 'Orig Def Prob', 'Log Odds', 'Log Odds 2'], axis = 1, inplace = True)
    y_test = test['del']


    smote_x_train, smote_y_train = smote.fit_resample(x_train, y_train)

    #print("Going into model")
    #print(smote_x_train.head())
    #print(smote_y_train.value_counts())

    model = sm.Logit(smote_y_train, smote_x_train).fit()
    print(model.summary())

    cut_off = .5

    y_pred = model.predict(x_train)
    y_pred1 = np.where(y_pred > cut_off, 1, 0)
    print("Train Classification")
    print(classification_report(y_train, y_pred1))

    y_pred = model.predict(x_test)

    y_pred2 = np.where(y_pred > cut_off, 1, 0)
    print("Test Classification")
    print(classification_report(y_test, y_pred2))

    x = pd.concat([x_train, x_test], axis = 0)
    x_change = x.copy()
    y_true = model.predict(x_change)
    x_change["cnt_1_zip"] = x_change["cnt_1_zip"] + 1
    y_change = model.predict(x_change)
    y_cat = pd.concat([y_true, y_change], axis=1)
    y_cat.columns = ['true_pred', 'change_pred']
    y_cat['delta'] = y_cat['change_pred'] - y_cat['true_pred']
    median_val= np.median(y_cat['delta'])
    print(y_cat.head())
    print(f"Median Delta is {median_val}")


# Call Macro

model(31080)
model(19100)
model(12060)
model(38060)
model(41860)

model(19740)
model(26420)
model(40140)
model(19820)
model(42660)