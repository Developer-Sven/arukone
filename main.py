import random
import pygame

def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def is_solvable(grid):
    n = len(grid)

    def check_visibility(i, j, num):
        # Überprüfe Zeile
        for col in range(n):
            if grid[i][col] == num:
                return False

        # Überprüfe Spalte
        for row in range(n):
            if grid[row][j] == num:
                return False

        # Überprüfe inneres 2x2-Quadrat
        start_row, start_col = 2 * (i // 2), 2 * (j // 2)
        for row in range(start_row, start_row + 2):
            for col in range(start_col, start_col + 2):
                if grid[row][col] == num:
                    return False

        return True

    def is_valid(i, j):
        num = grid[i][j]
        grid[i][j] = 0  # Temporär entferne die Zahl für die Überprüfung
        result = check_visibility(i, j, num)
        grid[i][j] = num  # Setze die Zahl zurück
        return result

    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0 and not is_valid(i, j):
                return False

    return True

def generate_arukone(n, num_pairs):
    grid = [[0] * n for _ in range(n)]

    for num in range(1, num_pairs + 1):
        for _ in range(2):  # Füge jedes Paar zweimal ein
            while True:
                row = random.randint(0, n - 1)
                col = random.randint(0, n - 1)
                if grid[row][col] == 0:
                    grid[row][col] = num
                    break

    while not is_solvable(grid):
        # Wenn das Arukone nicht lösbar ist, setze das Gitter zurück und versuche es erneut
        grid = [[0] * n for _ in range(n)]
        for num in range(1, num_pairs + 1):
            for _ in range(2):  # Füge jedes Paar zweimal ein
                while True:
                    row = random.randint(0, n - 1)
                    col = random.randint(0, n - 1)
                    if grid[row][col] == 0:
                        grid[row][col] = num
                        break

    return grid, num_pairs

def create_field(grid):
    rows = []
    for row in grid:
        rows.append([str(val) if val != 0 else "" for val in row])
    return rows

def main():
    while True:
        n = int(input("Gib die Größe des Gitters (n) ein: "))
        min_num_pairs = n / 2
        max_num_pairs = int(n * 0.75)
        num_pairs = random.randint(min_num_pairs, max_num_pairs)
        if n % 2 != 0:
            print("Ungültige Eingabe. Stelle sicher, dass n gerade ist und die Anzahl der Paare im gültigen Bereich liegt.")
            return
        grid, num_pairs = generate_arukone(n, num_pairs)
        print(n)
        print(num_pairs)
        print_grid(grid)

        # Pygame-Visualisierung
        pygame.init()
        WIDTH = 30
        HEIGHT = 30
        WINDOW_SIZE = (WIDTH * n, HEIGHT * n + 50)  # Zusätzlicher Platz für die Farbauswahl
        screen = pygame.display.set_mode(WINDOW_SIZE)

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        drawing_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_pairs)]
        drawing_color_index = 0
        drawing_color = drawing_colors[drawing_color_index]  # Standardfarbe
        drawing = False
        erasing = False
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linker Mausklick
                        drawing = True
                        erasing = False
                    elif event.button == 3:  # Rechter Mausklick
                        drawing = False
                        erasing = True
                elif event.type == pygame.MOUSEMOTION and (drawing or erasing):
                    x, y = event.pos
                    row = y // HEIGHT
                    col = x // WIDTH
                    if 0 <= row < n and 0 <= col < n:
                        if erasing:
                            grid[row][col] = 0
                        elif grid[row][col] == 0:
                            grid[row][col] = "X" if drawing_color == drawing_colors[0] else "O"  # "X" für Linie, "O" für Löschvorgang

                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    erasing = False

            screen.fill(WHITE)

            field = create_field(grid)

            for i, row in enumerate(field):
                for j, value in enumerate(row):
                    pygame.draw.rect(screen, BLACK, (j * WIDTH, i * HEIGHT, WIDTH, HEIGHT), 1)
                    if value == "X":
                        pygame.draw.line(screen, drawing_color, (j * WIDTH, i * HEIGHT), ((j + 1) * WIDTH, (i + 1) * HEIGHT), 2)
                        pygame.draw.line(screen, drawing_color, ((j + 1) * WIDTH, i * HEIGHT), (j * WIDTH, (i + 1) * HEIGHT), 2)
                    elif value == "O":
                        pygame.draw.rect(screen, WHITE, (j * WIDTH, i * HEIGHT, WIDTH, HEIGHT))
                    elif value != "":
                        font = pygame.font.Font(None, 36)
                        text = font.render(value, True, BLACK)
                        text_rect = text.get_rect(center=(j * WIDTH + WIDTH // 2, i * HEIGHT + HEIGHT // 2))
                        screen.blit(text, text_rect)

            # Farbauswahl am unteren Rand
            for idx, color in enumerate(drawing_colors):
                pygame.draw.rect(screen, color, (idx * WIDTH, HEIGHT * n, WIDTH, 50))

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    main()