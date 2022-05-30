import pandas as pd
import os

DATADIR = "C:/SUMEET/WORK/OCR/data/output-csvs/out"

ALL_FILEPATHS = [DATADIR + "/" + f for f in os.listdir(DATADIR)]

def get_outlier(df, colname):
    cred_mean = df[colname].mean(skipna=True)
    cred_std = df[colname].std(skipna=True)
    cred_outlier = (df[colname] - cred_mean) > (2 * cred_std)
    return cred_outlier

def get_page_no(filepath):
    pg_no = int(filepath.split("/")[-1].split("_")[-1].split(".")[0]) + 1
    
    return pg_no
        
# print(ALL_FILEPATHS)


def get_bank_statement_info(all_filepaths):
    dfs = []
    pages_retrieved = []
    columns = []
    required_columns = ['Tran Date ', 'Particulars ', 'Debit ', 'Credit ', 'Balance ', 'Init. Br ', 'pg_no']
    for f in all_filepaths:
#         print(f)
        pg_no = get_page_no(f)
        if pg_no == 1:
            df = pd.read_csv(f, skiprows = 2, on_bad_lines='skip')
            columns.append(df.columns)
            df["pg_no"] = pg_no
#             print(df.shape)
            dfs.append(df)
            pages_retrieved.append(pg_no)
            
        else:
            try:
                df = pd.read_csv(f, skiprows = 1, on_bad_lines='skip', header = None)
                df.columns = columns[0]
                df["pg_no"] = pg_no
#                 print(df.shape)
                dfs.append(df)
                pages_retrieved.append(pg_no)
            except:
                pass
    
#     print(len(dfs))
    bank_statement_df = pd.concat(dfs, axis = 0)
    bank_statement_df = bank_statement_df[required_columns].iloc[1:-2]
    bank_statement_df = bank_statement_df.reset_index().drop("index", axis = 1)
    total_transactions = bank_statement_df.shape[0]
    outliers = get_outlier(bank_statement_df, 'Credit ')
    bank_statement_df["outliers"] = outliers
    outliers_df = bank_statement_df[bank_statement_df["outliers"] == True]
    outlier_ind = list(outliers_df.index)
    
    info = {}
    if len(outlier_ind) > 0:
        info['total_transactions'] = total_transactions
        info['outliers_found'] = True
        info['outlier_indices'] = outlier_ind
        info['outliers'] = outliers_df.to_dict('index')
#         info['outliers'] = outliers_df
    else:
        info['outliers_found'] = False
        outlier_coordinates = dict()
        for outlier in outliers.values():
            with open('out_json/output_000.json', 'r') as openfile:  
                # Reading from json file
                json_object = json.load(openfile)
            
    
    
    
    return bank_statement_df, pages_retrieved, info


bank_statement_df, pages_retrieved, info = get_bank_statement_info(ALL_FILEPATHS)
print(bank_statement_df.shape)