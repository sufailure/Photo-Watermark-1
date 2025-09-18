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
                    # 只取年月日
                    date_part = value.split(" ")[0]
                    ymd = date_part.split(":")
                    if len(ymd) == 3:
                        return f"{ymd[0]}-{ymd[1]}-{ymd[2]}"
                    return date_part.replace(":", "-")
        return None
    except Exception as e:
        print(f"Error reading EXIF data for {image_path}: {e}")
        return None

def add_watermark(image_path, text, font_size, color, position):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        # 加载系统字体 DejaVuSans.ttf
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except Exception as e:
            print(f"Error loading font 'DejaVuSans.ttf': {e}. Using default font.")
            font = ImageFont.load_default()

        # 使用 textbbox 替代 textsize
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
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

        # 确保输出目录始终为 ./picture/picture_watermark
        parent_dir = os.path.dirname(image_path)
        output_dir = os.path.join(parent_dir, "picture_watermark")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, os.path.basename(image_path))
        image.save(output_path)
        print(f"Watermarked image saved to {output_path}")
    except Exception as e:
        print(f"Error adding watermark for {image_path}: {e}")

def main():
    print("=== 图片批量水印工具 ===")
    image_dir = input("请输入图片文件夹路径: ").strip()
    if not os.path.isdir(image_dir):
        print("目录不存在: ", image_dir)
        exit()

    font_size = int(input("请输入字体大小（如32）: ").strip())
    color = input("请输入字体颜色（如'white'、'255,255,255'或'#FF5733'，默认white）: ").strip() or 'white'
    position = input("请输入水印位置（top-left, center, bottom-right，默认bottom-right）: ").strip() or 'bottom-right'

    # 确保输出目录始终为 ./picture/picture_watermark
    output_dir = os.path.join(image_dir, "picture_watermark")
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for file in os.listdir(image_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            image_path = os.path.join(image_dir, file)
            exif_date = extract_exif_date(image_path)
            if exif_date:
                add_watermark(image_path, exif_date, font_size, color, position)
                count += 1
            else:
                print(f"未找到EXIF日期: {file}")
    print(f"处理完成，共处理 {count} 张图片。输出目录: {output_dir}")

if __name__ == "__main__":
    main()
