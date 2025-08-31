import pygame
import sys
from gtts import gTTS
import tempfile
import time

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Text to MP3")

# BACKGROUND_COLOR = pygame.Color(245, 245, 245)
# TEXT_COLOR = pygame.Color(20, 20, 20)
# INPUT_BG_COLOR = pygame.Color(255, 255, 255)
# BUTTON_COLOR = pygame.Color(240, 240, 240)
# BUTTON_HOVER_COLOR = pygame.Color(220, 220, 220)
# BUTTON_TEXT_COLOR = pygame.Color(0, 0, 0)
# BORDER_COLOR = pygame.Color(0, 0, 0)

BACKGROUND_COLOR = pygame.Color(50, 50, 50)
INPUT_BG_COLOR = pygame.Color(100, 100, 100)
BUTTON_COLOR = pygame.Color(75, 75, 75)
BUTTON_TEXT_COLOR = pygame.Color(220, 220, 220)
BUTTON_HOVER_COLOR = pygame.Color(100, 100, 100)
TEXT_COLOR = pygame.Color(220, 220, 220)
BORDER_COLOR = pygame.Color(100, 100, 100)

font_name = "Tahoma"
font = pygame.font.SysFont(font_name, 36)
label_font = pygame.font.SysFont(font_name, 24)
button_font = pygame.font.SysFont(font_name, 30)
dropdown_font = pygame.font.SysFont(font_name, 20)

# Input box
input_box = pygame.Rect(100, 120, 440, 150)
input_active = True
text = ''
# cursor
cursor_visible = True
last_cursor_toggle = time.time()
cursor_interval = 0.5  # seconds
cursor_index = 0  # Tracks the position in the `text`
# backspace
backspace_held = False
backspace_timer = 0
backspace_delay = 0.1  # seconds between deletions

# Buttons
button_height = 50
button_width1 = 100
button_width2 = 160
ok_button = pygame.Rect(input_box.right - button_width1, input_box.bottom + 30, button_width1, button_height)
clear_button = pygame.Rect(input_box.x, input_box.bottom + 30, button_width1, button_height)
test_button = pygame.Rect(input_box.x + (input_box.width - button_width2) // 2, input_box.bottom + 30, button_width2, button_height)

# File number dropdown
file_numbers = ['1', '2', '3', '4', '5']
selected_file_number = '1'
file_dropdown_open = False
file_dropdown_rect = pygame.Rect(input_box.x + 180, input_box.bottom + button_width1, 50, 30)

# Languages
languages = ["de", "en", "fr", "it"]
accents = ["de", "co.uk", "fr", "it"]
selected_language = "de"
selected_accent = "de"
dropdown_open = False
dropdown_rect = pygame.Rect(input_box.right - 80, 20, 80, 30)

# Draw the circle (outline only)
circle_center = (16, 16)
circle_radius = 15
circle_width = 2  # Thickness of the outline
# Define the triangle points
triangle_points = [
    (12, 8),
    (12, 24),
    (24, 16)
]

def wrap_text(text, font, max_width):
    words = text.replace('\n', ' \n ').split(' ')
    lines = []
    line = ''
    for word in words:
        if word == '\n':
            lines.append(line)
            line = ''
            continue
        test_line = f"{line} {word}".strip() if line else word
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines

# Main loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # File dropdown opened and a number is selected
            if file_dropdown_open:
                for i, num in enumerate(file_numbers):
                    option_rect = pygame.Rect(file_dropdown_rect.x, file_dropdown_rect.y - (i + 1) * 30, file_dropdown_rect.width, 30)
                    if option_rect.collidepoint(event.pos):
                        selected_file_number = num
                        file_dropdown_open = False
                        break
                else:
                    file_dropdown_open = False
                continue  # <- Skip further checks in this event
        
            # Language dropdown
            if dropdown_open:
                for i, lang in enumerate(languages):
                    option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + i * 30, dropdown_rect.width, 30)
                    if option_rect.collidepoint(event.pos):
                        selected_language = lang
                        selected_accent = accents[i]
                        dropdown_open = False
                        break
                else:
                    dropdown_open = False
                continue  # <- Skip further checks if language dropdown handled
        
            # Toggle dropdowns
            if dropdown_rect.collidepoint(event.pos):
                dropdown_open = not dropdown_open
            elif file_dropdown_rect.collidepoint(event.pos):
                file_dropdown_open = not file_dropdown_open
        
            elif ok_button.collidepoint(event.pos) and text.strip():
                # Save MP3 file
                tts = gTTS(text=text, lang=selected_language, tld=selected_accent, slow=False)
                tts.save(f"000{selected_file_number}.mp3")
                text = ''
            elif test_button.collidepoint(event.pos) and text.strip():
                # Play MP3 audio
                tts = gTTS(text=text, lang=selected_language, tld=selected_accent, slow=False)
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tmp_file.close()
                tts.save(tmp_file.name)
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
            elif clear_button.collidepoint(event.pos):
                text = ''
                            
            if input_box.collidepoint(event.pos):
                # Determine cursor position based on click
                mx, my = event.pos
                relative_x = mx - input_box.x - 10
                relative_y = my - input_box.y - 10
            
                lines = wrap_text(text, font, input_box.width - 20)
                y_offset = 0
                cursor_index = len(text)  # default to end if not found
                char_counter = 0
            
                for line in lines:
                    line_height = font.get_height() + 5
                    if y_offset <= relative_y <= y_offset + line_height:
                        for i in range(len(line) + 1):
                            substr = line[:i].replace(" ", "\u00A0")
                            if font.size(substr)[0] >= relative_x:
                                cursor_index = char_counter + i
                                break
                        break
                    char_counter += len(line)
                    y_offset += line_height
                    
        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                if cursor_index > 0 and time.time() - backspace_timer > backspace_delay:
                    backspace_held = True
                    text = text[:cursor_index - 1] + text[cursor_index:]
                    cursor_index -= 1
                    backspace_timer = time.time()
            elif event.key == pygame.K_DELETE:
                if cursor_index < len(text):
                    text = text[:cursor_index] + text[cursor_index + 1:]
            elif event.key == pygame.K_LEFT:
                if cursor_index > 0:
                    cursor_index -= 1
            elif event.key == pygame.K_RIGHT:
                if cursor_index < len(text):
                    cursor_index += 1
            elif event.key == pygame.K_RETURN:
                text = text[:cursor_index] + '\n' + text[cursor_index:]
                cursor_index += 1
            else:
                text = text[:cursor_index] + event.unicode + text[cursor_index:]
                cursor_index += 1
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                backspace_held = False
    
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(BACKGROUND_COLOR)

    label = label_font.render("Write your sentence:", True, TEXT_COLOR)
    screen.blit(label, (input_box.x, input_box.y - 30))

    pygame.draw.rect(screen, INPUT_BG_COLOR, input_box, border_radius = 10)
    border_col = pygame.Color(100, 100, 255) if input_active else BORDER_COLOR
    pygame.draw.rect(screen, border_col, input_box, 2, border_radius = 10)
    
    if backspace_held and time.time() - backspace_timer > backspace_delay:
        if cursor_index > 0 and text:
            text = text[:cursor_index - 1] + text[cursor_index:]
            cursor_index -= 1
            backspace_timer = time.time()
            
    lines = wrap_text(text, font, input_box.width - 20)
    y_offset = 0
    for line in lines:
        txt_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10 + y_offset))
        y_offset += txt_surface.get_height() + 5

    if input_active and cursor_visible:        
        lines = wrap_text(text[:cursor_index], font, input_box.width - 20)
        cursor_line = lines[-1] if lines else ''
        cursor_x = input_box.x + 10 + font.size(cursor_line.replace(" ", "\u00A0"))[0]
        cursor_y = input_box.y + 10 + (len(lines) - 1) * (font.get_height() + 5)
        cursor_height = font.get_height()
        pygame.draw.line(screen, TEXT_COLOR, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
    
    # OK button
    ok_hover = ok_button.collidepoint(mouse_pos)
    ok_bg = BUTTON_HOVER_COLOR if ok_hover else BUTTON_COLOR
    pygame.draw.rect(screen, ok_bg, ok_button, border_radius=8)
    pygame.draw.rect(screen, BORDER_COLOR, ok_button, 1, border_radius=8)
    ok_text = button_font.render("OK", True, BUTTON_TEXT_COLOR)
    screen.blit(ok_text, (ok_button.x + (ok_button.width - ok_text.get_width()) // 2, ok_button.y + (ok_button.height - ok_text.get_height()) // 2))
    
    # Clear button
    clear_hover = clear_button.collidepoint(mouse_pos)
    clear_bg = BUTTON_HOVER_COLOR if clear_hover else BUTTON_COLOR
    pygame.draw.rect(screen, clear_bg, clear_button, border_radius=8)
    pygame.draw.rect(screen, BORDER_COLOR, clear_button, 1, border_radius=8)
    clear_text = button_font.render("Clear", True, BUTTON_TEXT_COLOR)
    screen.blit(clear_text, (clear_button.x + (clear_button.width - clear_text.get_width()) // 2, clear_button.y + (clear_button.height - clear_text.get_height()) // 2))

    # Test button with play icon
    spacing = 10
    test_text = button_font.render("Test", True, BUTTON_TEXT_COLOR)
    
    icon_size = circle_radius * 2 + circle_width
    total_width = icon_size + spacing + test_text.get_width()
    
    # Start X to center the whole block 
    start_x = test_button.x + (test_button.width - total_width) // 2
    # Vertical center for icon and text
    y_center = test_button.y + (test_button.height - icon_size) // 2
    
    if file_dropdown_open:
        test_bg = BUTTON_COLOR
    else:
        test_hover = test_button.collidepoint(mouse_pos)
        test_bg = BUTTON_HOVER_COLOR if test_hover else BUTTON_COLOR
    pygame.draw.rect(screen, test_bg, test_button, border_radius = 8)
    pygame.draw.rect(screen, BORDER_COLOR, test_button, 1, border_radius = 8)

    # Draw a simple play icon (triangle) next to the text
    triangle_color = BUTTON_TEXT_COLOR
    # Apply offsets
    triangle_points_offset = [
        (x + start_x, y + y_center) for (x, y) in triangle_points
    ]
    pygame.draw.polygon(screen, triangle_color, triangle_points_offset)
    
    # Draw the circle (outline only)
    circle_color = BUTTON_TEXT_COLOR  # Dark gray
    circle_center_offset = (circle_center[0] + start_x, circle_center[1] + y_center)
    pygame.draw.circle(screen, circle_color, circle_center_offset, circle_radius, circle_width)
    
    # Draw text next to icon with spacing
    text_x = start_x + icon_size + spacing
    text_y = test_button.y + (test_button.height - test_text.get_height()) // 2
    screen.blit(test_text, (text_x, text_y))


    # buttons
    ok_text = button_font.render("OK", True, BUTTON_TEXT_COLOR)
    clear_text = button_font.render("Clear", True, BUTTON_TEXT_COLOR)

    screen.blit(ok_text, (ok_button.x + (ok_button.width - ok_text.get_width()) // 2, ok_button.y + (ok_button.height - ok_text.get_height()) // 2))
    screen.blit(clear_text, (clear_button.x + (clear_button.width - clear_text.get_width()) // 2, clear_button.y + (clear_button.height - clear_text.get_height()) // 2))

    # language dropdown
    pygame.draw.rect(screen, BUTTON_COLOR, dropdown_rect, border_radius = 6)
    pygame.draw.rect(screen, BORDER_COLOR, dropdown_rect, 1, border_radius = 6)
    lang_surface = dropdown_font.render(selected_language, True, BUTTON_TEXT_COLOR)
    screen.blit(lang_surface, (dropdown_rect.x + (dropdown_rect.width - lang_surface.get_width()) // 2, dropdown_rect.y + 5))

    if dropdown_open:
        for i, lang in enumerate(languages):
            option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + i * 30, dropdown_rect.width, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, option_rect, border_radius = 6)
            pygame.draw.rect(screen, BORDER_COLOR, option_rect, 1, border_radius = 6)
            option_text = dropdown_font.render(lang, True, BUTTON_TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + (option_rect.width - option_text.get_width()) // 2, option_rect.y + 5))

    file_label = label_font.render("Index Nr:", True, TEXT_COLOR)
    screen.blit(file_label, (input_box.x, input_box.bottom + button_width1))

    pygame.draw.rect(screen, BUTTON_COLOR, file_dropdown_rect, border_radius = 6)
    pygame.draw.rect(screen, BORDER_COLOR, file_dropdown_rect, 1, border_radius = 6)
    file_num_surface = dropdown_font.render(selected_file_number, True, BUTTON_TEXT_COLOR)
    screen.blit(file_num_surface, (file_dropdown_rect.x + (file_dropdown_rect.width - file_num_surface.get_width()) // 2, file_dropdown_rect.y + 5))

    if file_dropdown_open:
        for i, num in enumerate(file_numbers):
            option_rect = pygame.Rect(file_dropdown_rect.x, file_dropdown_rect.y - (i + 1) * 30, file_dropdown_rect.width, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, option_rect, border_radius = 6)
            pygame.draw.rect(screen, BORDER_COLOR, option_rect, 1, border_radius = 6)
            option_text = dropdown_font.render(num, True, BUTTON_TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + (option_rect.width - option_text.get_width()) // 2, option_rect.y + 5))

    # Hover for language dropdown main button
    dropdown_hover = dropdown_rect.collidepoint(mouse_pos)
    dropdown_bg = BUTTON_HOVER_COLOR if dropdown_hover else BUTTON_COLOR
    pygame.draw.rect(screen, dropdown_bg, dropdown_rect, border_radius = 6)
    pygame.draw.rect(screen, BORDER_COLOR, dropdown_rect, 1, border_radius = 6)
    lang_surface = dropdown_font.render(selected_language, True, BUTTON_TEXT_COLOR)
    screen.blit(lang_surface, (dropdown_rect.x + (dropdown_rect.width - lang_surface.get_width()) // 2, dropdown_rect.y + (dropdown_rect.height - lang_surface.get_height()) // 2))
    
    # Hover for language options if open
    if dropdown_open:
        for i, lang in enumerate(languages):
            option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + i * 30, dropdown_rect.width, 30)
            option_hover = option_rect.collidepoint(mouse_pos)
            option_bg = BUTTON_HOVER_COLOR if option_hover else BUTTON_COLOR
            pygame.draw.rect(screen, option_bg, option_rect, border_radius = 6)
            pygame.draw.rect(screen, BORDER_COLOR, option_rect, 1, border_radius = 6)
            option_text = dropdown_font.render(lang, True, BUTTON_TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + (option_rect.width - option_text.get_width()) // 2, option_rect.y + 5))
    
    # Hover for file number dropdown main button
    file_dropdown_hover = file_dropdown_rect.collidepoint(mouse_pos)
    file_dropdown_bg = BUTTON_HOVER_COLOR if file_dropdown_hover else BUTTON_COLOR
    pygame.draw.rect(screen, file_dropdown_bg, file_dropdown_rect, border_radius = 6)
    pygame.draw.rect(screen, BORDER_COLOR, file_dropdown_rect, 1, border_radius = 6)
    file_num_surface = dropdown_font.render(selected_file_number, True, BUTTON_TEXT_COLOR)
    screen.blit(file_num_surface, (file_dropdown_rect.x + (file_dropdown_rect.width - file_num_surface.get_width()) // 2, file_dropdown_rect.y + (file_dropdown_rect.height - file_num_surface.get_height()) // 2))
    
    # Hover for file number options if open
    if file_dropdown_open:
        for i, num in enumerate(file_numbers):
            option_rect = pygame.Rect(file_dropdown_rect.x, file_dropdown_rect.y - (i + 1) * 30, file_dropdown_rect.width, 30)
            option_hover = option_rect.collidepoint(mouse_pos)
            option_bg = BUTTON_HOVER_COLOR if option_hover else BUTTON_COLOR
            pygame.draw.rect(screen, option_bg, option_rect, border_radius = 6)
            pygame.draw.rect(screen, BORDER_COLOR, option_rect, 1, border_radius = 6)
            option_text = dropdown_font.render(num, True, BUTTON_TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + (option_rect.width - option_text.get_width()) // 2, option_rect.y + 5))
    
    # Toggle cursor visibility
    current_time = time.time()
    if current_time - last_cursor_toggle > cursor_interval:
        cursor_visible = not cursor_visible
        last_cursor_toggle = current_time
    
    cursor_index = max(0, min(cursor_index, len(text)))
    
    pygame.display.flip()

pygame.quit()
sys.exit()