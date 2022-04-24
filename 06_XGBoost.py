# IMport Things
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import xgboost as xgb


pd.set_option('display.max_columns', None)

# Model Macro

def model(msa):
    print(f"Modeling MSA {msa}")

    base = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_analysis_set.csv")
    base['fico'] = np.where(base['Cbrwr Fico'].isnull(), base['Brwr Fico'], np.where(base['Brwr Fico'].isnull(), base['Cbrwr Fico'], np.where(base['Brwr Fico'] > base['Cbrwr Fico'], base['Cbrwr Fico'], base['Brwr Fico'])))

    base['year'] = base['Orig Dt'].astype(str).str[-4:].astype(int)
    base['month'] = base['Orig Dt'].astype(str).str.split(pat='20',expand=True)[0].astype(int)
    base['mnth_cnt'] = 12*base['year']+base['month']

    #print(base['Orig Dt'].value_counts())

    #Build MSA Level and Zip Level delinquency counts
    delinq = pd.read_csv(f"/Users/USER/Documents/Classes/2022 Spring/Capstone/Data/{msa}_delinquency_set.csv")

    #delinq['Month of First 90'] = delinq['Month of First 90'].astype(str).str[:-2]
    #delinq['Month of First 120'] = delinq['Month of First 120'].astype(str).str[:-2]
    #delinq['Month of Default'] = delinq['Month of Default'].astype(str).str[:-2]

    delinq['year'] = delinq['Month of First 60'].astype(str).str[-4:].astype(int)
    delinq['month'] = delinq['Month of First 60'].astype(str).str.split(pat='20',expand=True)[0].astype(int)
    delinq['mnth_cnt_60'] = 12*delinq['year']+delinq['month']
    delinq['year'] = delinq['Month of First 90'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of First 90'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    delinq['mnth_cnt_90'] = 12*delinq['year']+delinq['month']
    delinq['year'] = delinq['Month of First 120'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of First 120'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    delinq['mnth_cnt_120'] = 12*delinq['year']+delinq['month']
    delinq['year'] = delinq['Month of Default'].astype(str).str[-6:].astype(float)
    delinq['month'] = delinq['Month of Default'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    delinq['mnth_cnt_def'] = 12*delinq['year']+delinq['month']


    for i in range(36):
        mnth_cnt = 2016*12+i+1
        mnth_subset_60 = delinq[(delinq['mnth_cnt_60'] < mnth_cnt) & (delinq['mnth_cnt_60'] + 24 >= mnth_cnt)]
        mnth_subset_90 = delinq[(delinq['mnth_cnt_90'] < mnth_cnt) & (delinq['mnth_cnt_90'] + 24 >= mnth_cnt)]
        mnth_subset_120 = delinq[(delinq['mnth_cnt_120'] < mnth_cnt) & (delinq['mnth_cnt_120'] + 24 >= mnth_cnt)]
        mnth_subset_def = delinq[(delinq['mnth_cnt_def'] < mnth_cnt) & (delinq['mnth_cnt_def'] + 24 >= mnth_cnt)]

        list = [[mnth_cnt, mnth_subset_60.shape[0], mnth_subset_90.shape[0], mnth_subset_120.shape[0], mnth_subset_def.shape[0]]]
        if i == 0:
            del_cnts = pd.DataFrame(list, columns = ['mnth_cnt', 'cnt_60', 'cnt_90', 'cnt_120', 'cnt_def'])
        else:
            del_cnts = pd.concat([del_cnts, pd.DataFrame(list, columns = ['mnth_cnt', 'cnt_60', 'cnt_90', 'cnt_120', 'cnt_def'])], ignore_index = True)
    #print(del_cnts)

    zip_list = base['Zip_3'].unique()
    first = 1

    for i in range(36):
        mnth_cnt = 2016*12+i+1
        for zip in zip_list:
            mnth_subset_60 = delinq[(delinq['mnth_cnt_60'] < mnth_cnt) & (delinq['mnth_cnt_60'] + 24 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_90 = delinq[(delinq['mnth_cnt_90'] < mnth_cnt) & (delinq['mnth_cnt_90'] + 24 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_120 = delinq[(delinq['mnth_cnt_120'] < mnth_cnt) & (delinq['mnth_cnt_120'] + 24 >= mnth_cnt) & (delinq['Zip_3'] == zip)]
            mnth_subset_def = delinq[(delinq['mnth_cnt_def'] < mnth_cnt) & (delinq['mnth_cnt_def'] + 24 >= mnth_cnt) & (delinq['Zip_3'] == zip)]

            list = [[mnth_cnt, zip, mnth_subset_60.shape[0], mnth_subset_90.shape[0], mnth_subset_120.shape[0], mnth_subset_def.shape[0]]]
            if first == 1:
                del_cnts_zip = pd.DataFrame(list, columns = ['mnth_cnt', 'Zip_3', 'cnt_60', 'cnt_90', 'cnt_120', 'cnt_def'])
                first = 0
            else:
                del_cnts_zip = pd.concat([del_cnts_zip, pd.DataFrame(list, columns = ['mnth_cnt', 'Zip_3', 'cnt_60', 'cnt_90', 'cnt_120', 'cnt_def'])], ignore_index=True)

    #print(del_cnts)
    #print(del_cnts_zip)

    join1 = pd.merge(base, del_cnts, how = 'left', on = 'mnth_cnt')
    join2 = pd.merge(join1, del_cnts_zip, how = 'left', on = ['mnth_cnt', 'Zip_3'], suffixes=['_msa', '_zip'])
    #print(join2.head())

    model_subset = join2[["Fnma Ln", "Orig Int Rate", "Orig CLTV", "Brwr Cnt", "DTI", "fico", "FTMB",
                          "Loan Purp", "Prop Typ", "Occ Stat", "cnt_120_msa", "cnt_120_zip",
                          "Orig Dt", "Month of First 60", "mnth_cnt"]].copy()


    model_subset['year'] = model_subset['Month of First 60'].astype(str).str[-6:].astype(float)
    model_subset['month'] = model_subset['Month of First 60'].astype(str).str.split(pat='20',expand=True)[0].astype(float)
    model_subset['mnth_cnt_frst'] = 12*model_subset['year']+model_subset['month']
    model_subset['60 in 24'] = np.where((model_subset['mnth_cnt_frst'] > model_subset['mnth_cnt']) & (model_subset['mnth_cnt_frst'] <= model_subset['mnth_cnt'] + 24), 1, 0)
    model_subset['ever 60'] = np.where(base['Month of First 60'].isnull(), 0, 1)
    model_subset['constant'] = 1

    #model_subset['fico_spline1'] = np.minimum(640, np.maximum(0, model_subset['fico']))
    #model_subset['fico_spline2'] = np.minimum(20, np.maximum(0, model_subset['fico'] - 640))
    #model_subset['fico_spline3'] = np.minimum(20, np.maximum(0, model_subset['fico'] - 660))
    #model_subset['fico_spline4'] = np.minimum(20, np.maximum(0, model_subset['fico'] - 680))
    #model_subset['fico_spline5'] = np.minimum(20, np.maximum(0, model_subset['fico'] - 700))
    #model_subset['fico_spline6'] = np.minimum(20, np.maximum(0, model_subset['fico'] - 720))
    #model_subset['fico_spline7'] = np.maximum(0, model_subset['fico'] - 740)

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

    #model_subset['mi flg'] = np.where(model_subset["Orig CLTV"] > 80, 1, 0)
    #model_subset['LTV_Spline1'] = np.minimum(60, np.maximum(0, model_subset['Orig CLTV']))
    #model_subset['LTV_Spline2'] = np.minimum(10, np.maximum(0, model_subset['Orig CLTV'] - 60))
    #model_subset['LTV_Spline3'] = np.minimum(5, np.maximum(0, model_subset['Orig CLTV'] - 70))
    #model_subset['LTV_Spline4'] = np.minimum(5, np.maximum(0, model_subset['Orig CLTV'] - 75))
    #model_subset['LTV_Spline5'] = np.minimum(5, np.maximum(0, model_subset['Orig CLTV'] - 80))
    #model_subset['LTV_Spline6'] = np.minimum(5, np.maximum(0, model_subset['Orig CLTV'] - 85))
    #model_subset['LTV_Spline7'] = np.minimum(5, np.maximum(0, model_subset['Orig CLTV'] - 90))
    #model_subset['LTV_Spline8'] = np.minimum(2, np.maximum(0, model_subset['Orig CLTV']- 95))
    #model_subset['LTV_Spline9'] = np.maximum(0, model_subset['Orig CLTV'] - 97)

    model_subset['cltv_bin'] = np.where(model_subset['Orig CLTV'] <= 60, '0',
                                        np.where(model_subset['Orig CLTV'] <= 70, '1',
                                                 np.where(model_subset['Orig CLTV'] <= 75, '2',
                                                          np.where(model_subset['Orig CLTV'] <= 80, '3',
                                                                   np.where(model_subset['Orig CLTV'] <= 85, '4',
                                                                            np.where(model_subset['Orig CLTV'] < 90, '5',
                                                                                     np.where(model_subset['Orig CLTV'] < 95, '6',
                                                                                              np.where(model_subset['Orig CLTV'] < 97, '7', '8')
                                                                                              )
                                                                                     )
                                                                            )
                                                                   )
                                                          )
                                                 )
                                        )

    #print(model_subset['mi flg'].value_counts())

    #print(f"All Records: {model_subset.shape}")
    model_subset = model_subset.dropna(subset=['fico', 'DTI'])
    #print(f"All Records with Fico and DTI: {model_subset.shape}")
    model_subset["cnt_120_msa"] = model_subset["cnt_120_msa"].fillna(0)
    model_subset["cnt_120_zip"] = model_subset["cnt_120_zip"].fillna(0)

    x = model_subset[["Orig Int Rate", "Brwr Cnt", "DTI", "FTMB",'Orig CLTV', 'fico_bin',
                          "Loan Purp", "Occ Stat", "cnt_120_msa", "cnt_120_zip", 'constant']].copy()

    missing = x[x.isna().any(axis=1)]
    print(missing.head())

    dummies = pd.get_dummies(x[["FTMB", "Loan Purp", "Occ Stat", 'fico_bin']], drop_first=True)
    x = pd.concat([x.drop(["FTMB", "Loan Purp", "Occ Stat", 'fico_bin'], axis=1), dummies], axis=1)

    #print(x.head())

    y = model_subset[['60 in 24']].copy()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=1221)

    smote = SMOTE(random_state = 1221)
    smote_x_train, smote_y_train = smote.fit_resample(x_train, y_train)

    xg_class = xgb.XGBClassifier(objective='binary:logistic',
                                 max_depth=8,
                                 learning_rate=.01,
                                 colsample_bytree=.8,
                                 )
    xg_class.fit(smote_x_train, smote_y_train.values.ravel())

    cut_off = .5

    y_pred = xg_class.predict(x_train)
    y_pred1 = np.where(y_pred > cut_off, 1, 0)
    print("Train Classification")
    print(classification_report(y_train, y_pred1))

    y_pred = xg_class.predict(x_test)

    y_pred2 = np.where(y_pred > cut_off, 1, 0)
    print("Test Classification")
    print(classification_report(y_test, y_pred2))

    x_edit = x.copy()
    pred_true = xg_class.predict_proba(x_edit)
    pred_true_pd = pd.DataFrame(pred_true)
    y_pred_true = pd.DataFrame(np.where(pred_true > cut_off, 1, 0))

    x_edit['cnt_120_msa'] = x_edit['cnt_120_msa'] + x_edit['cnt_120_zip']
    x_edit['cnt_120_zip'] = 0
    pred_sim = xg_class.predict_proba(x_edit)
    pred_sim_pd = pd.DataFrame(pred_sim)
    y_pred_sim = pd.DataFrame(np.where(pred_sim > cut_off, 1, 0))

    y_cat = pd.concat([pred_true_pd, y_pred_true, pred_sim_pd, y_pred_sim], axis = 1)
    y_cat.columns = ['true_0_prob', 'true_1_prob', 'true_0_pred', 'true_1_pred', 'sim_0_prob', 'sim_1_prob', 'sim_0_pred', 'sim_1_pred']

    y_cat_decrease = y_cat[y_cat['true_1_prob'] < y_cat['sim_1_prob']]
    y_cat_equal = y_cat[y_cat['true_1_prob'] == y_cat['sim_1_prob']]
    y_cat_greater = y_cat[y_cat['true_1_prob'] > y_cat['sim_1_prob']]

    print(f"number of obs: {y_cat.shape}, number of obs decreased prob: {y_cat_decrease.shape}")
    print(f"number of obs: {y_cat.shape}, number of obs equal prob: {y_cat_equal.shape}")
    print(f"number of obs: {y_cat.shape}, number of obs increased prob: {y_cat_greater.shape}")



    x_edit = x.copy()
    pred_true = xg_class.predict_proba(x_edit)
    pred_true_pd = pd.DataFrame(pred_true)
    y_pred_true = pd.DataFrame(np.where(pred_true > cut_off, 1, 0))

    x_edit['cnt_120_msa'] = x_edit['cnt_120_msa']
    x_edit['cnt_120_zip'] = 0
    pred_sim = xg_class.predict_proba(x_edit)
    pred_sim_pd = pd.DataFrame(pred_sim)
    y_pred_sim = pd.DataFrame(np.where(pred_sim > cut_off, 1, 0))

    y_cat = pd.concat([pred_true_pd, y_pred_true, pred_sim_pd, y_pred_sim], axis = 1)
    y_cat.columns = ['true_0_prob', 'true_1_prob', 'true_0_pred', 'true_1_pred', 'sim_0_prob', 'sim_1_prob', 'sim_0_pred', 'sim_1_pred']

    y_cat_decrease = y_cat[y_cat['true_1_prob'] < y_cat['sim_1_prob']]
    y_cat_equal = y_cat[y_cat['true_1_prob'] == y_cat['sim_1_prob']]
    y_cat_greater = y_cat[y_cat['true_1_prob'] > y_cat['sim_1_prob']]

    print(f"number of obs: {y_cat.shape}, number of obs decreased prob: {y_cat_decrease.shape}")
    print(f"number of obs: {y_cat.shape}, number of obs equal prob: {y_cat_equal.shape}")
    print(f"number of obs: {y_cat.shape}, number of obs increased prob: {y_cat_greater.shape}")

    x_change = x.copy()
    y_true = pd.DataFrame(xg_class.predict_proba(x_change))
    x_change["cnt_120_zip"] = x_change["cnt_120_zip"] + 1
    y_change = pd.DataFrame(xg_class.predict_proba(x_change))
    y_cat = pd.concat([y_true, y_change], axis=1)
    #print(y_cat.head())
    y_cat.columns = ['true_0_prob', 'true_1_prob', 'change_0_pred', 'change_1_pred']
    y_cat['delta'] = y_cat['change_1_pred'] - y_cat['true_1_prob']
    median_val= np.median(y_cat['delta'])
    mean_val= np.mean(y_cat['delta'])
    #print(y_cat.head())
    print(f"Median Delta is: {median_val}, Mean is: {mean_val}")


#Call Function

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

