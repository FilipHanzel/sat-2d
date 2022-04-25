import pygame

from sat import Shape, Point, sat


def display_message(
    surface: pygame.Surface, text: str, coords=(300, 30), font_size=20
) -> None:
    font = pygame.font.Font("freesansbold.ttf", font_size)
    text_surface = font.render(text, True, (0.1, 0.7, 0.2))
    text_rect = text_surface.get_rect()
    text_rect.center = coords
    surface.blit(text_surface, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SAT")

    clock = pygame.time.Clock()

    square = Shape(
        shape=[Point(-40, 40), Point(40, 40), Point(40, -40), Point(-40, -40)],
        position=(400, 300),
    )
    triangle = Shape(
        shape=[Point(-40, -40), Point(-40, 40), Point(40, 0)], position=(400, 300)
    )

    resolve = True

    end = False
    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            end = True

        if keys[pygame.K_w]:
            square.forward()
        if keys[pygame.K_s]:
            square.reverse()
        if keys[pygame.K_a]:
            square.turn_left()
        if keys[pygame.K_d]:
            square.turn_right()

        if keys[pygame.K_UP]:
            triangle.forward()
        if keys[pygame.K_DOWN]:
            triangle.reverse()
        if keys[pygame.K_LEFT]:
            triangle.turn_left()
        if keys[pygame.K_RIGHT]:
            triangle.turn_right()

        screen.fill((170, 180, 110))

        result = sat(square, triangle, resolve)

        display_message(screen, "Collision:", (400, 10), 15)
        display_message(screen, str(result), (400, 25), 15)

        triangle.update()
        square.update()

        if result:
            triangle.draw(screen, (255, 0, 0))
            square.draw(screen, (255, 0, 0))
        else:
            triangle.draw(screen, (0, 0, 255))
            square.draw(screen, (0, 0, 255))

        pygame.display.flip()
        clock.tick(120)  # 120 fps cap

    pygame.quit()


if __name__ == "__main__":
    main()
