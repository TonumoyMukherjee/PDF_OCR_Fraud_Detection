from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import werkzeug
import pandas as pd
import numpy as np
import tabula
import time
import datetime
import re

app = Flask(__name__)
api = Api(app)
text_parser = reqparse.RequestParser()
text_parser.add_argument("text", type=str, help="needed a text input in string format", location='form')
text_parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files') 



def table_extraction_from_pdf(pdf_file):
    df = tabula.read_pdf(pdf_file, pages = 'all', lattice = True)
    
    new_df = pd.DataFrame()       # Empty DataFrame
    for i in range(len(df)):
        new_df = new_df.append(df[i])

    new_df = new_df.replace({'\r':' '}, regex = True)          # removing unwanted characters from Date column
    
    new_df['Txn Date'] = pd.to_datetime(new_df['Txn Date'])            # Parsing / Converting to Datetime
    new_df['Value\rDate'] = pd.to_datetime(new_df['Value\rDate'])      # Parsing / Converting to Datetime
    
    new_df.reset_index(drop=True, inplace=True)     # Reseting index

    return new_df


# Function to extract Date column
def get_date_columns(df):
    date_cols = []
    # print(df.info())
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
                print(f'{col} ==contains date')
                # date_cols.append(col)
            except:
                pass
    
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            print(f'{col}:: Contains datelike format')
            date_cols.append(col)
            
    return date_cols


# Function to extract transaction column
def get_transaction_columns(df):
    transaction_cols = []
    for col in df.columns:
        try:
            if df[col].dtype == 'float64':
                df[col].apply(str).str.extract(r'(\d+.\d{1,2})')
                print(f'{col}: is like a Transaction')
                transaction_cols.append(col)
            elif type(df[col][0]) == float:
                print(f'{col}: is like a Transaction')
                transaction_cols.append(col)
            elif df[col].dtype == 'object':
                if '.' in df[col][0]:
                    df[col].apply(str).str.extract(r'(\d+[.]\d{1,2})')
                    print(f'{col}: is like a Transaction')
                    transaction_cols.append(col)
          
        except:
            pass
        
    return transaction_cols

   
def get_outlier(df, colname):
    cred_mean = df[colname].mean(skipna=True)
    cred_std = df[colname].std(skipna=True)
    cred_outlier = (df[colname] - cred_mean) > (2 * cred_std)
    return cred_outlier


@app.route("/")
def hello_world():
    return jsonify({'hello': "Hello, World!"})

class predict(Resource):
    def post(self,):
        pred = False
        args = text_parser.parse_args()
        filename = args['text']
        print("ARGS=>",args)
        df = table_extraction_from_pdf(filename)
        date_cols = get_date_columns(df)
        transaction_cols = get_transaction_columns(df)

        for c in transaction_cols:
            df[c] = df[c].replace({',':''}, regex = True)          # removing unwanted characters from Date column
            df[c] = df[c].astype(float)

        outliers = get_outlier(df, 'Credit')
        outlier_ind = list(df[outliers].index)
        # print(df[outliers])
        result = dict()
        rows = df.shape[0]

        if len(outlier_ind) > 0:
            
            result['total_transactions'] = rows
            result['outliers_found'] = True
            result['outlier_indices'] = outlier_ind
            result['outliers'] = df[outliers].to_dict('index')
        else:
            result['outliers_found'] = False
            
        return jsonify(result)

        





api.add_resource(predict,'/predict')

# api.add_resource(predict_redact,'/predict_redact/<string:module>/<string:model>')
# api.add_resource(redact,'/redact/<string:module>/<string:model>')
# api.add_resource(predict_extension,'/predict_extension/<string:module>/<string:model>')


if __name__ == "__main__":
    app.run(debug=True)