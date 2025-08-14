# 代码生成时间: 2025-08-14 14:54:01
import os
from PIL import Image
from celery import Celery

# 配置Celery
app = Celery('batch_image_resizer')
app.config_from_object('celeryconfig')

# 任务函数：调整图片尺寸
@app.task
def resize_image(image_path, output_path, size):
    try:
        # 打开图片
        with Image.open(image_path) as img:
            # 调整图片尺寸
            resized_img = img.resize(size)
            # 保存调整后的图片
            resized_img.save(output_path)
            print(f"Image resized and saved to {output_path}")
    except IOError:
        print(f"Error: Could not open or process image {image_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# 任务函数：批量调整图片尺寸
@app.task
def resize_images(image_paths, output_paths, size):
    for image_path, output_path in zip(image_paths, output_paths):
        resize_image.delay(image_path, output_path, size)

# 辅助函数：检查输出目录是否存在
def check_and_create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# 主函数：批量调整图片尺寸
def main():
    # 输入参数
    input_dir = 'path/to/input/images'
    output_dir = 'path/to/output/images'
    output_size = (800, 600)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    # 检查输出目录是否存在
    check_and_create_output_dir(output_dir)

    # 获取所有图片文件
    image_paths = []
    output_paths = []
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_paths.append(os.path.join(input_dir, filename))
            output_paths.append(os.path.join(output_dir, filename))

    # 批量调整图片尺寸
    resize_images(image_paths, output_paths, output_size)

if __name__ == '__main__':
    main()