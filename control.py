import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import ImageGrab, ImageOps
import numpy as np
import os
import shutil

# Set up the WebDriver
driver = webdriver.Chrome()
driver.set_window_size(800, 600)  # Set the window size
driver.get("https://elgoog.im/dinosaur-game/")

# Clear the image cache
image_cache_dir = "game_images"
if os.path.exists(image_cache_dir):
    shutil.rmtree(image_cache_dir)  # Remove the directory and its contents

os.makedirs(image_cache_dir)  # Recreate the empty directory

# Wait for the game to load
time.sleep(2)

# Press space to start the game
body = driver.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.SPACE)


def jump():
    body.send_keys(Keys.SPACE)


def is_obstacle(data, threshold):
    # Check if there's any column in the image where the sum of black pixels is greater than the threshold
    for column in data.T:
        if np.sum(column) < threshold:
            print(np.sum(column))
            return True
    return False


def get_image():
    # Capture the screen
    bbox = (153, 571, 253, 671)  # Adjust the bounding box to your screen resolution and game area
    img = ImageGrab.grab(bbox)
    gray_image = ImageOps.grayscale(img)
    a = np.array(gray_image)
    return a, img


def has_movement(current_image, previous_image, movement_threshold):
    if previous_image is None:
        return True  # Assume movement if there is no previous image to compare
    diff = np.sum(np.abs(current_image - previous_image))
    print(f"Movement difference: {diff}")
    return diff > movement_threshold


# Set the threshold for detecting obstacles
threshold = 25100
movement_threshold = 2000  # Increase the threshold to make it less sensitive
no_movement_duration = 0

previous_image = None
image_index = 1  # Start index for image filenames

while True:
    image_data, img = get_image()

    # Check for movement
    if not has_movement(image_data, previous_image, movement_threshold):
        no_movement_duration += 0.2
    else:
        no_movement_duration = 0  # Reset the duration if movement is detected

    if no_movement_duration >= 5:
        print("No movement detected for 1 second. Quitting the game.")
        break

    previous_image = image_data  # Update the previous image

    if is_obstacle(image_data, threshold):  # Use the set threshold
        # Save the captured image before the jump with incrementing filename
        filename = f"{image_cache_dir}/image_{image_index}.png"
        img.save(filename)
        print(f"Saved {filename}")
        image_index += 1  # Increment the filename index

        jump()
        time.sleep(0.1)  # Small delay after jump to avoid multiple jumps

    time.sleep(0.2)  # Capture images every 200ms

# Quit the browser after the loop
driver.quit()
