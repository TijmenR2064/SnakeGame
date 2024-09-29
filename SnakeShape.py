import pygame

white = (255, 255, 255)
yellow = (255,255,102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)


def draw_snake_head(dis, x, y, size, direction):
    # Draw the head (rounded rectangle for a more natural snake head shape)
    pygame.draw.rect(dis, green, [x, y, size, size], border_radius=size // 4)

    # Draw the eyes (larger and more centered)
    eye_size = size // 3
    eye_offset_x = size // 5
    eye_offset_y = size // 4

    # Position the eyes based on direction
    if direction == "UP" or direction == "DOWN":
        pygame.draw.circle(dis, white, (x + eye_offset_x, y + eye_offset_y), eye_size)
        pygame.draw.circle(dis, white, (x + size - eye_offset_x, y + eye_offset_y), eye_size)
    elif direction == "LEFT":
        pygame.draw.circle(dis, white, (x + eye_offset_y, y + eye_offset_x), eye_size)
        pygame.draw.circle(dis, white, (x + eye_offset_y, y + size - eye_offset_x), eye_size)
    elif direction == "RIGHT":
        pygame.draw.circle(dis, white, (x + size - eye_offset_y, y + eye_offset_x), eye_size)
        pygame.draw.circle(dis, white, (x + size - eye_offset_y, y + size - eye_offset_x), eye_size)

    # Draw pupils
    pupil_size = eye_size // 2
    if direction == "UP" or direction == "DOWN":
        pygame.draw.circle(dis, black, (x + eye_offset_x, y + eye_offset_y), pupil_size)
        pygame.draw.circle(dis, black, (x + size - eye_offset_x, y + eye_offset_y), pupil_size)
    elif direction == "LEFT":
        pygame.draw.circle(dis, black, (x + eye_offset_y, y + eye_offset_x), pupil_size)
        pygame.draw.circle(dis, black, (x + eye_offset_y, y + size - eye_offset_x), pupil_size)
    elif direction == "RIGHT":
        pygame.draw.circle(dis, black, (x + size - eye_offset_y, y + eye_offset_x), pupil_size)
        pygame.draw.circle(dis, black, (x + size - eye_offset_y, y + size - eye_offset_x), pupil_size)

    # Draw the tongue based on direction
    tongue_length = size // 1.5
    tongue_width = 3
    tongue_offset = size // 2

    if direction == "UP":
        pygame.draw.line(dis, red, (x + tongue_offset, y), (x + tongue_offset, y - tongue_length), tongue_width)
    elif direction == "DOWN":
        pygame.draw.line(dis, red, (x + tongue_offset, y + size), (x + tongue_offset, y + size + tongue_length), tongue_width)
    elif direction == "LEFT":
        pygame.draw.line(dis, red, (x, y + tongue_offset), (x - tongue_length, y + tongue_offset), tongue_width)
    elif direction == "RIGHT":
        pygame.draw.line(dis, red, (x + size, y + tongue_offset), (x + size + tongue_length, y + tongue_offset), tongue_width)