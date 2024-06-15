from collections import deque
MAX_L = 70

R, C, K = map(int, input().split())
A = [[0] * MAX_L for _ in range(MAX_L+3)] # 골렘이 끝까지 못내려오는 경우도 있으니깐, 실제 숲을 3행부터라고 생각

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
isExit = [[False] * MAX_L for _ in range(MAX_L + 3)] # 해당 칸이 골렘의 출구인지 저장
answer = 0 # 각 정령들이 도달할 수 있는 최하단 행의 합

# (r, c)가 숲의 범위 안에 있는지 확인
def inRange(r, c):
    return 3 <= r < R + 3 and 0 <= c < C

# 숲에 있는 골렘들 다 빠져나가기
def resetMap():
    for i in range(R+3):
        for j in range(C):
            A[i][j] = 0
            isExit[i][j] = False

# 골렘 중심이 r, c에 위치할 수 있는지 확인
# 북쪽에서 남쪽으로 내려와야하기 때문에 중심이 (r, c)에 위치할 때의 범위랑, (r-1, c)에 위치할 때의 범위 모두 확인
def canGo(r, c):
    flag = 0 <= c - 1 and c + 1 < C and r+1 < R+3
    flag = flag and (A[r-1][c-1] == 0)
    flag = flag and (A[r-1][c] == 0)
    flag = flag and (A[r-1][c+1] == 0)
    flag = flag and (A[r][c-1] == 0)
    flag = flag and (A[r][c] == 0)
    flag = flag and (A[r][c+1] == 0)
    flag = flag and (A[r+1][c] == 0)
    return flag

# 정령이 움직일 수 있는 모든 범위 확인하고, 도달할 수 있는 최하단 행 반환
def bfs(r, c):
    result = r
    q = deque([(r, c)])
    visited = [[False] * C for _ in range(R+3)]
    visited[r][c] = True
    while q:
        cur_r, cur_c = q.popleft()
        for k in range(4):
            nr = cur_r + dr[k]
            nc = cur_c + dc[k]
            if inRange(nr, nc) and not visited[nr][nc] and (A[nr][nc] == A[cur_r][cur_c] or (A[nr][nc] != 0 and isExit[cur_r][cur_c])):
                q.append((nr, nc))
                visited[nr][nc] = True
                result = max(result, nr)
    return result


# 골렘id가 중심(r, c), 출구방향이 d일 때 규칙에 따라서 움직임을 취하는 함수
def move(r, c, d, id):
    if canGo(r+1, c):
        # 아래로 내려갈 수 있으면
        move(r+1, c, d, id)
    elif canGo(r+1, c-1):
        # 왼쪽 아래로 내려갈 수 있으면
        move(r+1, c-1, (d+3) % 4 , id)
    elif canGo(r+1, c+1):
        # 오른쪽 아래로 내려갈 수 있으면
        move(r+1, c+1, (d+1) % 4, id)
    else:
        if not inRange(r-1, c-1) or not inRange(r+1, c+1):
            resetMap()
        else:
            # 골렘이 숲에 정착
            A[r][c] = id
            for k in range(4):
                A[r + dr[k]][c + dc[k]] = id
            # 골렘 출구 기록
            isExit[r+dr[d]][c+dc[d]] = True
            global answer
            # bfs로 정령이 최대로 내려갈 수 있는 행 구해서 누적
            answer += bfs(r, c) - 3 + 1

for id in range(1, K+1): # 골렘 번호 : id
    c, d = map(int, input().split())
    move(0, c-1, d, id)
print(answer)