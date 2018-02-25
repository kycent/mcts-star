"mcts for pop star"

class Block(object):
    def __init__(self):
        self.color = 0
        self.members = []

#definition for game class
class Game(object):
    def __init__(self):
        self.map = None
        self.score = 0

    def __find_point_in_blocks(self, blocks, x, y):
        for block in blocks:
            for p in block.members:
                if p[0] == x and p[1] == y:
                    return block
        return None

    def __merge_blocks(self, block1, block2):
        if block1.color != block2.color:
            raise  Exception("two blocks' color is not same")
        block1.members.extend(block2.members)
        return block1

    #get available moves(blocks)
    #each block is a list of coordinates
    def getAvailableBlocks(self):
        blocks = []
        for x in xrange(len(self.map)):
            for y in xrange(len(self.map[x])):
                if None != self.__find_point_in_blocks(blocks, x, y):
                    continue
                if self.map[x][y] is None:
                    continue
                #has up neiboughs?
                upBlock = None
                leftBlock = None
                if x >= 1:
                    upBlock = self.__find_point_in_blocks(blocks, x-1, y)
                    upBlock = upBlock if  upBlock is not None and upBlock.color == self.map[x][y] else None
                if y >= 1:
                    leftBlock = self.__find_point_in_blocks(blocks, x, y-1)
                    leftBlock = leftBlock if leftBlock is not None and leftBlock.color == self.map[x][y] else None

                #if one of these is None, then extend the other block
                if upBlock is None and leftBlock is not None:
                    leftBlock.members.append((x,y))
                elif leftBlock is None and upBlock is not None:
                    upBlock.members.append((x,y))
                elif leftBlock is not None and upBlock is not None and leftBlock is upBlock:
                    leftBlock.members.append((x,y))
                elif leftBlock is not None and upBlock is not None and leftBlock is not upBlock:
                    #need to merge the 2 blocks
                    sumblock = self.__merge_blocks(leftBlock, upBlock)
                    leftBlock.members.append((x,y))
                    #need to remove the upBlock in blocks list
                    for b in blocks:
                        if b is upBlock:
                            blocks.remove(b)
                else:
                    newBlock = Block()
                    newBlock.color = self.map[x][y]
                    newBlock.members.append((x,y))
                    blocks.append(newBlock)

        for b in blocks:
            if len(b.members) <= 1:
                blocks.remove(b)
        return blocks

    def removeBlock(self, block):
        #replace the color with None
        if len(block.members) <= 1:
            return
        cols = {}
        for x, y in block.members:
            if y not in cols:
                items = []
                items.append(x)
                cols[y] = items
            else:
                cols[y].append(x)
            self.map[x][y] = None

        # assign the None to above
        for y in cols:
            for x in xrange(len(self.map)):
                xx = len(self.map) - 1 - x
                if self.map[xx][y] is None:
                    topPosition = 0
                    while topPosition < xx:
                        if self.map[topPosition][y] is not None:
                            break
                        topPosition = topPosition + 1
                    if topPosition < xx:
                        #swap the two items
                        temp = self.map[xx][y]
                        self.map[xx][y] = self.map[topPosition][y]
                        self.map[topPosition][y] = temp

            #check the blank cols
            if len(cols[y]) == len(self.map):
                yMax = len(self.map[0])
                xMax = len(self.map)
                if y == yMax - 1:
                    continue
                else:
                    yy = y + 1
                    while yy < yMax:
                        for xx in xrange(xMax):
                            self.map[xx][yy - 1] == self.map[xx][yy]
                    #fill the last col as None
                    for xx in xrange(xMax):
                        self.map[xx][yMax - 1] = None

    def getScore(self, block):
        if len(block.members) <= 1:
            return 0
        else:
            num = len(block.members)
            return num * num * 5

    def printMap(self):
        for row in self.map:
            printrow = [ item if item is not None else "N" for item in row]
            print repr(printrow)

    def getLeftItemNumber(self):
        num = 0
        for row in self.map:
            for item in row:
                if item is not None:
                    num = num + 1
        return num

    def getBonusScore(self):
        scoreMap = {
            0 : 2000,
            1 : 1980,
            2:  1920,
            3:  1820,
            4:  1680,
            5:  1500,
            6:  1280,
            7:  1020,
            8:  720,
            9:  380,
            10: 0
        }
        num = self.getLeftItemNumber()
        if num  < 10:
            return scoreMap[num]
        else:
            return 0

if __name__ == "__main__":
    game = Game()
    game.map = [
        [0, 0, 1, 0, 2],
        [0, 1, 1, 1, 0],
        [0, 1, 2, 1, 0],
        [1, 1, 1, 4, 1],
        [3, 1, 0, 1, 5],
    ]
    blocks = game.getAvailableBlocks()
    for b in blocks:
        if len(b.members) > 4:
            print "remove block %s" %(repr(b.members))
            game.removeBlock(b)
        print "block: %s" %(repr(b.members))
    game.printMap()