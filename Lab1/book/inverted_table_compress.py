source = open('inverted_table_file.txt', 'r')
target = open('inverted_table_gap.txt', 'w')

line = source.readline()
while line:
    pre_element = 0
    elements = line.replace('\n', '').replace('\r', '').split('\t')
    for element in elements[:-1]:
        print(element)
        target.write(str(int(element)-pre_element)+'\t')
        pre_element = int(element)
    target.write('\n')
    line = source.readline()