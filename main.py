import pygame as pg
import time, random
import asyncio
pg.init()

# Variable
running = True
score = 0
font = pg.font.Font(None, 30)
last_tick = pg.time.get_ticks()

# Stuff you can modify
clock = 30  # Time you get
speed_up = 30
speed_left = 30
speed_right = 30
speed_down = 0
apple = 5
square_gravity = 1
apple_gravity = 2  # fall speed of apples
score_add = 1
bg_colour = (125, 255, 255)
text_colour = (0, 0, 0)
win_width = 500
win_height = 500
sq_size = 100
ap_size = 20
clock_dec = 1
freeze = 2

# Lives
lives = 5
max_lives = 5

# Window setup
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Fun game v1')

# Load sprites
sq_img = pg.image.load('./assets/images/square.png')
sq_img = pg.transform.scale(sq_img, (sq_size, sq_size))
ap_img = pg.image.load('./assets/images/apple.png')
ap_img = pg.transform.scale(ap_img, (ap_size, ap_size))


ap_data = []

# Square initial position
sq_pos = [win_width / 2, win_height / 2]
sq_data = [{"x": sq_pos[0], "y": sq_pos[1], "image": sq_img}]

# Gravity for square
def gravity():
    for square in sq_data:
        if square["y"] < win_height - sq_size + 22:
            square["y"] += square_gravity

# Create apple
def create_object(ap_data):
    if len(ap_data) < apple and random.random() < 0.1:
        x = random.randint(0, win_width - ap_size)
        y = win_height
        ap_data.append([x, y, ap_img])

# Update apples
def update_objects(ap_data):
    global score, clock, apple_gravity, lives
    for object in ap_data[:]:
        x, y, image_data = object
        if y > 0:
            y -= apple_gravity
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            clock -= clock_dec
            lives -= 1
            ap_data.remove(object)

# Collision check
def collision_check(ap_data, sq_pos):
    global score
    for object in ap_data[:]:
        x, y, image_data = object
        ap_rect = pg.Rect(x, y, ap_size, ap_size)
        sq_rect = pg.Rect(sq_pos[0], sq_pos[1], sq_size, sq_size)
        if sq_rect.colliderect(ap_rect):
            score += score_add
            ap_data.remove(object)

# Clock
def clock_time():
    global clock, running, last_tick
    now = pg.time.get_ticks()
    if now - last_tick >= 1000:
        clock -= 1
        last_tick = now
    if clock <= 0 or lives <= 0:
        time.sleep(freeze)
        running = False

# Main loop

async def main():
    global running, apple_gravity

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    sq_data[0]["x"] -= speed_left
                elif event.key == pg.K_RIGHT:
                    sq_data[0]["x"] += speed_right
                elif event.key == pg.K_UP:
                    sq_data[0]["y"] -= speed_up
                elif event.key == pg.K_DOWN:
                    sq_data[0]["y"] += speed_down

                # Adjust apple fall speed
                elif event.key == pg.K_EQUALS or event.key == pg.K_KP_PLUS:
                    apple_gravity += 1
                elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                    if apple_gravity > 1:
                        apple_gravity -= 1

                sq_pos[0], sq_pos[1] = sq_data[0]["x"], sq_data[0]["y"]

        # Fill background
        screen.fill(bg_colour)

        gravity()
        create_object(ap_data)
        collision_check(ap_data, sq_pos)
        update_objects(ap_data)
        clock_time()

        # Draw square
        screen.blit(sq_data[0]["image"], (sq_data[0]["x"], sq_data[0]["y"]))

        # Draw UI text
        text = font.render(f'Score: {score}', True, text_colour)
        screen.blit(text, (win_width - 100, win_height - 40))

        text2 = font.render(f'Time: {clock}', True, text_colour)
        screen.blit(text2, (win_width - 100, win_height - 60))

        speed_info = f'Speed: ←{speed_left} →{speed_right} ↑{speed_up} ↓{speed_down}'
        speed_text = font.render(speed_info, True, text_colour)
        screen.blit(speed_text, (10, win_height - 60))

        apple_speed_text = font.render(f'Apple Speed: {apple_gravity}', True, text_colour)
        screen.blit(apple_speed_text, (10, win_height - 80))

        lives_text = font.render(f'Lives: {lives}', True, text_colour)
        screen.blit(lives_text, (win_width - 100, win_height - 20))


        pg.display.flip()
        pg.time.Clock().tick(60)
        await asyncio.sleep(0)

    pg.quit()



asyncio.run(main())