import npyscreen

# SSD_SIZE = 1
# PACKAGE_SIZE = 1
# DIE_SIZE = 1
PLANE_SIZE = 20  # Blocks per Plane / Total Blocks
BLOCK_SIZE = 4  # Pages per Block
MAX_BLOCK_NUM = int(PLANE_SIZE / 2)  # Maximun Block Number
TOTAL_PAGE = BLOCK_SIZE * PLANE_SIZE  # Total Pages
MAX_PAGE_NUM = int(BLOCK_SIZE * PLANE_SIZE / 2)  # Maximun Page Number

class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = npyscreen.Form(name = "SSD simulator: ftl-fmax-simul",)
        ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Tester",
                values = ["Run Test"], scroll_exit=True)
        F.edit()
        
        if ms.value is "Run Test":
            SSD = [[[0] * 2 for j in range(BLOCK_SIZE)] for i in range(PLANE_SIZE)]

            print('Initialized SSD')
            print_after_write(SSD)

            # debug SSD information set
            print('Print SSD information')
            print('> Total Blocks\t\t: ' + str(PLANE_SIZE))
            print('> Total Pages\t\t: ' + str(TOTAL_PAGE))
            print('> Maximum Block Number\t: ' + str(MAX_BLOCK_NUM - 1))
            print('> Maximum Page Number\t: ' + str(MAX_PAGE_NUM - 1))
            print()

            initMapper()

            # debug mapping table initialization
            print('LBN\t|\tPBN1\t|\tPBN2\n--------------------------------------')
            for i in range(MAX_BLOCK_NUM):
                temp = str(translation_table[i][0]) + '\t|\t' + str(
                    translation_table[i][1]) + '\t|\t' + str(translation_table[i][2])
                print(temp)
            print()

            print('Write to All Logical Page Numbers')
            write_in_free(SSD)
            print_after_write(SSD)

            print('Try to Overwrite to All Logical Page Numbers')
            write_in_free(SSD)
            print_after_write(SSD)

            print('Try to Overwrite to Full Replacement Block')
            write_in_free(SSD)
            print_after_write(SSD)

            print()
            input('End of Program: Press Any Key to Close ')

# Initialize Table Mapping Logical Block Address to Physical Block Address
def initMapper():
    global translation_table
    translation_table = [[0 for div in range(3)]
                         for num in range(MAX_BLOCK_NUM)]
    for i in range(MAX_BLOCK_NUM):
        translation_table[i][0] = i
        translation_table[i][1] = MAX_BLOCK_NUM - i - 1
        translation_table[i][2] = MAX_BLOCK_NUM + i
    print('Initialized Mapping Table')


# Write to all available Logical Sector(Page) Number
def write_in_free(SSD):
    for lsn in range(MAX_PAGE_NUM):
        lbn = int(lsn / BLOCK_SIZE)  # Logical Block Number
        offset = int(lsn % BLOCK_SIZE)
        pbn = translation_table[lbn][1]

        # If page already written
        if SSD[pbn][offset][0] is 1:
            write_in_rep(SSD, lsn)
        # If not
        else:
            SSD[pbn][offset][0] = 1


# Write to all available Logical Sector(Page) Number
def write_in_rep(SSD, lsn):
    lbn = int(lsn / BLOCK_SIZE)
    offset = int(lsn % BLOCK_SIZE)
    pbn = translation_table[lbn][1]
    rep_pbn = translation_table[lbn][2]

    SSD[pbn][offset][1] = 1
    for i in range(BLOCK_SIZE):
        if SSD[rep_pbn][i][0] is 0:
            SSD[rep_pbn][i][0] = 1
            SSD[rep_pbn][i][1] = lsn
            break

        if i is BLOCK_SIZE - 1:
            block_transfer(lsn)

    # SSD[rep_pbn][offset][0] = 1
    # SSD[rep_pbn][offset][1] = lsn


# Print all data of SSD
def print_after_write(SSD):
    print(hex(id(SSD)))
    print(hex(id(SSD[0])))
    print(hex(id(SSD[0][0])))
    print(hex(id(SSD[1][0][0])))
    print(SSD)
    print()


def block_transfer(lsn):
    lbn = int(lsn / BLOCK_SIZE)
    offset = int(lsn % BLOCK_SIZE)
    pbn = translation_table[lbn][1]
    rep_pbn = translation_table[lbn][2]
    # buffer = [[0 for area in range(4)] for p in range(BLOCK_SIZE)]
    # j = 0

    # for p in range(BLOCK_SIZE):
    #     i = BLOCK_SIZE - p - 1
    #     buf_lsn = SSD[rep_pbn][i][1]
    #     buf_data = SSD[rep_pbn][i][1]
    #     if buf_lsn is not 0:
    #         buffer[i][j] = buf_lsn
    #         j += 1


# main
if __name__ == "__main__":
    App = TestApp()
    App.run()