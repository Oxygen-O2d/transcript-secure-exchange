import os
from PIL import Image

def generate_text_file(filename, size_in_bytes):
    base_text = "UNIVERSITY REGISTRAR - ACADEMIC TRANSCRIPT\n"
    base_text += "Name: Jane Doe | Student ID: 987654321\n"
    base_text += "Course: Information Security | Grade: A+\n"
    base_text += "Course: Cryptography | Grade: A\n"
    base_text += "Course: Network Security | Grade: A-\n"
    base_text += "-" * 50 + "\n"
    
    with open(filename, 'w') as f:
        written = 0
        while written < size_in_bytes:
            f.write(base_text)
            written += len(base_text)

def generate_bitmap(filename):
    # Create a 256x256 image with simple patterns (checkerboard)
    width, height = 256, 256
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()
    
    for i in range(width):
        for j in range(height):
            if (i // 32) % 2 == (j // 32) % 2:
                pixels[i, j] = (0, 0, 0)
            else:
                pixels[i, j] = (255, 255, 255)
                
    img.save(filename, format='BMP')

if __name__ == "__main__":
    data_dir = os.path.dirname(__file__)
    print("Generating mock data...")
    generate_text_file(os.path.join(data_dir, "transcript.txt"), 1024)
    generate_text_file(os.path.join(data_dir, "test_10kb.txt"), 10240)
    generate_text_file(os.path.join(data_dir, "test_100kb.txt"), 102400)
    generate_text_file(os.path.join(data_dir, "test_1mb.txt"), 1024 * 1024)
    generate_bitmap(os.path.join(data_dir, "sample_image.bmp"))
    print("Mock data generated successfully.")
