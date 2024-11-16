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
window = pygame.display.set_mode((900, 800))

font = pygame.font.SysFont('arial', 20)

def clear_screen():

    window.fill(WHITE)

    # Drawing area
    pygame.draw.rect(window, BLACK, pygame.Rect(100, 100, 300, 300), 10)

    # Clear button
    clear_text = font.render('Clear', True, BLACK)
    window.blit(clear_text, (215, 450))
    pygame.draw.rect(window, BLACK, pygame.Rect(175, 425, 150, 75), 10)

def clear_button_handler(event):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 175 <= x <= 325 and 425 <= y <= 500:
            clear_screen()
            pygame.display.update()

def draw_handler(event):

    if event.type == pygame.MOUSEMOTION and event.buttons[0]:
        x, y = pygame.mouse.get_pos()
        if 110 <= x <= 390 and 110 <= y <= 390:
            x = x - (x % 10)
            y = y - (y % 10)
            obj = pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 10, 10))
            pygame.display.update(obj)

            predict()

def predict():

    # Get 280x280 image from drawing area
    pixels = pygame.surfarray.array3d(window)
    pixels = np.mean(pixels, axis=2)
    pixels = pixels[110:390, 110:390]

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

    prediction = model.predict(pixels)
    display_predictions(prediction, np.argmax(prediction))


def display_predictions(predictions, digit):

    pygame.draw.rect(window, WHITE, pygame.Rect(475, 50, 425, 600))

    # Draw prediction label
    text = font.render(f'Prediction: {digit}', True, BLACK)
    window.blit(text, (500, 50))
    
    # Draw bars
    for i in range(10):
        label = font.render(f'{i}:', True, BLACK)
        window.blit(label, (480, 100 + i*50))
        pygame.draw.rect(window, RED, pygame.Rect(500, 100 + i*50, int(predictions[0][i]*400), 50))

running = True
clear_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        draw_handler(event)
        clear_button_handler(event)

    pygame.display.flip()

pygame.quit()