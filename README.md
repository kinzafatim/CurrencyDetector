# CurrencyDetector
This is a desktop application built using Python, OpenCV, and Tkinter for detecting fake Pakistani currency notes (PKR). It uses Digital Image Processing techniques such as grayscale conversion and template matching (correlation) to compare uploaded note images with real note templates.

## 🖼️ Overview

The app compares an uploaded image of a currency note against a set of preloaded templates (real currency notes) and uses correlation to determine authenticity.

## 📷 Features
   📁 Upload .jpg, .jpeg, or .png images of currency notes
   
  ⚙️ Compares them with real currency templates using grayscale correlation
  
  🖼️ Displays:
  
      -The uploaded input image
      -The closest matching template
      -A result label indicating Real or Fake
  
  🎨 Simple and minimal Tkinter GUI

## 🧰 Requirements
  Install the following Python libraries before running the app:
      
      pip install opencv-python pillow numpy
## 📁 Folder Structure

      project/
      │
      ├── main.py               # Main application file
      ├── templates/            # Folder containing template currency images
      │   ├── 10.jpg
      │   ├── 20.jpg
      │   └── ...               # Name files as denomination (e.g., 50.jpg, 100.jpg)
      └── README.md             # This file

## 🚀 How to Run

  Ensure the templates/ folder exists and contains valid grayscale currency images.

  Run the application:

      python main.py
## 📊 Detection Logic

  -Converts input and template images to grayscale

  -Resizes input image to match the template dimensions

  -Computes correlation coefficient between the images

  -Compares the highest correlation score against a threshold (0.9 by default) to determine authenticity
