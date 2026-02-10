class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0


def parse_row(line, n):
    """
    ورودی هر سطر را هم به شکل با فاصله (0 1 0 0)
    و هم بدون فاصله (0100) می‌پذیرد.
    """
    line = line.strip()

    # حالت بدون فاصله: مثل 0101
    if " " not in line:
        if len(line) != n or any(ch not in "01" for ch in line):
            return None
        return [int(ch) for ch in line]

    # حالت با فاصله: مثل 0 1 0 1
    parts = line.split() #تبدیل له لیست
    if len(parts) != n or any(p not in ("0", "1") for p in parts):
        return None
    return [int(p) for p in parts]


def read_maze():
    while True:
        try:
            n = int(input("Andaze matris ra vared konid(methal n=4) : "))
            if n <= 0:
                print("Andaze bayad  mothbat bashad!\n")
                continue
            break
        except ValueError:
            print("Lotfan yek adad sahih vared konid\n")

    print(f"\nحالا {n} خط وارد کنید. هر خط باید دقیقاً {n} مقدار 0/1 باشد.")
    print("می‌تواند با فاصله باشد:")
    print("0 0 1 0")
    print("یا بدون فاصله:")
    print("0010\n")

    maze = []
    for i in range(n):  #satr be satr 
        while True:
            line = input(f"خط {i+1}: ")
            row = parse_row(line, n)
            if row is None:
                print(f"ورودی اشتباه! باید دقیقاً {n} عدد 0/1 باشد. دوباره وارد کنید.")
                continue
            maze.append(row)
            break

    return maze


def solve_maze(maze):
    n = len(maze)

    # اگر شروع یا پایان دیوار باشد
    if maze[0][0] == 1 or maze[n - 1][n - 1] == 1:
        return None

    # بالا، پایین، چپ، راست
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #حرکت قطری مجاز نیست

    visited = [[False] * n for _ in range(n)]
    came_from = {}  # برای بازسازی مسیر
    stack = Stack()

    stack.push((0, 0))  #نقطه شروع
    visited[0][0] = True

    while not stack.is_empty():
        x, y = stack.pop()

        if (x, y) == (n - 1, n - 1):
            # مسیر پیدا شد -> بازسازی
            path = []
            cur = (x, y)
            while True:
                path.append(cur)
                if cur == (0, 0):
                    break
                cur = came_from[cur]
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if maze[nx][ny] == 0 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    came_from[(nx, ny)] = (x, y)
                    stack.push((nx, ny))

    return None  # مسیر پیدا نشد


def print_maze(maze):
    print("\nماتریس وارد شده:")
    for row in maze:
        print(" ".join(map(str, row)))


def print_path(path):
    print("\nPath Found:")
    print(" → ".join(f"({r},{c})" for r, c in path))


def print_maze_with_path(maze, path):
    n = len(maze)
    path_set = set(path)  #path into set bc of speed 

    print("\nنمایش Maze نهایی:")
    print("راهنما: S=Start ، E=Exit ، #=Wall(1) ، *=Path ، .=Free(0)\n")

    for i in range(n):
        line = []
        for j in range(n):
            if (i, j) == (0, 0):
                line.append("S")
            elif (i, j) == (n - 1, n - 1):
                line.append("E")
            elif maze[i][j] == 1:
                line.append("#")
            elif (i, j) in path_set:
                line.append("*")
            else:
                line.append(".")
        print(" ".join(line))



print("حل‌کننده Maze با Stack\n")

maze = read_maze()
print_maze(maze)

path = solve_maze(maze)

if path is None:
    print("\nهیچ مسیری از (0,0) به (n-1,n-1) پیدا نشد :(")
else:
    print_path(path)
    print_maze_with_path(maze, path)