# 시뮬레이션(BFS)
from collections import deque

# 처음 아기상어 크기는 2
# 나보다 작거나 같은 물고기가 있는 칸은 지나갈 수 있음.
# 나보다 작은 물고기만 먹을 수 있음.
# 더이상 먹을 수 있는 물고기가 없으면 중단
# 먹을 수 있는 물고기가 1마리면 먹음
# 더 많으면 거리가 제일 가까운걸 먹음
# 거리가 가까운게 많으면 가장 위에 있는 물고기(r이 가장 작은), 그거도 많으면 가장 왼쪽에 있는 물고기(c가 가장 작은)
# 아기 상어는 자기 크기랑 같은 수의 물고기를 먹을 때마다 크기가 1 증가.
# 몇 초 동안 엄마한테 도움 안 요청하고 물고기 잡아먹을 수 있는가?
N = int(input())
board = []
for i in range(N):
    arr = list(map(int, input().split()))
    for j in range(N):
        if arr[j] == 9:
            s_r, s_c = i, j
            arr[j] = 0
    board.append(arr)
fish_size = 2 # 현재 물고기 크기
eat_cnt = 2 # 물고기가 지금까지 먹은 수

# 계속 bfs 돌리기
# - bfs 돌릴때마다 visited 신규로 만들기,





dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

def bfs(s_r, s_c, f_size):
    fishes = []
    visited = [[-1] * N for _ in range(N)]
    q = deque()
    q.append((s_r, s_c))
    visited[s_r][s_c] = 0
    while q:
        r, c = q.popleft()
        for k in range(4):
            nr = r + dr[k]
            nc = c + dc[k]
            if 0 <= nr < N and 0 <= nc < N:
                if visited[nr][nc] == -1 and board[nr][nc] <= f_size: # 지나갈 수 있음
                    q.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1
                    if 1 <= board[nr][nc] < f_size:
                        fishes.append((visited[nr][nc], nr, nc))
    return fishes

time = 0
while True:
    # 현재 위치에서 전체 bfs 돌면서 먹을 수 있는 물고기 담기
    fishes = bfs(s_r, s_c, fish_size)
    # 먹을 수 있는 물고기 len이 0이면 중단
    if len(fishes) == 0:
        break
    # 물고기들 distance, r, c 기준으로 정렬해서 제일 앞에꺼 먹기
    fishes.sort(key=lambda x : (x[0], x[1], x[2]))
    # 물고기 먹을 때
    time += fishes[0][0] # 이동 시간만큼 시간 추가
    eat_cnt -= 1
    # 만약 0이 되면 성장.
    if eat_cnt == 0:
        fish_size += 1
        eat_cnt = fish_size
    # 상어 위치 바꿔주기
    s_r, s_c = fishes[0][1], fishes[0][2]
    # 물고기 먹은거 표시
    board[s_r][s_c] = 0

print(time)