from PIL import Image, ImageDraw, ImageFont
import os

uploads_dir = os.path.join('static', 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

img = Image.new('RGB', (300, 300), color = (255, 255, 255))
draw = ImageDraw.Draw(img)

border_color = (220, 220, 220)
draw.rectangle([0, 0, 299, 299], outline=border_color, width=2)

font = ImageFont.truetype("arial.ttf", 40)
text = "No\nImage"
draw.text((100, 120), text, fill=(150, 150, 150), font=font, align="center")

img.save(os.path.join(uploads_dir, 'default-item.jpg'))
