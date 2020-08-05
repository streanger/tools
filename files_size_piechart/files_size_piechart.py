'''
info:
    -script for showing files size as piechart
    -after writing script i realize that matplotlib calculates percentage by itself :)
todo:
    -think of block chart
    -think of interactive chart
    -think of directories/files mode
'''

import sys
import os
import matplotlib.pyplot as plt


def script_path():
    '''change dir, to current script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def get_size(start_path='.'):
    '''
    -copied from:
        https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    -modified
    '''
    data = {}
    # total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                file_size = os.path.getsize(fp)
                # total_size += file_size
                data[f] = file_size
                
    # return total_size
    # return data, total_size
    return data
    
    
def calc_to_percent(data):
    '''
    data - list of two element tuples
    convert numbers in data to percentage value
    '''
    total_size = sum([value for _, value in data])
    # percentage_data = [(file, round(100*value/total_size, 2)) for file, value in data]
    percentage_data = [(file, 100*value/total_size) for file, value in data]
    return percentage_data
    
    
def join_small(data, low_percent_level=None, total_items=None):
    '''
    data - list of two element tuples
    join small items into one;
    if low_percent_level specified - low items under this level
    if total_items specified - join items to get total number of them equal to specified
    '''
    # breakpoint()
    if (not low_percent_level) and (not total_items):
        return join_small
        
    if low_percent_level:
        if not (0 < low_percent_level <= 100):
            return data
            
        out = []
        rest_of_data = 0
        for (file, value) in data:
            if value <= low_percent_level:
                rest_of_data += value
            else:
                out.append((file, value))
        if rest_of_data:
            out.append(('rest of data', rest_of_data))
            
    if total_items:
        if not (total_items > 0):
            return data
            
        if len(data) <= total_items:
            return data
            
        data = sorted(data, key=lambda x: x[1], reverse=True)
        out = data[:total_items-1]
        # breakpoint()
        rest_of_data = sum([value for (_, value) in data[total_items-1:]])
        if rest_of_data:
            out.append(('rest of data', rest_of_data))
    out = sorted(out, key=lambda x: x[1], reverse=True)
    return out
    
    
def shorten_names(data):
    '''make filenames shorter; for now max length is fixed and equal 15'''
    out = []
    for file, value in data:
        # if file is shorten return it
        if len(file) <= 15:
            out.append((file, value))
            continue
            
        # if dot in file, return part of first
        if '.' in file:
            parts = [item[::-1] for item in file[::-1].split('.', 1)][::-1]
            last = parts[-1]
            first = parts[0]
            if len(last) < len(first):
                last = last[-5:]
                first = first[:(12-len(last))]
            else:
                first = first[:5]
                last = last[-(12-len(first)):]
            new = '{}...{}'.format(first, last)
            # print(file, new, len(file), len(new))   # DEBUG
            # if len(new) != 15: input('\nHERE\n')    # DEBUG
            out.append((new, value))
            continue
            
        # if file is longer than 15 and there is no dot
        # just cut 15 first elements
        out.append((file[:15], value))
    return out
    
def calc_explode(data, to_explode, start=0.1, depend_on_value=False):
    '''list of tuples with data; to_explode e.g. 5; start (distance) e.g. 0.1'''
    total = len(data)
    if to_explode > total:
        to_explode = total
    rest = total - to_explode
    
    if not depend_on_value:
        explode = [start*(x/total) for x in range(1, to_explode+1)][::-1]
    else:
        data = sorted(data, key=lambda x: x[1], reverse=True)
        values = [val for (_, val) in data[:to_explode]]
        explode = [start*(val/100) for val in values]
        
    rest = [0 for x in range(rest)]
    out = tuple(explode + rest)        
    return out
    
    
def plot_pie_chart(data):
    labels, sizes = list(zip(*data))
    items_number = len(data)
    explode = calc_explode(data, 5, start=0.1, depend_on_value=False)
    
    fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.pie(sizes,
            explode=explode,
            labels=labels,
            autopct='%1.2f%%',
            shadow=False,
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor' : 'black', 'antialiased': True}
            )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    return True
    
    
if __name__ == "__main__":
    script_path()
    
    # ********* generate and perform data *********
    data = get_size('.')
    data = list(data.items())
    data = calc_to_percent(data)
    # data = join_small(data, low_percent_level=2)      # get items over n[%]
    data = join_small(data, total_items=10)           # get n-th items
    data = shorten_names(data)
    # data = [('file_{:02}'.format(key), value) for key, (file, value) in enumerate(data)]  # DEBUG
    
    
    # ********* show data in text format *********
    sum_of_percent = sum([value for (_, value) in data])
    print('sum_of_percent: {:.2f}'.format(sum_of_percent))
    
    for key, item in enumerate(data):
        print('{}: {:.2f}[%]'.format(*item))
        # if not (key+1)%20:
            # input()
            
    # ********* plot data *********
    plot_pie_chart(data)
    
    