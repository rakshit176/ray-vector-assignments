# ImageProcessor

ImageProcessor is a Python script designed to process images, identify shapes, and calculate dimensions based on a calibration shape. It can work with both image files and generated shapes, making it versatile for various applications.

## Features

- **Image Input Options**: Accepts file paths or numpy arrays as input.
- **Gray & Binary Image Conversion**: Converts images to grayscale and binary format.
- **Shape Detection**: Identifies contours and filters them based on area.
- **Calibration Shape**: Detects a rectangular calibration shape to calculate a pixel-to-unit ratio.
- **Contour Drawing**: Draws contours, edges, and corner points on detected shapes.
- **Edge Length Calculation**: Computes and displays the lengths of edges in real-world units.
- **Output Options**: Saves the processed image with annotations and displays the number of detected shapes.

## Requirements

- Python 3.x
- OpenCV
- NumPy

## Installation

```bash
pip install numpy opencv-python
