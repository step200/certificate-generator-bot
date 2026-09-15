import io
import os
from PIL import Image, ImageDraw, ImageFont

def get_cyrillic_font(size: int):
    font_names = [
        "arial.ttf", "Arial.ttf", 
        "DejaVuSans.ttf", "FreeSans.ttf", 
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
        "/System/Library/Fonts/Supplemental/Arial.ttf"     
    ]
    for font in font_names:
        try:
            return ImageFont.truetype(font, size)
        except OSError:
            continue
    return ImageFont.load_default()

def generate_certificate_image(name: str, course: str, date_str: str) -> io.BytesIO:
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color='#F9F9FB')
    draw = ImageDraw.Draw(img)

    draw.rectangle([30, 30, width - 30, height - 30], outline="#2C3E50", width=5)
    draw.rectangle([45, 45, width - 45, height - 45], outline="#3498DB", width=2)

    font_title = get_cyrillic_font(52)
    font_name = get_cyrillic_font(44)
    font_body = get_cyrillic_font(28)
    font_sub = get_cyrillic_font(22)

    draw.text((width // 2, 120), "СЕРТИФИКАТ", fill="#2C3E50", font=font_title, anchor="mm")
    draw.text((width // 2, 180), "ОБ УСПЕШНОМ ОКОНЧАНИИ КУРСА", fill="#7F8C8D", font=font_sub, anchor="mm")
    
    draw.text((width // 2, 290), "Настоящий сертификат подтверждает, что", fill="#34495E", font=font_body, anchor="mm")
    draw.text((width // 2, 380), name, fill="#2980B9", font=font_name, anchor="mm")
    draw.text((width // 2, 470), "успешно прошел(а) обучение по программе:", fill="#34495E", font=font_body, anchor="mm")
    draw.text((width // 2, 540), f"«{course}»", fill="#2C3E50", font=font_body, anchor="mm")
    
    draw.text((200, 680), f"Дата выдачи: {date_str}", fill="#7F8C8D", font=font_sub, anchor="lm")
    draw.text((width - 200, 680), "Школа программирования", fill="#7F8C8D", font=font_sub, anchor="rm")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer