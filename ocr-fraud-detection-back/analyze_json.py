import json

# Opening JSON file
with open('out_json/output_000.json', 'r') as openfile:
  
    # Reading from json file
    json_object = json.load(openfile)
  
# print(json_object)
# print(type(json_object))

blocks=json_object['Blocks']
# print(blocks)


blocks_map = {}
table_blocks = []
for block in blocks:
    blocks_map[block['Id']] = block
    if block['BlockType'] == "TABLE":
        table_blocks.append(block)

for index, table in enumerate(table_blocks):
    rows = {}
    for relationship in table['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                print('++++++++++++++++++++++')
                print(cell)
                # if cell['BlockType'] == 'CELL':
                #     row_index = cell['RowIndex']
                #     col_index = cell['ColumnIndex']
                #     if row_index not in rows:
                #         # create new row
                #         rows[row_index] = {}
                        
                #     # get the text value
                #     rows[row_index][col_index] = get_text(cell, blocks_map)

# blocks_map = {}
# table_blocks = []
# for block in blocks:
#     blocks_map[block['Id']] = block
#     if block['BlockType'] == "TABLE":
#         table_blocks.append(block)
#         # print(block)
#         print(block.keys())
#         print(block['Relationships'])
#         for relationship in block['Relationships']:
#             if relationship['Type'] == 'CHILD':
#                 for child_id in relationship['Ids']:
#                     cell = blocks_map[child_id]
#                     print('++++++')
#                     print(cell)
#                     # if cell['BlockType'] == 'CELL':
#                     #     row_index = cell['RowIndex']
#                     #     col_index = cell['ColumnIndex']
#                     #     if row_index not in rows:
#                     #         # create new row
#                     #         rows[row_index] = {}
                            
#                     #     # get the text value
#                     #     rows[row_index][col_index] = get_text(cell, blocks_map)
        