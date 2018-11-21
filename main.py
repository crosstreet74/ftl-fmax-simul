# SSD_SIZE = 1
# PACKAGE_SIZE = 1
# DIE_SIZE = 1
PLANE_SIZE = 20  # Blocks per Plane / Total Blocks
BLOCK_SIZE = 4  # Pages per Block
MAX_BLOCK_NUM = int(PLANE_SIZE / 2)  # Maximun Block Number
TOTAL_PAGE = BLOCK_SIZE * PLANE_SIZE  # Total Pages
MAX_PAGE_NUM = int(BLOCK_SIZE * PLANE_SIZE / 2)  # Maximun Page Number


# Initialize Table Mapping Logical Block Address to Physical Block Address
def initMapper():
    global translation_table
    translation_table = [[0 for div in range(3)]
                         for num in range(MAX_BLOCK_NUM)]
    for i in range(MAX_BLOCK_NUM):
        translation_table[i][0] = i
        translation_table[i][1] = MAX_BLOCK_NUM - i - 1
        translation_table[i][2] = MAX_BLOCK_NUM + i
    print('Mapping Table Initialized\n')


def write_in_free(SSD):
    for lsn in range(MAX_PAGE_NUM):
        lbn = int(lsn / BLOCK_SIZE)
        offset = int(lsn % BLOCK_SIZE)
        pbn = translation_table[lbn][1]
        SSD[pbn][offset][0] = 1


def write_in_rep():
    # do something
    i = 0


def print_after_write():
    print(SSD)
    print()


# main
if __name__ == "__main__":

    SSD = [[[0] * 2 for j in range(BLOCK_SIZE)] for i in range(PLANE_SIZE)]

    # debug SSD information set
    print('Print SSD information')
    print('> Total Blocks\t\t: ' + str(PLANE_SIZE))
    print('> Total Pages\t\t: ' + str(TOTAL_PAGE))
    print('> Maximum Block Number\t: ' + str(MAX_BLOCK_NUM - 1))
    print('> Maximum Page Number\t: ' + str(MAX_PAGE_NUM - 1))
    print()

    initMapper()
    # # debug mapping table initialization
    # print('LBN\t|\tPBN1\t|\tPBN2\n--------------------------------------')
    # for i in range(MAX_BLOCK_NUM):
    #     temp = str(translation_table[i][0]) + '\t|\t' + str(translation_table[i][1]) + '\t|\t' + str(translation_table[i][2])
    #     print(temp+'\n')

    write_in_free(SSD)
    print_after_write()

    print('End of Program')