import os
import librosa
import soundfile as sf
import numpy as np
import pygame
import sys


pygame.init()

folder_original = "Original"
folder_adjusted = "Adjusted"

# Window setup
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Volume Settings")

# Colors
BACKGROUND_COLOR = pygame.Color(50, 50, 50)
BUTTON_COLOR = pygame.Color(75, 75, 75)
BUTTON_HOVER_COLOR = pygame.Color(100, 100, 100)
TEXT_COLOR = pygame.Color(220, 220, 220)

# Font
font = pygame.font.SysFont("Tahoma", 32)
header_font = pygame.font.SysFont("Tahoma", 28)
status_font = pygame.font.SysFont("Tahoma", 28)

# Function that will be executed when "Apply" is clicked
def change_audio_volume(input_file: str, output_file: str, percent: float):
    global status_text
    status_text = "Working..."
    redraw_screen()  # update UI before doing the work
    pygame.display.flip()

    # print(f"Applying function with volume: {percent}%")
    # Here you can call your librosa / soundfile volume scaling function instead
    # change_audio_volume("yourfile.mp3", volume_percent)
    
    """
    Change volume of an audio file (mp3 or wav) to a target percentage.
    
    :param input_file: path to input file
    :param output_file: path to save output
    :param percent: volume level in percent (100 = original, 50 = half, 200 = double)
    """
    if percent <= 0:
        raise ValueError("Percent must be greater than 0")

    # Load audio (sr=None keeps original sample rate)
    y, sr = librosa.load(input_file, sr=None, mono=False)  

    # Scale waveform
    scale = percent / 100.0
    y_scaled = y * scale

    # Prevent clipping
    max_val = np.max(np.abs(y_scaled))
    if max_val > 1.0:
        y_scaled = y_scaled / max_val
    # Save output
    sf.write(output_file, y_scaled.T, sr)
    
    status_text = "Ready"

def process_folder(folder = folder_original):
    for filename in os.listdir(folder):
        if filename.lower().endswith((".wav", ".mp3")):
            # print(filename)
            change_audio_volume(os.path.join(folder, filename), os.path.join(folder_adjusted, filename), VOLUME_PERCENT)
            
# Button class
class Button:
    def __init__(self, text, x, y, w, h, value=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.value = value

    def draw(self, screen, selected=False):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR

        if selected:
            # Brighten if selected
            color = (min(color[0]+40,255), min(color[1]+40,255), min(color[2]+40,255))

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        label = font.render(self.text, True, TEXT_COLOR)
        screen.blit(label, (self.rect.x + (self.rect.width - label.get_width()) // 2,
                            self.rect.y + (self.rect.height - label.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Function to execute when Apply is clicked
def apply_volume_setting(volume_percent):
    print(f"Applying function with volume: {volume_percent}%")
    # Replace this with your librosa/soundfile processing function

# Helper to redraw everything (so status updates immediately)
def redraw_screen():
    screen.fill(BACKGROUND_COLOR)

    # Render header text
    header_text = header_font.render("Adjusting volume of all the files", True, TEXT_COLOR)
    screen.blit(header_text, ((SCREEN_WIDTH - header_text.get_width()) // 2, 80))

    # Draw volume buttons
    for b in volume_buttons:
        b.draw(screen, selected_value == b.value)

    # Draw apply button
    apply_button.draw(screen)

    # Draw status text
    status_label = status_font.render(status_text, True, TEXT_COLOR)
    screen.blit(status_label, ((SCREEN_WIDTH - status_label.get_width()) // 2, 380))
    
# Create buttons in one row
button_width, button_height = 120, 60
start_x = 50
gap = 30
y_pos = 180  # adjusted downward to leave space for the header

volume_buttons = [
    Button("50%", start_x + (button_width+gap)*0, y_pos, button_width, button_height, 50),
    Button("75%", start_x + (button_width+gap)*1, y_pos, button_width, button_height, 75),
    Button("150%", start_x + (button_width+gap)*2, y_pos, button_width, button_height, 150),
    Button("200%", start_x + (button_width+gap)*3, y_pos, button_width, button_height, 200),
]

apply_button = Button("Apply", (SCREEN_WIDTH-150)//2, 300, 150, 60)

# Default selection
selected_value = 150
VOLUME_PERCENT = selected_value
status_text = "Ready"

# Main loop
clock = pygame.time.Clock()
while True:
    screen.fill(BACKGROUND_COLOR)

    # Render header text
    header_text = header_font.render("Adjusting volume of all the files", True, TEXT_COLOR)
    screen.blit(header_text, ((SCREEN_WIDTH - header_text.get_width()) // 2, 80))

    # Draw volume buttons
    for b in volume_buttons:
        b.draw(screen, selected_value == b.value)

    # Draw apply button
    apply_button.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Check volume buttons
            for b in volume_buttons:
                if b.is_clicked(pos):
                    selected_value = b.value
                    print(f"Selected {selected_value}%")
                    VOLUME_PERCENT = selected_value
            # Check apply button
            if apply_button.is_clicked(pos) and selected_value is not None:
                # apply_volume_setting(selected_value)
                process_folder()

    clock.tick(60)
