import sys
import os
import codecs


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def read_file(file):
    '''read data from specified file'''
    content = ''
    with codecs.open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return content
    
    
def write_file(file, data):
    '''write data to .txt file, with specified data'''
    with codecs.open(file, "w", encoding="utf-8") as f:
        f.write(data)
    return True
    
    
def combine_txt(files, clear_data=True):
    '''read content from all .txt files and write to combined string
    clear_data - remove newlines before and after lines with text
    '''
    str_container = []
    for key, file in enumerate(files):
        header = '{}) {}'.format(key+1, file)
        file_content = read_file(file)
        
        # if file contain only blank chars - append only header
        if clear_data and (not file_content.strip()):
            str_container.append(header)
            continue
            
        lines = file_content.splitlines()
        if clear_data:
            for key, line in enumerate(lines):
                if line.strip():
                    lines = lines[key:]
                    break
            lines = lines[::-1]
            for key, line in enumerate(lines):
                if line.strip():
                    lines = lines[key:]
                    break
            lines = lines[::-1]
            
        converted = '\n'.join(['{}{}'.format(' '*4, line) for line in lines])
        single_str = '\n'.join([header, converted])
        str_container.append(single_str)
        
    join_items_str = '\n'
    if clear_data:
        join_items_str = '\n\n'
        
    return join_items_str.join(str_container) + '\n'
    
    
if __name__ == "__main__":
    script_path()
    files = [file for file in os.listdir() if file.endswith('.txt')]
    combined = combine_txt(files)
    write_file('out.txt', combined)
