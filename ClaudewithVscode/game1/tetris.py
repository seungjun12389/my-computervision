"""간단한 테트리스 게임 (tkinter, 표준 라이브러리만 사용)

실행: python tetris.py
조작: ←/→ 이동, ↓ 소프트드롭, ↑ 회전, Space 하드드롭, P 일시정지, R 재시작
"""

import random
import tkinter as tk

COLS, ROWS = 10, 20
CELL = 30
MARGIN = 20
SIDEBAR = 150

# 각 블록의 회전 상태들을 (x, y) 좌표 목록으로 정의
SHAPES = {
    "I": [[(0, 1), (1, 1), (2, 1), (3, 1)],
          [(2, 0), (2, 1), (2, 2), (2, 3)]],
    "O": [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    "T": [[(1, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)],
          [(1, 0), (0, 1), (1, 1), (1, 2)]],
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)],
          [(1, 0), (1, 1), (2, 1), (2, 2)]],
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)],
          [(2, 0), (1, 1), (2, 1), (1, 2)]],
    "J": [[(0, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)],
          [(1, 0), (1, 1), (0, 2), (1, 2)]],
    "L": [[(2, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (1, 2), (2, 2)],
          [(0, 1), (1, 1), (2, 1), (0, 2)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
}

COLORS = {
    "I": "#00f0f0", "O": "#f0f000", "T": "#a000f0", "S": "#00f000",
    "Z": "#f00000", "J": "#0000f0", "L": "#f0a000",
}


class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.rot = 0
        self.x = COLS // 2 - 2
        self.y = 0

    @property
    def cells(self):
        """현재 회전 상태의 블록 칸들을 보드 좌표로 반환"""
        shape = SHAPES[self.kind][self.rot]
        return [(self.x + cx, self.y + cy) for cx, cy in shape]

    def rotated_cells(self):
        shape = SHAPES[self.kind][(self.rot + 1) % len(SHAPES[self.kind])]
        return [(self.x + cx, self.y + cy) for cx, cy in shape]


class Tetris:
    def __init__(self, root):
        self.root = root
        root.title("테트리스")
        root.resizable(False, False)

        width = COLS * CELL + MARGIN * 2 + SIDEBAR
        height = ROWS * CELL + MARGIN * 2
        self.canvas = tk.Canvas(root, width=width, height=height,
                                bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()

        root.bind("<Key>", self.on_key)
        self.timer = None
        self.reset()

    def reset(self):
        if self.timer is not None:  # 재시작 시 이전 타이머가 남아 두 배로 빨라지는 것 방지
            self.root.after_cancel(self.timer)
            self.timer = None
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.bag = []
        self.piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.over = False
        self.tick()

    def new_piece(self):
        # 7-bag 방식: 7종류를 한 번씩 섞어서 배출
        if not self.bag:
            self.bag = list(SHAPES)
            random.shuffle(self.bag)
        return Piece(self.bag.pop())

    # --- 게임 로직 ---

    def valid(self, cells):
        for x, y in cells:
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def move(self, dx, dy):
        moved = [(x + dx, y + dy) for x, y in self.piece.cells]
        if self.valid(moved):
            self.piece.x += dx
            self.piece.y += dy
            return True
        return False

    def rotate(self):
        cells = self.piece.rotated_cells()
        # 벽이나 블록에 막히면 옆으로 살짝 밀어서 회전 시도
        for kick in (0, -1, 1, -2, 2):
            if self.valid([(x + kick, y) for x, y in cells]):
                self.piece.rot = (self.piece.rot + 1) % len(SHAPES[self.piece.kind])
                self.piece.x += kick
                return

    def hard_drop(self):
        while self.move(0, 1):
            self.score += 2
        self.lock()

    def lock(self):
        for x, y in self.piece.cells:
            if y < 0:
                self.over = True
                return
            self.board[y][x] = self.piece.kind
        self.clear_lines()
        self.piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid(self.piece.cells):
            self.over = True

    def clear_lines(self):
        kept = [row for row in self.board if not all(row)]
        cleared = ROWS - len(kept)
        if cleared:
            self.board = [[None] * COLS for _ in range(cleared)] + kept
            self.lines += cleared
            self.score += (0, 100, 300, 500, 800)[cleared] * self.level
            self.level = self.lines // 10 + 1

    def tick(self):
        if not self.paused and not self.over:
            if not self.move(0, 1):
                self.lock()
        self.draw()
        if not self.over:
            delay = max(80, 500 - (self.level - 1) * 40)
            self.timer = self.root.after(delay, self.tick)

    # --- 입력 ---

    def on_key(self, event):
        key = event.keysym.lower()
        if key == "r":
            self.reset()
            return
        if self.over:
            return
        if key == "p":
            self.paused = not self.paused
            self.draw()
            return
        if self.paused:
            return

        if key == "left":
            self.move(-1, 0)
        elif key == "right":
            self.move(1, 0)
        elif key == "down":
            if self.move(0, 1):
                self.score += 1
        elif key == "up":
            self.rotate()
        elif key == "space":
            self.hard_drop()
        self.draw()

    # --- 그리기 ---

    def cell_rect(self, col, row, color, ox=MARGIN, oy=MARGIN):
        x, y = ox + col * CELL, oy + row * CELL
        self.canvas.create_rectangle(x, y, x + CELL, y + CELL,
                                     fill=color, outline="#1a1a1a", width=2)

    def draw(self):
        self.canvas.delete("all")
        bx, by = MARGIN, MARGIN

        self.canvas.create_rectangle(bx, by, bx + COLS * CELL, by + ROWS * CELL,
                                     fill="#101010", outline="#444")
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c]:
                    self.cell_rect(c, r, COLORS[self.board[r][c]])

        if not self.over:
            color = COLORS[self.piece.kind]
            # 고스트: 블록이 떨어질 위치 미리보기
            ghost = 0
            while self.valid([(x, y + ghost + 1) for x, y in self.piece.cells]):
                ghost += 1
            for x, y in self.piece.cells:
                if y + ghost >= 0:
                    self.canvas.create_rectangle(
                        bx + x * CELL, by + (y + ghost) * CELL,
                        bx + (x + 1) * CELL, by + (y + ghost + 1) * CELL,
                        outline=color, width=1)
            for x, y in self.piece.cells:
                if y >= 0:
                    self.cell_rect(x, y, color)

        # 사이드바
        sx = bx + COLS * CELL + 20
        self.canvas.create_text(sx, by, anchor="nw", fill="white",
                                font=("Consolas", 12, "bold"), text="NEXT")
        for cx, cy in SHAPES[self.next_piece.kind][0]:
            self.cell_rect(cx, cy, COLORS[self.next_piece.kind], ox=sx, oy=by + 25)

        info = "SCORE\n{}\n\nLINES\n{}\n\nLEVEL\n{}".format(
            self.score, self.lines, self.level)
        self.canvas.create_text(sx, by + 160, anchor="nw", fill="white",
                                font=("Consolas", 11), text=info)
        self.canvas.create_text(sx, by + 330, anchor="nw", fill="#888",
                                font=("Consolas", 8),
                                text="←→ 이동\n↓ 내리기\n↑ 회전\nSpace 드롭\nP 일시정지\nR 재시작")

        if self.paused:
            self.overlay("PAUSED")
        elif self.over:
            self.overlay("GAME OVER", "R 키로 재시작")

    def overlay(self, text, sub=None):
        cx = MARGIN + COLS * CELL // 2
        cy = MARGIN + ROWS * CELL // 2
        self.canvas.create_rectangle(MARGIN, cy - 45, MARGIN + COLS * CELL, cy + 45,
                                     fill="#000", outline="")
        self.canvas.create_text(cx, cy - 10, fill="white",
                                font=("Consolas", 20, "bold"), text=text)
        if sub:
            self.canvas.create_text(cx, cy + 20, fill="#aaa",
                                    font=("Consolas", 10), text=sub)


if __name__ == "__main__":
    root = tk.Tk()
    Tetris(root)
    root.mainloop()
