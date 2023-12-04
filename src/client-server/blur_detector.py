import cv2
import os


def detect_blur_spot(image, threshold=10):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian filter for edge detection
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Calculate maximum intensity and variance
    laplacian_variance = laplacian.var()

    # Initialize result variables
    blur_text = "Normal"
    text_color = (0, 255, 0)

    # Check blur condition based on variance of Laplacian image
    if laplacian_variance < threshold:
        blur_text = "Blurry"
        text_color = (255, 0, 0)
    # Add labels to the image
    cv2.putText(image, "{}: {:.2f}".format(blur_text, laplacian_variance), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                text_color, 3)

    return image
