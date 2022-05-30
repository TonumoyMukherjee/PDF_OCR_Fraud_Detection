from textract_wrapper import TextractWrapper
import boto3
from pdf2image import convert_from_path
import json
import os

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

# for image in os.listdir('Kailash/'):

#     got_blocks = twrapper.analyze_file(feature_types, document_file_name='Kailash/'+ image)
    
    
#     # Serializing json 
#     json_object = json.dumps(got_blocks, indent = 4)
    
#     # Writing to sample.json
#     with open('out_json/' + image.replace('jpg', 'json'), "w") as outfile:
#         outfile.write(json_object)
    

#     # Get the text blocks
#     blocks=got_blocks['Blocks']

#     blocks_map = {}
#     table_blocks = []
#     for block in blocks:
#         blocks_map[block['Id']] = block
#         if block['BlockType'] == "TABLE":
#             table_blocks.append(block)

#     csv = ''
#     rows_dict = dict()
#     for index, table in enumerate(table_blocks):
#         csv_in, rows_bb = generate_table_csv(table, blocks_map, index +1)
#         csv += csv_in
#         rows_dict.update(rows_bb)
#         csv += '\n\n'
        
#     output_file = 'out/' + image.replace('jpg', 'csv')
#     with open(output_file, "wt") as fout:
#         fout.write(csv)
        
#     output_file = 'out_bb/' + image.replace('jpg', 'json')
#     with open(output_file, "w") as fout:
#         json.dump(rows_dict, fout)
#         # fout.write(csv)
    
def image_converter(filename):
    pages = convert_from_path(filename, 500)
    for i in range(len(pages)):
        page = pages[i]
        page.save(filename.replace('.pdf', '') + '/output_{:03}.jpg'.format(i), 'JPEG')


filename = "AXIS_statement.pdf"
name_var = filename.replace('.pdf', '')
# if name_var in os.listdir():
#     print("caching from existing images")
# else:
print("converting pdf to images")
os.mkdir(name_var)
image_converter(filename)
            
        
# if name_var + '_out_json/' in os.listdir():
#     print("using cached version of Textract output")
# else:
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

    csv = ''
    rows_dict = dict()
    for index, table in enumerate(table_blocks):
        csv_in, rows_bb = generate_table_csv(table, blocks_map, index +1)
        csv += csv_in
        rows_dict.update(rows_bb)
        csv += '\n\n'
        
    output_file = name_var + '_out/' + image.replace('jpg', 'csv')
    with open(output_file, "wt") as fout:
        fout.write(csv)
        
    output_file = name_var + '_out_bb/' + image.replace('jpg', 'json')
    with open(output_file, "w") as fout:
        json.dump(rows_dict, fout)
        # fout.write(csv)
