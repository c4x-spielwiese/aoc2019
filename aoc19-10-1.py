import sys, math, copy
from fractions import gcd

def initField(strInput):
    m = []
    y = 0
    for line in strInput.split("\n"):
        line = line.strip()
        m.append([])
        for x in range(0, len(line)):
            m[y].append(0 if line[x : x+1] == '.' else 1)
        y += 1
    return m

def printField(m):
    print('-'*len(m)*3)
    for y in range(0, len(m)):
        for x in range(0, len(m[0])):        
            if m[y][x] == 1:
                sys.stdout.write('#')
            elif m[y][x] == 7:
                sys.stdout.write('X')
            elif m[y][x] == 3:
                sys.stdout.write('o')
            elif m[y][x] == 8:
                sys.stdout.write('.')
            elif m[y][x] == 2:
                sys.stdout.write('*')
            elif m[y][x] > 1:
                sys.stdout.write(str(m[y][x]))
            else:
                sys.stdout.write(' ')
            sys.stdout.write('  ')
        sys.stdout.write('\n')
    print('-'*len(m)*3)

def hideAsteroids(field, startX, startY, x, y):
    dX = x - startX
    dY = y - startY
    
    d = gcd(abs(dX), abs(dY)) 
    dX = int(dX / d)
    dY = int(dY / d)

    i = 1
    while True:
        x += dX
        y += dY
        if len(field) > y and len(field[0]) > x and y >= 0 and x >= 0:
            field[y][x] = 8
        if y < 0 or x < 0 or y > len(field) or x > len(field[0]):
            return
        i += 1

def checkAsteroid(field, startX, startY, x, y):
    if len(field) <= y or len(field[y]) <= x or y < 0 or x < 0:
        return

    if field[y][x] == 1:    # found an asteroid
        field[y][x] = 2
        hideAsteroids(field, startX, startY, x, y)
    elif field[y][x] == 0:
        field[y][x] = 3

def countAsteroids(field, startX, startY):     
    x = startX
    y = startY
    d = 1
    assert field[y][x] == 1, "no asteroid at %i %i" % (startX, startY)
    field[y][x] = 7
        
    while d < len(field) * 2:  # cycle around the start XY
        x += 1                                  # 1 right
        checkAsteroid(field, startX, startY, x, y)      
        for _ in range(1, d+1):                 # down
            y += 1
            checkAsteroid(field, startX, startY, x, y)
        d += 1
        for _ in range(1, d+1):                 # left
            x -= 1
            checkAsteroid(field, startX, startY, x, y)
        for _ in range(1, d+1):                 # up
            y -= 1
            checkAsteroid(field, startX, startY, x, y)
        for _ in range(1, d+1):                 # right
            x += 1
            checkAsteroid(field, startX, startY, x, y)
        d += 1
    
    res = 0
    for y in range(0, len(field)):
        for x in range (0, len(field[0])):
            if field[y][x] == 2:
                res += 1
    return res

def findBestPosition(field):
    maxC = -1
    maxX = -1
    maxY = -1
    for y in range(0, len(field)):
        for x in range(0, len(field[0])):
            if field[y][x] == 1:
                res = countAsteroids(copy.deepcopy(field), x, y)
                if res > maxC:
                    maxC = res
                    maxX = x
                    maxY = y
    return {'c': maxC, 'x': maxX, 'y': maxY} 
       
if len(sys.argv) > 1 and sys.argv[1] == "test":
    print("test mode:")
    tests = [                
                 """.#..#
                    .....
                    #####
                    ....#
                    ...##""", 3, 4, 8,
                 """..........
                    ..........
                    ..........
                    ...#.#....
                    ..#...#...
                    ....#.....
                    ..#...#...
                    ...#.#....
                    ..........
                    ..........""", 4, 5, 8,
                 """#...........
                    ............
                    ............
                    ............
                    ............
                    ............
                    ............
                    ............
                    ......#.....
                    ............
                    ............
                    ............
                    .........#..""", 0, 0, 1,                    
                 """...........
                    ...........
                    ...........
                    ...#.#.#...
                    ....###....
                    ...#####...
                    ....###....
                    ...#.#.#...
                    ...........
                    ...........
                    ...........""", 5, 5, 8,                    
                 """......#.#.
                    #..#.#....
                    ..#######.
                    .#.#.###..
                    .#..#.....
                    ..#....#.#
                    #..#....#.
                    .##.#..###
                    ##...#..#.
                    .#....####""", 5, 8, 33,
                 """.#..#..###
                    ####.###.#
                    ....###.#.
                    ..###.##.#
                    ##.##.#.#.
                    ....###..#
                    ..#.#..#.#
                    #..#.#.###
                    .##...##.#
                    .....#.#..""", 6,3, 41,
                 """#.#...#.#.
                    .###....#.
                    .#....#...
                    ##.#.#.#.#
                    ....#.#.#.
                    .##..###.#
                    ..#...##..
                    ..##....##
                    ......#...
                    .####.###.""", 1, 2, 35,
                 """.#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##""", 11, 13, 210
            ]
    i = 0
    if len(sys.argv) > 2:
        testNum = 4 * int(sys.argv[2])
        tests = [tests[testNum], tests[testNum+1], tests[testNum+2], tests[testNum+3]]
    while i < len(tests):
        field1 = initField(tests[i])
        field2 = copy.deepcopy(field1)
        printField(field1)
        res = countAsteroids(field1, tests[i+1], tests[i+2])
        printField(field1)
        bestPos = findBestPosition(field2)
        print("asteroids count=%i, bestPos=%s, test=%s, targetCount=%i" % (res, bestPos, "OK" if res == tests[i+3] and bestPos['x'] == tests[i+1] and bestPos['y'] == tests[i+2] else "ERR!", tests[i+3]))        
        i += 4

else:
    with open(__file__.replace('.py', '.input.txt'), 'r') as f:
        contents = f.read()
        field = initField(contents)
        printField(field)
        print(findBestPosition(field))