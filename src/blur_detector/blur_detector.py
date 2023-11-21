import cv2
import os


def detect_blur_spot(image_path, threshold):
    # Read the image
    image = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian filter for edge detection
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Calculate maximum intensity and variance
    laplacian_variance = laplacian.var()

    # Initialize result variables
    blur_text = "Not Blurry"

    # Check blur condition based on variance of Laplacian image
    if laplacian_variance < threshold:
        blur_text = "Blurry"

    # Add labels to the image
    cv2.putText(image, "{}: {:.2f}".format(blur_text, laplacian_variance), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    # Display the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
