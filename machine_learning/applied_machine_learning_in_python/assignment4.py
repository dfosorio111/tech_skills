import pandas as pd
import numpy as np


# y_target: compliance (blight ticket will be paid on time) [1:early/on_time/1_month - 0:after_hearning/notatall  Null:not_responsible]
# y_target compliance = Null, not_responsible NOT in test-set (data clean-leakage)
# y_target compliance: only available in train-set(data leakage (not in test-set)
# model.predict(x_test), probability that compliance is paid on time  (decision function)
# evaluation metric, scoring parameter=auc


# create Binary Classifier with probability output for entry



def blight_model():
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import roc_auc_score
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.metrics import roc_curve, auc
    from adspy_shared_utilities import plot_class_regions_for_classifier_subplot

    # Your code here

    # load source data
    # 'readonly/test.csv'
    df_train = pd.read_csv('train.csv', encoding="ISO-8859-1")
    df_test = pd.read_csv('test.csv', encoding="ISO-8859-1")
    df_address = pd.read_csv('addresses.csv', encoding="ISO-8859-1")
    df_coords = pd.read_csv('latlons.csv', encoding="ISO-8859-1")

    # create DataFrames for easy data manipulation using Pandas
    df_train = pd.DataFrame(df_train)
    df_test = pd.DataFrame(df_test)
    df_address = pd.DataFrame(df_address)  # columns: ticket_id y address
    df_coords = pd.DataFrame(df_coords)  # columns: address; lat-lon

    # clean data

    # df_train.dropna() drop rows where compliance feature is nan, clean Null data
    df_train.dropna(subset=["compliance"], inplace=True)

    # over-over write df_train rows, condition: country == 'USA'
    df_train = df_train[df_train['country'] == 'USA']
    df_test = df_test[df_test['country'] == 'USA']

    # merge df_address and df_coords by address, with df_dataset
    # first merge() df_address and df_coords by(on) 'address', then merge with dataset by(on) 'ticket_id'
    df_aux = pd.merge(df_address, df_coords, on='address')
    df_train = pd.merge(df_train, df_aux, on='ticket_id')
    df_test = pd.merge(df_test, df_aux, on='ticket_id')

    # df_train.drop() drop columns of data leakage, unnecesary variables
    # remove features non existing in test-set

    # drop all unnecessary columns
    df_train.drop(['agency_name', 'inspector_name', 'violator_name', 'non_us_str_code', 'violation_description',
                   'grafitti_status', 'state_fee', 'admin_fee', 'ticket_issued_date', 'hearing_date',
                   # columns not available in test
                   'payment_amount', 'balance_due', 'payment_date', 'payment_status',
                   'collection_status', 'compliance_detail',
                   # address related columns
                   'violation_zip_code', 'country', 'address', 'violation_street_number',
                   'violation_street_name', 'mailing_address_str_number', 'mailing_address_str_name',
                   'city', 'state', 'zip_code', 'address'], axis=1, inplace=True)

    # LabelEncoder(),  convert string columns into discrete  to  build the model using LabelEncoder class
    # create new LabelEncoder()
    label_encoder = LabelEncoder()
    # fit/train new LabelEncoder with column 'disposition' for train-set and test-set
    label_encoder.fit(df_train['disposition'].append(df_test['disposition'], ignore_index=True))
    df_train['disposition'] = label_encoder.transform(df_train['disposition'])
    df_test['disposition'] = label_encoder.transform(df_test['disposition'])

    aux = df_train['disposition']

    # create new LabelEncoder()
    label_encoder = LabelEncoder()
    # fit/train new LabelEncoder with column 'violation_code' for train-set and test-set
    label_encoder.fit(df_train['violation_code'].append(df_test['violation_code'], ignore_index=True))
    # fit/train new LabelEncoder with column 'violation_code' for train-set and test-set
    df_train['violation_code'] = label_encoder.transform(df_train['violation_code'])
    df_test['violation_code'] = label_encoder.transform(df_test['violation_code'])

    # convert lat-lon table, fillna
    df_train['lat'] = df_train['lat'].fillna(df_train['lat'].mean())
    df_train['lon'] = df_train['lon'].fillna(df_train['lon'].mean())
    df_test['lat'] = df_test['lat'].fillna(df_test['lat'].mean())
    df_test['lon'] = df_test['lon'].fillna(df_test['lon'].mean())

    # df_train.columns.values,  get df_train columns
    cols = list(df_train.columns.values)

    # remove y_target 'compliance' from columns
    cols.remove('compliance')

    # set df_test
    df_test = df_test[cols]



    # # train the model
    # X_train, X_test, y_train, y_test = train_test_split(df_train[df_train != 'compliance'], df_train['compliance'],
    #                                                     random_state=0)
    #
    # # print(X_train)
    # # print("\b")
    # # print(y_train)
    #
    # # create models
    #
    # # create RandomForestClassifier model, parameters: random_state=0
    # # fit/train model with train-set
    # rfc = RandomForestRegressor(max_depth = None)#.fit(X_train, y_train)
    #
    # # gamma parameter range to optimize
    # grid_values = {'n_estimators': [10, 100, 1000, 10000], 'max_depth': [None, 10, 20, 30 ] }
    #
    # #  optimize parameter values of model, given an evaluation metric over the range
    # # create GridSearchCV optimizer, parameters: model rfc, param_grid = param_range, scoring = evaluation_metric
    #
    # grid_rfc_auc = GridSearchCV(rfc, param_grid=grid_values, scoring='roc_auc')
    #
    # # fit/train GridSearchCV class with train-set
    # grid_rfc_auc.fit(X_train, y_train)
    #
    # # get decision function probability scores of classification (binary), using the GridSearchCV optimizer with X_test
    # y_decisionfunction_scores_rfc = grid_rfc_auc.decision_function(X_test)
    #
    # # print('Test set AUC: ', roc_auc_score(y_test, y_decisionfunction_scores_auc))
    # #print('Grid best parameter (max. AUC): ', grid_rfc_auc.best_params_)
    # #print('Grid best score (AUC): ', grid_rfc_auc.best_score_)
    #
    # #y_predict = pd.DataFrame(grid_rfc_auc.predict(df_test), df_test.ticked_id )
    #
    # # rfc.predict(X_test)  y_target values for the model trained
    #
    #
    # #y_predict = rfc.predict(X_test)
    # #y_scores_rfc = rfc.decision_function(X_test)
    #
    #
    # print(y_decisionfunction_scores_rfc)

    # print(df_train.columns)

    aux1 = df_train[cols]
    aux2 = df_train['compliance']

    # divide source data into train-set and test-set, with df_train
    X_train, X_test, y_train, y_test = train_test_split(df_train[cols], df_train['compliance'])

    # create SVectorMachine, parameters: kernel function = 'linear, random_state=0
    #svm = SVC(kernel='linear', random_state=0)
    # grid_values for optimization to iterate. parameters: 'gamma', 'C'
    #grid_values = {'gamma': [0.01, 0.1, 1, 10], 'C': [0.01, 0.1, 10, 20, 100]}


    # create RandomForestRegressor, parameters: random_state
    regr_rf = RandomForestRegressor(max_features=3, random_state=0)


    # max_features= np.log2(len(df_test.columns)),
    # grid_values for optimization to iterate. parameters: 'n_estimators', 'max_depth', 'n_jobs'
    grid_values = {'n_estimators': [10,30,50], 'max_depth': [None, 10, 30, 50], 'n_jobs': [1, 3, 5] }
    # 'n_estimators': [10,40,50,100]
    # 'max_depth': [10, 30, 50, 100]
    # 'n_jobs': [1, 3, 5, 7]


    # create GradientBoostingClassifier, parameters: random_state=0
    #gbc = GradientBoostingClassifier(random_state=0)
    # grid_values GradientBoostingClassifier for optimization to iterate. parameters: 'gamma', 'C'
    #grid_values = {'n_estimators': [1,5,10], 'learning_rate': [0.01, 0.1, 1], 'n_estimators': [10,20,50,100], 'max_depth':[3,4,5]}



    # create GridSearchCV parameter optimizer, parameters: model = RandomForestRegressor, param_grid = grid_values, scoring='roc_auc'
    grid_clf_rfr = GridSearchCV(regr_rf, param_grid=grid_values, scoring='roc_auc')

    # fit/train GridSearchCV optimizer with train-set
    grid_clf_rfr.fit(X_train, y_train)

    # get best parameters/optimized parameters for the model trained with train-set
    # get evaluation metric of the model, given the scoring metric
    print('GridSearchCV optimized parameters (max. AUC): ', grid_clf_rfr.best_params_)
    print('GridSearchCV best score (scoring= AUC', grid_clf_rfr.best_score_)


    y_predict = grid_clf_rfr.predict(X_test)
    y_predict_index = X_test.ticket_id

    #print( pd.DataFrame(grid_clf_rfr.predict(X_test), X_test.ticket_id ) )

    print('\b')
    print(aux1)


    return pd.DataFrame(y_predict, y_predict_index)


blight_model()