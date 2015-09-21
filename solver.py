import sys, os, fmt
import logging
import requests
import math

cardinal = {
        'N': 0,
        'E': 1,
        'S': 2,
        'W': 3,
}

def main():
    #logging.basicConfig(level=logging.DEBUG)
    get_puzzle()
    fmt.Println(puzzle, '')
    swapXY('A', 0, 0)
    rotate_to_north('A', 1)

    finish = solve(width)
    fmt.Println('Finish')
    print_matrix(puzzle)

    transform(puzzle, finish)

    get_puzzle()

    print_matrix(puzzle)

def print_matrix(m):
    for r in m:
        fmt.Println(r)

def transform(start, finish):
    for y in xrange(width):
        for x in xrange(width):
            fin_id = finish[y][x]['id']
            if start[y][x]['id'] == fin_id:
                fmt.Println('skipping move on %s' % start[y][x]['id'])
                continue

            fmt.Println('Start:')
            print_matrix(puzzle)
            fmt.Println('Finish:')
            print_matrix(finish)

            fmt.Println("Square:", finish[y][x]['id'])
            fmt.Println('startx:', cords[fin_id]['x'], 'starty:', cords[fin_id]['y'])
            fmt.Println('loop x:', x, 'loop y:', y)
            diffx = x - cords[fin_id]['x']
            diffy = y - cords[fin_id]['y']
            fmt.Println("diff x:", diffx, "diff y:", diffy)

            updown = 'UP'
            leftright = 'RIGHT'

            if diffx < 0:
                leftright = 'LEFT'

            if diffy > 0:
                updown = 'DOWN'

            diffx = int(math.fabs(diffx))
            diffy = int(math.fabs(diffy))

            fmt.Println('leftright:', leftright)
            fmt.Println('updown:', updown)
            fmt.Println("diff x:", diffx, "diff y:", diffy)

            for x in xrange(diffx):
                move(fin_id, leftright)

            for y in xrange(diffy):
                move(fin_id, updown)

            rotate_to(start, x, y, finish[y][x]['edges'][cardinal['N']], 'N')

            get_puzzle()

def solve(n):
    final = []
    for i in xrange(n):
        final.append([])

    final[0].append(puzzle[0][0])

    for y in xrange(n):
        if y < n -1:
            final[y + 1].append(get_possible_squares(final[y][0], 'S')[0])
            rotate_to(final, 0, y + 1, final[y][0]['edges'][cardinal['S']], 'N')
        for x in xrange(n - 1):
            final[y].append(get_possible_squares(final[y][x], 'E')[0])
            print_matrix(final)
            fmt.Println("x:", x, "y:", y)
            rotate_to(final, x + 1, y, final[y][x]['edges'][cardinal['E']], 'W')
    return final

def rotate_to_north(sid, x):
    while not(puzzle[cords[sid]['x']][cords[sid]['y']]['edges'][0] == x):
        rotate(sid)

def rotate_to(grid, x, y, edge, direction):
    i = 0
    while not(grid[y][x]['edges'][cardinal[direction]] == edge) and i <=4:
        i += 1
        rotate(grid[y][x]['id'])

def get_possible_squares(s, direction):
    squares = []
    for row in puzzle:
        for square in row:
            if not(square['id'] == s['id']) and s['edges'][cardinal[direction]] in square['edges']:
                squares.append(square)
    return squares

cid = ''
puzzle = ''
cords = ''
width = 0
def get_puzzle():
    if len(sys.argv) <= 1:
        print "no args"
        sys.exit()

    global cid
    cid = sys.argv[1]

    res = requests.get("http://localhost:8080/challenges/%s/" % cid)
    fmt.Println(res.content)

    global width
    width = len(res.json()['board'][0])

    global puzzle
    puzzle = res.json()['board']

    global cords
    cords = { puzzle[x][y]['id']:{ 'x': x, 'y': y } for x in xrange(len(puzzle)) for y in xrange(len(puzzle[x]))}

def swap(first, second):
    payload = {
            'squareId1': first,
            'squareId2': second,
            }
    res = requests.post("http://localhost:8080/challenges/%s/action/swap" % cid, data=payload)
    print res.content

def swapXY(first, x2, y2):
    payload = {
            'squareId1': first,
            'x2': x2,
            'y2': y2,
            }
    requests.post("http://localhost:8080/challenges/%s/action/swap" % cid, data=payload)

def move(first, direction):
    payload = {
            'squareId1': first,
            'direction': direction,
            }
    res = requests.post("http://localhost:8080/challenges/%s/action/move" % cid, data=payload)
    print res.content

def rotate(sid):
    payload = {
            'squareId1': sid,
            }
    res = requests.post("http://localhost:8080/challenges/%s/action/rotate" % cid, data=payload)
    print res.content

def eval(cid):
    res = requests.get("http://localhost:8080/challenges/%s/evaluate" % cid)
    print res.content

if __name__ == "__main__":
    main()
