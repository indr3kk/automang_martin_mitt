import pygame
import random


def reset_game():
    global punane_x, punane_y, sinised_autod, skoor, running
    punane_x = WIDTH // 2 - punane_auto.get_width() // 2
    punane_y = HEIGHT - punane_auto.get_height() - 10
    sinised_autod = []
    skoor = 0
    running = True
    for i in range(autode_arv):
        x = random.choice([200, 300, 400])
        y = random.randint(-300, -50)
        kiirus_auto = random.randint(2, 5)
        sinised_autod.append([x, y, kiirus_auto])


def game_loop():
    global punane_x, running, skoor
    while running:
        screen.blit(taust, (0, 0))
        screen.blit(punane_auto, (punane_x, punane_y))

        # punktid
        skoor_tekst = font.render(f"Skoor: {str(skoor)}", True, (255, 255, 255))
        screen.blit(skoor_tekst, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Punase auto liikumine
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and punane_x > 150:
            punane_x -= kiirus
        if keys[pygame.K_RIGHT] and punane_x < 500 - punane_auto.get_width():
            punane_x += kiirus

        # Siniste autode liikumine ja kokkupõrke tuvastamine
        for auto in sinised_autod:
            auto[1] += auto[2]
            if auto[1] > HEIGHT:
                auto[1] = random.randint(-300, -50)
                auto[0] = random.choice([200, 300, 400])
                auto[2] = random.randint(2, 5)
                skoor += 1
            screen.blit(sinine_auto, (auto[0], auto[1]))

            # Kokkupõrke kontroll
            punane_rect = pygame.Rect(punane_x, punane_y, punane_auto.get_width(), punane_auto.get_height())
            sinine_rect = pygame.Rect(auto[0], auto[1], sinine_auto.get_width(), sinine_auto.get_height())
            if punane_rect.colliderect(sinine_rect):
                running = False  # Kui punane auto puutub kokku sinise autoga, mäng lõppeb

        pygame.display.flip()
        pygame.time.delay(30)

    # Küsi mängijalt, kas ta soovib uuesti mängida
    game_over_screen()


def game_over_screen():
    screen.fill((0, 0, 0))
    tekst = font.render("Mäng läbi! Vajuta ENTER, et uuesti mängida või SPACE, et väljuda", True, (255, 255, 255))
    screen.blit(tekst, (WIDTH // 2 - tekst.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER
                    reset_game()
                    game_loop()
                elif event.key == pygame.K_SPACE:  # SPACE
                    pygame.quit()
                    return


# Algseadistused
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autode mäng")

# Lae pildid
try:
    taust = pygame.image.load("bg_rally.jpg")  # Lisa taustapildi fail
    punane_auto = pygame.image.load("f1_red.png")
    sinine_auto = pygame.image.load("f1_blue.png")

    # Pööra autod tagurpidi
    sinine_auto = pygame.transform.rotate(sinine_auto, 180)
except pygame.error as e:
    print(f"Pildifaili laadimise viga: {e}")
    pygame.quit()
    exit()

# Mängu muutujad
autode_arv = 3
sinised_autod = []
skoor = 0
font = pygame.font.Font(None, 20)
kiirus = 5  # Punase auto kiirus

# Mängu käivitamine
reset_game()
game_loop()
