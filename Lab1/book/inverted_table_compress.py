source = open('inverted_table_file.txt', 'r')
target = open('inverted_table_gap.txt', 'wb')

line = source.readline()
while line:
    pre_element = 0
    elements = line.replace('\n', '').replace('\r', '').split('\t')
    for element in elements[:-1]:
        element = int(element)
        print(element)
        temp = element
        element = element - pre_element
        pre_element = temp
        low = element % 128
        high = element >> 7
        if high != 0:
            target.write(bytes([high+128]))
            target.write(bytes([low]))
        else:
            target.write(bytes([low+128]))
    target.write(b'\xff')
    target.write(b'\x7f')
    line = source.readline()

source.close()
target.close()
