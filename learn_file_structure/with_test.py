# not use with 
# f = open('myFile.txt', 'w', encoding='utf8')
# f.write('test')
# f.close 

#use with 

with open('mytextfile.txt', 'w', encoding='utf-8') as f: 
    f.write('test')