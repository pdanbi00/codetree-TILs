from collections import deque
from copy import deepcopy

# r, c를 왼쪽 상단으로 하는 3 * 3 배열을 시계방향으로 90도 회전시키기
def rotate(r, c, cnt): 
    result = deepcopy(board)
    for _ in range(cnt):
        tmp = result[r+0][c+2]
        result[r+0][c+2] = result[r+0][c+0]
        result[r+0][c+0] = result[r+2][c+0]
        result[r+2][c+0] = result[r+2][c+2]
        result[r+2][c+2] = tmp
        tmp = result[r+1][c+2]
        result[r+1][c+2] = result[r+0][c+1]
        result[r+0][c+1] = result[r+1][c+0]
        result[r+1][c+0] = result[r+2][c+1]
        result[r+2][c+1] = tmp
    return result

def cal_score(board):
    score = 0
    # 방문여부
    visited = [[0] * 5 for _ in range(5)]
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    for i in range(5):
        for j in range(5):
            if visited[i][j] == 0:
                q = deque([(i, j)])
                trace = deque([(i, j)])
                visited[i][j] = 1
                while q:
                    cur_r, cur_c = q.popleft()
                    for k in range(4):
                        nr, nc = cur_r + dr[k], cur_c + dc[k]
                        if 0 <= nr < 5 and 0 <= nc < 5:
                            if visited[nr][nc] == 0 and board[nr][nc] == board[cur_r][cur_c]:
                                q.append((nr, nc))
                                trace.append((nr, nc))
                                visited[nr][nc] = 1
                if len(trace) >= 3:
                    score += len(trace)
                    while trace:
                        t = trace.popleft()
                        board[t[0]][t[1]] = 0
    return score

def fill(b, queue):
    for j in range(5):
        for i in range(4, -1, -1):
            if b[i][j] == 0:
                b[i][j] = queue.popleft()
    return b


# 중심좌표를 다 돌아가면서 90도, 180도, 270도씩 돌려보면서
# (회전각도, 열, 행 순으로 입력해서 정렬해서 선택)

# 3개 이상 연결된 경우 유물이 됨. bfs로 개수 세서 3개 이상이면 ans에 추가
# 3개 이상인 것들 다시 bfs 돌면서 0으로 초기화?
# or 3개 미만인 것들 다시 bfs 돌면서 0으로 초기화

# 탐사, 유물 1차 획득, 유물 연쇄획득이 한 싸이클
# 유물 획득할 수 없다면 모든 탐사는 그 즉시 종료, 유물이 존재하지 않기 때문에 종료되는 턴에는 아무 값도 출력하면 안됨

K, M = map(int, input().split())

# 유물은 5 * 5 에 들어있음
board = [list(map(int, input().split())) for _ in range(5)]
peaces = deque(list(map(int, input().split())))

# 중심좌표를 기준으로 90도, 180도, 270도 회전 시키고
# 각각 bfs 돌면서 유물 가치 계산

# 최대 K번 탐사
for _ in range(K):
    maxScore = 0
    maxScoreBoard = None
    # 회전 목표에 맞는 결과를 maxScoreBoard에 저장
    # (1) 유물 1차 획득 가치 최대화
    # (2) 회전한 각도가 가장 작은 방법
    # (3) 회전 중심 좌표의 열이 가장 작은, 열이 같다면 행이 가장 작은 구간 선택
    for cnt in range(1, 4):
        for j in range(3):
            for i in range(3):
                rotated = rotate(i, j, cnt)
                score = cal_score(rotated)
                if maxScore < score:
                    maxScore = score
                    maxScoreBoard = rotated
    if maxScoreBoard == None:
        break
    board = maxScoreBoard
    while True:
        board = fill(board, peaces)
        newScore = cal_score(board)
        if newScore == 0:
            break
        maxScore += newScore
    print(maxScore, end = ' ')