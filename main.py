# SSD_SIZE = 1
# PACKAGE_SIZE = 1
# DIE_SIZE = 1
PLANE_SIZE = 20
BLOCK_SIZE = 4
MAX_BLOCK = int(PLANE_SIZE / 2)
flash_memory = [[0 for div in range(2)] for num in range(PLANE_SIZE)]
PAGE = [0 for area in range(2)]
BLOCK = [PAGE for size in range(BLOCK_SIZE)]
SSD = [BLOCK for size in range(PLANE_SIZE)]


# Initialize Table Mapping Logical Block Address to Physical Block Address
def initMapper():
    global translation_table
    translation_table = [[0 for div in range(3)] for num in range(MAX_BLOCK)]
    for i in range(MAX_BLOCK):
        translation_table[i][0] = i
        translation_table[i][1] = MAX_BLOCK - i - 1
        translation_table[i][2] = MAX_BLOCK + i
    print('Mapping Table Initialized\n')


# main
if __name__ == "__main__":
    initMapper()

    # debug mapping table initialization
    print('LBN\t|\tPBN1\t|\tPBN2\n--------------------------------------')
    for i in range(MAX_BLOCK):
        temp = str(translation_table[i][0]) + '\t|\t' + str(translation_table[i][1]) + '\t|\t' + str(translation_table[i][2])
        print(temp)