from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import werkzeug
import pandas as pd
import numpy as np
# import tabula
import time
import datetime
# import re
from textract_wrapper import TextractWrapper
from pdf2image import convert_from_path
import boto3
import json
import os

import csv

app = Flask(__name__)
api = Api(app)
text_parser = reqparse.RequestParser()
text_parser.add_argument("text", type=str, help="needed a text input in string format", location='form')
text_parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files') 

textract_client = boto3.client('textract',region_name='us-west-2')
feature_types = ['TABLES', 'FORMS']
blocks = [{'BlockType': 'TEST'}]

twrapper = TextractWrapper(textract_client, None, None)

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    rows_bb = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        rows_bb[row_index] = {}
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
                    rows_bb[row_index][col_index] = cell['Geometry']['BoundingBox']
    return rows, rows_bb

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text

def generate_table_csv(table_result, blocks_map, table_index):
    rows, rows_bb = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
        
    csv += '\n\n\n'
    return csv, rows_bb

def image_converter(filename):
    pages = convert_from_path(filename, 500)
    for i in range(len(pages)):
        page = pages[i]
        page.save(filename.replace('.pdf', '') + '/output_{:03}.jpg'.format(i), 'JPEG')

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
    
    
    
    return bank_statement_df, pages_retrieved, info


@app.route("/")
def hello_world():
    return jsonify({'hello': "Hello, World!"})

class predict(Resource):
    def post(self,):
        pred = False
        args = text_parser.parse_args()
        filename = args['text']
        name_var = filename.replace('.pdf', '')
        if name_var in os.listdir():
            print("caching from existing images")
        else:
            print("converting pdf to images")
            os.mkdir(name_var)
            image_converter(filename)
                    
                
        if name_var + '_out_json' in os.listdir():
            print("using cached version of Textract output")
        else:
            os.mkdir(name_var + '_out_json')
            os.mkdir(name_var + '_out_bb')
            os.mkdir(name_var + '_out')
            for image in os.listdir(name_var):

                got_blocks = twrapper.analyze_file(feature_types, document_file_name=name_var + '/'+ image)
                # Serializing json 
                json_object = json.dumps(got_blocks, indent = 4)                
                # Writing to sample.json
                with open(name_var + '_out_json/' + image.replace('jpg', 'json'), "w") as outfile:
                    outfile.write(json_object)
                

                # Get the text blocks
                blocks=got_blocks['Blocks']

                blocks_map = {}
                table_blocks = []
                for block in blocks:
                    blocks_map[block['Id']] = block
                    if block['BlockType'] == "TABLE":
                        table_blocks.append(block)

                csv_o = ''
                rows_dict = dict()
                for index, table in enumerate(table_blocks):
                    csv_in, rows_bb = generate_table_csv(table, blocks_map, index +1)
                    csv_o += csv_in
                    rows_dict.update(rows_bb)
                    csv_o += '\n\n'
                    
                output_file = name_var + '_out/' + image.replace('jpg', 'csv')
                with open(output_file, "wt") as fout:
                    fout.write(csv_o)
                    
                output_file = name_var + 'out_bb/' + image.replace('jpg', 'json')
                with open(output_file, "w") as fout:
                    json.dump(rows_dict, fout)
                    # fout.write(csv)
        ALL_FILEPATHS = [name_var + "_out/" + f for f in os.listdir(name_var + "_out")]
        bank_statement_df, pages_retrieved, info = get_bank_statement_info(ALL_FILEPATHS)
        
        result = dict()
        
        if info['outliers_found'] == False:
            result['outliers_found'] = False
        else:
            result['outliers_found'] = True
            result['info'] = info
            outliers = info['outliers']
            outlier_coordinates = dict()
            outlier_coord = []
            final_coords = []
            for outlier in outliers.values():
                outlier_coordinates['pg_no'] = outlier['pg_no']
                
                print(outlier['pg_no'])
                print(outlier['Particulars '])
                print(name_var + '_out/' + '/output_{:03}.csv'.format(outlier['pg_no'] - 1))
                with open(name_var + '_out/' + '/output_{:03}.csv'.format(outlier['pg_no'] - 1), 'r') as csvfile:
                    filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    row_nbr = 0
                    for row in filereader:
                        if outlier['Particulars '][0:10] in ','.join(row):
                            outlier_coordinates[row_nbr] = row_nbr 
                            with open(name_var + '_out_bb' + '/output_{:03}.json'.format(outlier['pg_no'] - 1), 'r') as openfile:  
                                # Reading from json file
                                json_object = json.load(openfile)
                                coord = json_object[str(row_nbr-1)]
                                
                                final_coord = {"Left":coord['1']["Left"],
                                               "Top": coord['1']["Top"],
                                               "Width":coord[sorted(coord.keys())[-1]]["Left"] + coord[sorted(coord.keys())[-1]]["Width"], 
                                                "Height":coord[sorted(coord.keys())[-1]]["Top"] + coord[sorted(coord.keys())[-1]]["Height"]}
                                outlier_coordinates['coordinates'] = coord
                                outlier_coord.append({'row_nbr': row_nbr, 'pg_no': outlier['pg_no'] - 1, 'coord':coord, 'final_coord': final_coord})
                        row_nbr += 1
                # result['outlier_coordinates'] =  outlier_coordinates   
                result['outlier_coord'] =  outlier_coord   
                 
            


        # if len(outlier_ind) > 0:
            
        #     result['total_transactions'] = rows
        #     result['outliers_found'] = True
        #     result['outlier_indices'] = outlier_ind
        #     result['outliers'] = df[outliers].to_dict('index')
        # else:
        #     result['outliers_found'] = False
            
        return result

        





api.add_resource(predict,'/predict')
# api.add_resource(predict_redact,'/predict_redact/<string:module>/<string:model>')
# api.add_resource(redact,'/redact/<string:module>/<string:model>')
# api.add_resource(predict_extension,'/predict_extension/<string:module>/<string:model>')


if __name__ == "__main__":
    app.run(debug=True)