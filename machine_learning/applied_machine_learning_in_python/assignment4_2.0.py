import pandas as pd
import numpy as np


def blight_model():
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.metrics import roc_auc_score

    # cargar dataset de train-set y test-set
    df_train = pd.read_csv('train.csv', encoding="ISO-8859-1")
    df_test = pd.read_csv('test.csv')

    # cargar addresses y coordenadas  lat-lon
    addresses = pd.read_csv('addresses.csv')
    latlons = pd.read_csv('latlons.csv')


    # drop all Null-NaN entries df_train
    df_train = df_train[np.isfinite(df_train['compliance'])]


    # over-over write df_train.country, on condition =='USA'
    df_train = df_train[df_train.country == 'USA']

    # over-over write df_test.country, on condition =='USA'
    df_test = df_test[df_test.country == 'USA']


    # unir  df_train y df_test con addresses
    add_latlons = pd.merge(addresses, latlons, on= 'address')
    df_train = pd.merge(df_train, add_latlons, on='ticket_id')
    df_test = pd.merge(df_test, add_latlons, on='ticket_id')

    # df_train.drop([cols])  eliminar columnas que no esten en test_set y que sean data leakage
    df_train.drop(['agency_name', 'inspector_name', 'violator_name', 'non_us_str_code', 'violation_description',
                'grafitti_status', 'state_fee', 'admin_fee', 'ticket_issued_date', 'hearing_date',
                'payment_amount', 'balance_due', 'payment_date', 'payment_status',
                'collection_status', 'compliance_detail',
                'violation_zip_code', 'country', 'address', 'violation_street_number',
                'violation_street_name', 'mailing_address_str_number', 'mailing_address_str_name',
                'city', 'state', 'zip_code', 'address'], axis=1, inplace=True)

    # LabelEncoder()  crear Label Encoder de columnas con string
    #  LabelEncoder() de columna 'disposition'
    label_encoder = LabelEncoder()
    # fi/train LabelEncoder con df_train y df_test en columna 'disposition'
    label_encoder.fit(df_train['disposition'].append(df_test['disposition'], ignore_index=True))

    # transform df_train['disposition'] con LabelEncoder()
    df_train['disposition'] = label_encoder.transform(df_train['disposition'])
    # transform df_test['disposition'] con LabelEncoder()
    df_test['disposition'] = label_encoder.transform(df_test['disposition'])

    #  LabelEncoder() de columna 'violation_code'
    label_encoder = LabelEncoder()
    label_encoder.fit(df_train['violation_code'].append(df_test['violation_code'], ignore_index=True))
    df_train['violation_code'] = label_encoder.transform(df_train['violation_code'])
    df_test['violation_code'] = label_encoder.transform(df_test['violation_code'])

    # df_train['lat'] fillna,  df_train['lon'] fillna
    # df_test['lat'] fillna,  df_test['lon'] fillna
    df_train['lat'] = df_train['lat'].fillna(df_train['lat'].mean())
    df_train['lon'] = df_train['lon'].fillna(df_train['lon'].mean())
    df_test['lat'] = df_test['lat'].fillna(df_test['lat'].mean())
    df_test['lon'] = df_test['lon'].fillna(df_test['lon'].mean())

    # extraer columnas de df_train
    cols = list(df_train.columns.values)
    # eliminar 'compliance' de lista de columnas de df_train
    cols.remove('compliance')

    # over-write df_test, on columns= cols
    df_test = df_test[cols]

    # dividir data-set entre train-set y test-set
    # train-test split utilizando X_data = df_train[cols]  y_target = df_train['compliance']
    X_train, X_test, y_train, y_test = train_test_split(df_train[cols], df_train['compliance'])

    # RandomForestRegressor crear modelo Arbol de Regresión
    regr_rf = RandomForestRegressor()

    # crear grid_values sobre los que itera GridSearchCV para optimizar
    grid_values = {'max_features': [1, 3, 5], 'n_estimators': [10, 50], 'max_depth': [None, 10, 30]}

    # GridSearchCV crear optimizador de parametros,  parametros: modelo= regr_rf, param_grid=grid_values, scoring='roc_auc'
    grid_clf_auc = GridSearchCV(regr_rf, param_grid=grid_values, scoring='roc_auc')

    # fit/train GridSearchCV con X_train, y_train
    grid_clf_auc.fit(X_train, y_train)

    # obtener los parámetros óptimos del modelo, y el valor óptimo de evaluation metric
    print('Grid best parameter (max. AUC): ', grid_clf_auc.best_params_)
    print('Grid best score (AUC): ', grid_clf_auc.best_score_)

    # crear DataFrame con grid_clf_auc.predict(df_test) y index = df_test.ticket_id
    df_prob = pd.DataFrame(grid_clf_auc.predict(df_test), df_test.ticket_id)
    print(df_prob)


    return df_prob


blight_model()