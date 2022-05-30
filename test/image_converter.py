from pdf2image import convert_from_path
# pages = convert_from_path('Kailash.pdf', 500)
# for i in range(len(pages)):
#    page = pages[i]
#    page.save('Kailash/output_{:03}.jpg'.format(i), 'JPEG')

def image_converter(filename):
    pages = convert_from_path(filename, 500)
    for i in range(len(pages)):
        page = pages[i]
        page.save(filename.replace('.pdf', '') + '/output_{:03}.jpg'.format(i), 'JPEG')
        
image_converter('Kailash.pdf')