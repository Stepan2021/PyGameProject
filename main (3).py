import pygame

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
BLUE = (0, 0, 155)

block_size = 40
left_margin = 50
upper_margin = 80

size = (1250, 680)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Морской Бой")

font_size = int(block_size / 1.5)

font = pygame.font.SysFont('notosans', font_size)
dotted_set = set()
crosses_set = set()
all_clicks = []
ships_coordinates_player_one = []
ships_coordinates_player_two = []
destroyed_ships = []
player = True

def draw_grid():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i in range(11):
        pygame.draw.line(screen, BLACK, (left_margin, upper_margin + i * block_size),
                         (left_margin + 10 * block_size, upper_margin + i * block_size), 1)
        pygame.draw.line(screen, BLACK, (left_margin + i * block_size, upper_margin),
                         (left_margin + i * block_size, upper_margin + 10 * block_size), 1)
        pygame.draw.line(screen, BLACK, (left_margin + 15 * block_size, upper_margin +
                                         i * block_size), (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
        pygame.draw.line(screen, BLACK, (left_margin + (i + 15) * block_size, upper_margin),
                         (left_margin + (i + 15) * block_size, upper_margin + 10 * block_size), 1)

        if i < 10:
            num_ver = font.render(str(i + 1), True, BLACK)
            letters_hor = font.render(letters[i], True, BLACK)

            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2),
                                  upper_margin + i * block_size + (block_size // 2 - num_ver_height//2)))
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 - letters_hor_width//2),
                                      upper_margin + 10 * block_size))
            screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2) + 15 *
                                  block_size, upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 - letters_hor_width // 2)
                                      + 15 * block_size, upper_margin + 10 * block_size))




class Build_ships():
    def __init__(self):
        self.board = [[1] * 10 for _ in range(10)]

    def build_grid(self):
        for x in range(10):
            for y in range(10):
                pygame.draw.rect(screen, BLACK, (410 + block_size * x, 100 + block_size * y, block_size, block_size), self.board[y][x])

    def get_coordinates(self, ships_coordinates):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if (425 <= mouse[0] <= (410 + block_size * 10)) and (80 <= mouse[1] <= (100 + block_size * 10)) and click == True:
            x, y = ((mouse[0] - 410) // block_size), ((mouse[1] - 100) // block_size)
            if (x, y) not in ships_coordinates:
                pygame.draw.rect(screen, BLUE,
                                 (411 + x * block_size, 101 + y * block_size, block_size - 2, block_size - 2))
                pygame.display.update()
                ships_coordinates.append((x, y))
            else:
                ships_coordinates.remove((x, y))
                pygame.draw.rect(screen, WHITE,
                                 (411 + x * block_size, 101 + y * block_size, block_size - 2, block_size - 2))
                pygame.display.update()


class Button():
    def __init__(self, weight, height, font_size=30, color_active=(), color_inactive=()):
        self.weight = weight
        self.height = height
        self.inactive_color = color_inactive
        self.active_color = color_active
        self.font_size = font_size

    def draw_button(self, x, y, massage):
        mouse = pygame.mouse.get_pos()
        if (x < mouse[0] < x + self.weight):
            if (y < mouse[1] < y + self.height):
                    pygame.draw.rect(screen, self.active_color, (x, y, self.weight, self.height))
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.weight, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.weight, self.height))
        self.text_on_button(massage, x + 10, y + 10)

    def text_on_button(self, massage, x, y, font_color=(0, 0, 0), font_type='georgia'):
        f = pygame.font.SysFont(font_type, self.font_size)
        text = f.render(massage, True, font_color)
        screen.blit(text, (x, y))


def fight_coordinates():
    global player
    mouse_position = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    fired_block = ((mouse_position[0] - left_margin + 1 * block_size) // block_size, (mouse_position[1] - upper_margin  + 1 * block_size) // block_size)
    if player:
        if ((left_margin + 15 * block_size) <= mouse_position[0] <= (left_margin + 25 * block_size)) and (upper_margin <= mouse_position[1] <= upper_margin + block_size * 10):
            if click:
                if ((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size) not in all_clicks:
                    all_clicks.append(((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size))
                    # проверяется попал ли игрок в корабль, если попал то крестик, нет точка
                    if ((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size) in ships_coordinates_player_two:
                        put_cross_on_hitted_block(fired_block)
                        ships_coordinates_player_two.remove(((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size))
                        if len(ships_coordinates_player_two) == 0:
                            draw_end_screen(player=True)                        
                    else:
                        put_dot_on_missed_block(fired_block)
                        player = False                                 
    else:
        if (left_margin <= mouse_position[0] <= (left_margin + block_size * 10)) and (upper_margin <= mouse_position[1] <= upper_margin + block_size * 10):
            if click:
                if ((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size) not in all_clicks:
                    all_clicks.append(((mouse_position[0] - left_margin - block_size * 15) // block_size, (mouse_position[1] - upper_margin) // block_size))
                    # проверяется попал ли игрок в корабль, если попал то крестик, нет точка
                    if ((mouse_position[0] - left_margin) // block_size, (mouse_position[1] - upper_margin) // block_size) in ships_coordinates_player_one:
                        put_cross_on_hitted_block(fired_block)
                        ships_coordinates_player_one.remove(((mouse_position[0] - left_margin) // block_size, (mouse_position[1] - upper_margin) // block_size))
                        if len(ships_coordinates_player_one) == 0:
                            draw_end_screen(player=False)                        
                    else:
                        put_dot_on_missed_block(fired_block)
                        player = True
                       
        
def put_cross_on_hitted_block(fired_block):
    crosses_set.add(fired_block)
    draw_cross_from_hitted_blocks(crosses_set)
    
    
def put_dot_on_missed_block(fired_block):
    dotted_set.add(fired_block)
    draw_from_dotted_set(dotted_set)


def draw_from_dotted_set(dotted_set):
    for i in dotted_set:
        pygame.draw.circle(screen, BLACK, (block_size*(i[0]-0.5)+left_margin, block_size*(i[1]-0.5)+upper_margin), block_size//6)


def draw_cross_from_hitted_blocks(crosses_set):
    for block in crosses_set:
        x1 = block_size * (block[0]-1) + left_margin
        y1 = block_size * (block[1]-1) + upper_margin
        pygame.draw.line(screen, BLACK, (x1, y1),
                         (x1+block_size, y1+block_size), block_size//6)
        pygame.draw.line(screen, BLACK, (x1, y1+block_size),
                         (x1+block_size, y1), block_size//6)
        

def draw_end_screen(player):
    end_menu_img = pygame.image.load("end_of_war.jpg")
    screen.blit(end_menu_img, (0, 0))
    if player:
        font_1 = pygame.font.SysFont('notosans', 50)
        player_1 = font_1.render("PLAYER 1 WIN", True, BLACK)
        screen.blit(player_1, (530, 100))
        pygame.display.update()
    else:
        font_1 = pygame.font.SysFont('notosans', 50)
        player_2 = font_1.render("PLAYER 2 WIN", True, BLACK)
        screen.blit(player_2, (530, 100))
        pygame.display.update()
    
    
def main():
    menu_img = pygame.image.load("light_fight.jpg")
    btn = Button(210, 70, 47, (78, 24, 2), (106, 45, 2))
    show = True
    game_over = False
    flag = False
    screen.blit(menu_img, (0, 0))
    btn.draw_button(500, 600, "ИГРАТЬ")

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                btn.draw_button(500, 600, "ИГРАТЬ")
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and (500 < event.pos[0] < 710) and (600 < event.pos[1] < 670):
                flag = True
        if flag:
            break

    btn = Button(220, 70, 47, (6, 30, 120), (5, 60, 110))
    flag = False
    bld_sps = Build_ships()
    screen.fill(WHITE)
    run = True
    bld_sps.build_grid()
    font_1 = pygame.font.SysFont('notosans', 50)
    player1 = font_1.render("PLAYER 1", True, BLACK)
    screen.blit(player1, (530, 40))
    btn.draw_button(500, 600, "Я ГОТОВ")
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                btn.draw_button(500, 600, "Я ГОТОВ")
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bld_sps.get_coordinates(ships_coordinates_player_one)
            if event.type == pygame.MOUSEBUTTONDOWN and (500 < event.pos[0] < 720) and (600 < event.pos[1] < 670):
                flag = True
        if flag:
            break

    btn = Button(220, 70, 47, (6, 30, 120), (5, 60, 110))
    flag = False
    bld_sps = Build_ships()
    screen.fill(WHITE)
    run = True
    bld_sps.build_grid()
    player2 = font_1.render("PLAYER 2", True, BLACK)
    screen.blit(player2, (530, 40))
    btn.draw_button(500, 600, "Я ГОТОВ")
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                btn.draw_button(500, 600, "Я ГОТОВ")
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bld_sps.get_coordinates(ships_coordinates_player_two)
            if event.type == pygame.MOUSEBUTTONDOWN and (500 < event.pos[0] < 720) and (600 < event.pos[1] < 670):
                flag = True
        if flag:
            break

    screen.fill(WHITE)
    draw_grid()
    player1 = font_1.render("PLAYER_1", True, BLACK)
    player2 = font_1.render("PLAYER_2", True, BLACK)
    sign1_width = player1.get_width()
    sign2_width = player2.get_width()
    screen.blit(player1, (left_margin + 5 * block_size - sign1_width //
                          2, upper_margin - block_size // 2 - font_size))
    screen.blit(player2, (left_margin + 20 * block_size - sign2_width //
                          2, upper_margin - block_size // 2 - font_size))
    while not game_over:
        if len(ships_coordinates_player_two) == 0:
            draw_end_screen(player=True)
        elif len(ships_coordinates_player_one) == 0:
            draw_end_screen(player=False)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                fight_coordinates()
        pygame.display.update()

main()
pygame.quit()
quit()
