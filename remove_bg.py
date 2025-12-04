from PIL import Image
import os

def remove_white_background(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Change all white (also shades of whites)
            # to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        print("Successfully removed white background")
        
    except Exception as e:
        print(f"Error processing image: {e}")

# Path to the logo
logo_path = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\static\core\logo.png"

# Process the image
remove_white_background(logo_path, logo_path)
