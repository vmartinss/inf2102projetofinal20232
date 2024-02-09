import pandas as pd
import json


def get_package_name(file_path: str) -> str:
    splited_path = file_path.split('\\')

    new_package_name = ''
    df_organic = pd.read_json('output.json')
    df_pmd = pd.read_csv('report.csv')
    df_designate1 = pd.read_csv('DesignSmells.csv', error_bad_lines=False)
    df_designate2 = pd.read_csv('ImplementationSmells.csv', error_bad_lines=False)
    df_repository_info = pd.read_csv('repository_info.csv', error_bad_lines=False)
    for i in range(9,len(splited_path)-1):
        new_package_name +='.'
        new_package_name += (splited_path[i])

    return new_package_name[1:]

def get_code_name(file_path: str) -> str:
    splited_path = file_path.split('\\')
    return splited_path[-1][:-5]

def is_long_method(x):
    return 1 if 'Long Method' in x.values else 0

def get_designate_data_filtered(df_designate: pd.DataFrame):

    df_designate['smell_Designite_num_aglomeration'] = 0

    df = df_designate.groupby(['Package Name','Type Name'])['smell_Designite_num_aglomeration'].count().reset_index()
    df2 = df_designate.groupby(['Package Name','Type Name'])['Implementation Smell'].agg(lambda x: is_long_method(x)).reset_index()

    df = pd.merge(df,df2,on=['Package Name','Type Name'])

    df['smell_Designite_aglomeration'] = (df['smell_Designite_num_aglomeration'] > 1).astype(int)

    df.rename(columns={'Implementation Smell': 'smell_Designite_longmethod'}, inplace=True)

    return df

def get_pmd_filtered_data(df_pmd: pd.DataFrame):
    df_pmd['File'] = df_pmd['File'].apply(lambda x: get_code_name(x))

    df_pmd['smell_PMD_num_aglomeration'] = 0
    df_pmd1 = df_pmd.groupby(['Package','File'])['smell_PMD_num_aglomeration'].count().reset_index()

    df_pmd2 = df_pmd.groupby(['Package', 'File'])['Rule'].agg(lambda x: ('ExcessiveMethodLength' in x.values)).astype(int).reset_index()
    df_pmd2.rename(columns={'Rule': 'smell_PMD_longmethod'}, inplace=True)
    df_pmd3 = df_pmd.groupby(['Package', 'File'])['Rule'].agg(lambda x: ('DataClass' in x.values)).astype(int).reset_index()
    df_pmd3.rename(columns={'Rule':'smell_PMD_dataclass'}, inplace=True)
    df_pmd4 = df_pmd.groupby(['Package', 'File'])['Rule'].agg(lambda x: ('GodClass' in x.values)).astype(int).reset_index()
    df_pmd4.rename(columns={'Rule':'smell_PMD_blob'}, inplace=True)

    df = pd.merge(df_pmd1, df_pmd2, on=['Package', 'File'])
    df = pd.merge(df, df_pmd3, on=['Package', 'File'])
    df = pd.merge(df, df_pmd4, on=['Package', 'File'])

    df.rename(columns={'Package': 'Package Name', 'File': 'Type Name'}, inplace=True)

    return df

def is_organic_longmethod(smells):
    for smell in smells:
        if smell['name'] == "LongMethod":
            return 1

    return 0

def is_organic_featureenvy(smells):
    for smell in smells:
        if smell['name'] == "FeatureEnvy":
            return 1

    return 0

def get_organic_filtered_data(df_organic: pd.DataFrame):

    df_organic = df_organic.explode('sourceFile').reset_index(drop=True)

    len(df_organic)
    df_organic['Package Name'] = df_organic['sourceFile'].apply(lambda x: get_package_name(x.values['fileRelativePath']))
    df_organic['Type Name'] = df_organic['sourceFile'].apply(lambda x: get_code_name(x.values['fileRelativePath']))

    df1 = df_organic.groupby(['Package Name','Type Name'])['smells'].agg(lambda x: is_organic_longmethod(x.values)).astype(int).reset_index()
    df1.rename(columns={'smells':'smell_Organic_longmethod'}, inplace=True)
    df2 = df_organic.groupby(['Package Name','Type Name'])['smells'].agg(lambda x: is_organic_featureenvy(x.values)).astype(int).reset_index()
    df2.rename(columns={'smells':'smell_Organic_featureenvy'}, inplace=True)

    df = pd.merge(df1,df2, on=['Package Name','Type Name'])

    return df

def get_organic_filtered_data(path):
    with open(path) as file_path:
        j = json.load(file_path)
    result = {
        'Package Name':[],
        'Type Name':[],
        'smell_Organic_longmethod':[],
        'smell_Organic_featureenvy':[]
    }

    for elem in j:
        for method in elem['methods']:
            result['Package Name'].append(get_package_name(method['sourceFile']['fileRelativePath']))
            result['Type Name'].append(get_code_name(method['sourceFile']['fileRelativePath']))
            result['smell_Organic_longmethod'].append(is_organic_longmethod(method['smells']))
            result['smell_Organic_featureenvy'].append(is_organic_featureenvy(method['smells']))

    return pd.DataFrame(result)



if __name__ == '__main__':

    df_organic = pd.read_json('output.json')
    df_pmd = pd.read_csv('report.csv')

    df_designate1 = pd.read_csv('DesignSmells.csv', error_bad_lines=False)
    df_designate2 = pd.read_csv('ImplementationSmells.csv', error_bad_lines=False)
    df_repository_info = pd.read_csv('repository_info.csv', error_bad_lines=False)
    df_designate = pd.merge(df_designate1, df_designate2, on=['Package Name', 'Type Name'])

    df = get_designate_data_filtered(df_designate)
    df2 = get_pmd_filtered_data(df_pmd)
    df3 = get_organic_filtered_data('output.json')
    # df3 = get_organic_filtered_data(df_organic)

    df_result = pd.merge(df,df2,on=['Package Name','Type Name'], how='outer')
    df_result = pd.merge(df_result,df3,on=['Package Name','Type Name'], how='outer')
    df_result.fillna(0, inplace=True)
    df_result['Stars'] = df_repository_info[df_repository_info['Repository Name'] == 'struts1']['Stars'].values[0]
    df_result['LOC'] = df_repository_info[df_repository_info['Repository Name'] == 'struts1']['LOC'].values[0]
    df_result['Number_of_Contributors'] = df_repository_info[df_repository_info['Repository Name'] == 'struts1']['Number of Contributors'].values[0]
    df_result['Commits'] = df_repository_info[df_repository_info['Repository Name'] == 'struts1']['Commits'].values[0]
    df_result.to_csv('result.csv')

    # print(len(df_organic))
    # print(len(df_organic.explode('sourceFile').reset_index(drop=True)))
