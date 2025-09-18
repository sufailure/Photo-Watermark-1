import os
import sys
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

def extract_exif_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return value.split(" ")[0].replace(":", "-")
        return None
    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return None

def add_watermark(image_path, text, font_size, color, position):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", font_size)

        text_width, text_height = draw.textsize(text, font=font)
        width, height = image.size

        if position == "top-left":
            x, y = 10, 10
        elif position == "center":
            x, y = (width - text_width) // 2, (height - text_height) // 2
        elif position == "bottom-right":
            x, y = width - text_width - 10, height - text_height - 10
        else:
            raise ValueError("Invalid position. Choose from 'top-left', 'center', 'bottom-right'.")

        draw.text((x, y), text, fill=color, font=font)

        output_dir = os.path.join(os.path.dirname(image_path), os.path.basename(os.path.dirname(image_path)) + "_watermark")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, os.path.basename(image_path))
        image.save(output_path)
        print(f"Watermarked image saved to {output_path}")
    except Exception as e:
        print(f"Error adding watermark: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python watermark.py <image_directory>")
        return

    image_dir = sys.argv[1]
    output_dir = "{}_watermark".format(image_dir)

    font_size = int(input("Enter font size: "))
    color = input("Enter font color (e.g., 'white', 'black', '#FF5733'): ")
    position = input("Enter position (top-left, center, bottom-right): ")

    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(root, file)
                exif_date = extract_exif_date(image_path)
                if exif_date:
                    add_watermark(image_path, exif_date, font_size, color, position)
                else:
                    print(f"No EXIF date found for {file}")

if __name__ == "__main__":
    main()
