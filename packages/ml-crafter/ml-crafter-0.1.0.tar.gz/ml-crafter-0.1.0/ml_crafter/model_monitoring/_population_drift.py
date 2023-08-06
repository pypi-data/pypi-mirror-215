import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def CSI(dev, cur, devFeature, curFeature,  bins=None):
    
    """
 
    :param dev: development/benchmark dataset.
    :param cur: current dataset.
    :param devFeature: Feature used to check.
    :param curFeature: Feature used to check.
    :param bins: using bins if there is. For numerical features need to specify this
    :return: PSI and IV
    
    PSI < 0.1 - No change. You can continue using existing model.
    PSI >=0.1 but less than 0.2 - Slight change is required.
    PSI >=0.2 - Significant change is required. Ideally, you should not use this model any more.

    """
    
    if bins is not None:
        curata = pd.cut(cur[curFeature], bins=bins)
        devata = pd.cut(dev[devFeature], bins=bins)
    else:
        devata=dev[devFeature]
        curata=cur[curFeature]
             
    agg=pd.DataFrame({devFeature:devata.value_counts().sort_index().index
                      , 'dev':devata.value_counts().sort_index().values})
    cur=pd.DataFrame({'Feature':curata.value_counts().sort_index().index
                      , 'test':curata.value_counts().sort_index().values})

    agg=pd.merge(agg,cur,left_on=devFeature,right_on='Feature',how='inner')
    agg['test']=agg['test'].fillna(0)

    agg=agg.set_index(devFeature)
    del agg['Feature']

    agg['devPop'] = agg['dev']/agg['dev'].sum()
    agg['testPop'] = agg['test']/agg['test'].sum()
    agg['change'] = agg['testPop'] - agg['devPop']
    agg['ratio'] = agg['testPop']/agg['devPop']
    agg = agg.fillna(0)
    agg['WoE'] = agg['ratio'].apply(lambda x: np.log(x)).apply(lambda x: 0 if np.isinf(x) else x )
    agg = agg.fillna(0)
    agg['IV'] = agg['WoE']*agg['change']

    PSI = agg['IV'].sum()
    
    return PSI, agg


def get_origin_feature_from_one_hot(df: pd.DataFrame,
                                    category_names_list,
                                    feature_name: str
                                    ) -> pd.DataFrame:
    """
    This function can be used to get the original feature from
    one hot encoded feature

    :param category_names_list: List-  Dummy variables in a list
    :param feature_name: str -  Name of the new column to be created

    :return: pd.DataFrame - the original dataframe with the UN-hotencoded feature
                            (original feature before one-hot encoding)


    """

    # ex: category_names_list = [col for col in df.columns if col.startswith('index_con')]

    values = df[category_names_list].idxmax(axis=1)
    df = df.assign(feature_name=values)
    df = df.rename(columns={'feature_name': feature_name})

    return df


def calc_CSI(train,
             test,
             feature,
             feature_type,
             one_hot_prefix = None,
             categorical_num_mapping_dict = None,
             bins_q = 6
            ):
    
    """
    :param train: development/benchmark dataset.
    :param test: current dataset.
    :param feature: Feature to check. Can be set to None if one_hot_prefix is specified
    :param feature_type: feature type either 'numerical' or 'categorical'
    :param one_hot_prefix: if the feature is one-hot-encoded specify the prefix
    :param categorical_num_mapping_dict:  if the feature is target encoded, specify the value to string dict to
                                          transform back to the string format
    :param bins_q: If the feature is numerical, the feature will be binned using pandas.qcut, Specify the
                   q (quantile) parameter for pandas.qcut
    :return: PSI and IV in a dataframe
    
    PSI < 0.1 - No change. You can continue using existing model.
    PSI >=0.1 but less than 0.2 - Slight change is required.
    PSI >=0.2 - Significant change is required. Ideally, you should not use this model any more.

    
    """
    if feature_type not in ['numerical','categorical']:
        raise ValueError(f"feature_type must be either 'numerical' or 'categorical' ")
        
    if train[feature].isin([0, 1]).all():
        feature_type = 'categorical'
        
    if categorical_num_mapping_dict is not None:

        rounded_dict = {}

        # if the mapping has long floats in the key, they will not match
        # with the values in the df - dataframe, so we are rounding in both
        # in this dictionary and the dataframe

        for key, value in categorical_num_mapping_dict.items():
            rounded_key = round(key, 8)
            rounded_dict[rounded_key] = value

        train[feature] = train[feature].round(8)
        train[feature] = train[feature].replace(rounded_dict)
        
        test[feature] = test[feature].round(8)
        test[feature] = test[feature].replace(rounded_dict)
        
        feature_type = 'categorical'

    if one_hot_prefix is not None:    
        if one_hot_prefix[-1] == '_':
            one_hot_prefix = one_hot_prefix[:-1]

            if feature is None:
                feature = one_hot_prefix

            category_names_list_trn = [col for col in train.columns if col.startswith(one_hot_prefix)]
            category_names_list_tst = [col for col in test.columns if col.startswith(one_hot_prefix)]

            train = get_origin_feature_from_one_hot(train, category_names_list_trn, feature)
            test = get_origin_feature_from_one_hot(test, category_names_list_tst, feature)

            train[one_hot_prefix] = train[one_hot_prefix].str.replace(one_hot_prefix + '_', '')
            test[one_hot_prefix] = test[one_hot_prefix].str.replace(one_hot_prefix + '_', '')

            if len(set(category_names_list_trn) - set(category_names_list_tst)) > 0:
                logging.info('Some categories missing in test dataset')

            if len(set(category_names_list_tst) - set(category_names_list_trn)) > 0:
                logging.info('Some categories missing in train dataset')

            feature_type = 'categorical'

    if feature_type == 'categorical': 
        train2 = train[[feature]].copy()
        #train2[feature] = train2[feature].astype(str)
        train2 = train2.dropna()
       
        test2 = test[[feature]].copy()
            
        test2 = test2.dropna()
        psi, agg = CSI(train2, test2, feature, feature, bins=None)
        
    else :    
        test2 = test[[feature]].copy()
        
        test2 = test2.dropna()
        test2 = test2[test2[feature]>=0]
        
        train2 = train[[feature]].copy()
        #train2[feature] = train2[feature].astype(float)
        
        train2 = train2.dropna()
        train2 = train2[train2[feature]>=0]
        
        cuts = pd.qcut(train2[feature].dropna().astype(float).values.reshape(-1, 1).reshape(-1)
                       , bins_q, duplicates='drop').unique()
        rights = sorted([x.right for x in cuts])[:-1]
        bins = [-999999999] + rights + [999999999]
        psi, agg = CSI(train2, test2, feature, feature, bins)
        
    return psi , agg
