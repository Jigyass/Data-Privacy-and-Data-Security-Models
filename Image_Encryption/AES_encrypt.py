import cv2

#image_path = input("Enter path to the image file:")
image_path = "/home/jigya/Desktop/Github_Projects/Data-Privacy-and-Data-Security-Models/Test/A1SizePorsche911GT3RS.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image could not be processed")
else: 
    print("Image loaded successfully")
flattened_image = image.flatten()
image_bytes = flattened_image.tobytes()
original_shape = image.shape()
