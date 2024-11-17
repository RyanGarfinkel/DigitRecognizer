import pygame
from tensorflow.keras.models import load_model
import numpy as np

# Initialize game and load model
pygame.init()
model = load_model('model.keras')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up window and font
pygame.display.set_caption('Digit Recognizer')
window = pygame.display.set_mode((800, 600))

font = pygame.font.SysFont('arial', 20)

def setup_winow():

    window.fill(WHITE)

    # Drawing area    
    text = font.render('Draw Here', True, BLACK)
    window.blit(text, (140, 45))
    pygame.draw.rect(window, BLACK, pygame.Rect(40, 70, 300, 300), 10)

    # Clear button
    clear_text = font.render('Clear', True, BLACK)
    clear_text_rect = clear_text.get_rect(center=(190, 437.5))
    window.blit(clear_text, clear_text_rect.topleft)
    pygame.draw.rect(window, BLACK, pygame.Rect(115, 400, 150, 75), 10)

    # Prediction labels
    display_predictions(np.zeros((1, 10)), 0)

    pygame.display.update()

def clear_drawing():

    pygame.draw.rect(window, WHITE, pygame.Rect(50, 80, 280, 280))
    pygame.display.update()

def handle_clear_button(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 115 <= x <= 265 and 400 <= y <= 475:
            clear_drawing()

def get_image():

    # Get 280x280 image from drawing area
    pixels = pygame.surfarray.array3d(window)
    pixels = np.mean(pixels, axis=2)
    pixels = pixels[50:330, 80:360]

    # Resize to 28x28 then normalize
    surface = pygame.surfarray.make_surface(pixels)
    surface = pygame.transform.scale(surface, (28, 28))
    pixels = pygame.surfarray.array3d(surface)
    pixels = np.mean(pixels, axis=2)

    pixels = (255 - pixels) / 255.0

    # Orient image then match model input shape
    pixels = np.rot90(pixels, 3)
    pixels = np.fliplr(pixels)

    pixels = pixels.reshape((28, 28, 1))
    pixels = np.expand_dims(pixels, axis=0)

    return pixels

def display_predictions(predictions, digit):

    pygame.draw.rect(window, WHITE, pygame.Rect(450, 30, 350, 570))

    # Draw prediction label
    text = font.render(f'Guess: {digit}', True, BLACK)
    window.blit(text, (500, 50))
    
    # Draw bars
    for i in range(10):
        label = font.render(f'{i}:', True, BLACK)
        label_height = label.get_height()
        y_position = 75 + i*50 + (35 - label_height) // 2
        window.blit(label, (455, y_position))
        pygame.draw.rect(window, RED, pygame.Rect(455 + label.get_width() + 10, 75 + i*50, int(predictions[0][i]*175), 35))
    
    pygame.display.update()

def predict():

    img = get_image()
    prediction = model.predict(img)
    guess = np.argmax(prediction)

    display_predictions(prediction, guess)

def draw_handler(event):

    if event.type != pygame.MOUSEMOTION or not event.buttons[0]:
        return
    
    x, y = pygame.mouse.get_pos()

    if 50 <= x <= 330 and 80 <= y <= 330:
        x = x - (x % 10)
        y = y - (y % 10)
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 10, 10))
        pygame.display.update()

        predict()

setup_winow()

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        draw_handler(event)
        handle_clear_button(event)

pygame.quit()