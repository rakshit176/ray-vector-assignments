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
```

## Usage
Run the script and follow the prompts to either generate shapes or provide an image path:

```bash
python process.py
```

## Example Workflow
Generate Shapes:
- Choose to generate shapes.
- The script will create an image with random shapes.
- Shapes will be processed and displayed.
- 
##Provide Image Path:
- Provide the path to an image file.
- The image will be processed, and shapes will be detected and annotated.
  
## Functions
- ImageProcessor.__init__(image_input): Initializes the processor with an image.
- _threshold_image(gray): Converts a grayscale image to binary.
- _find_calibration_shape(binary): Finds a calibration shape (rectangle).
- _calculate_calibration_ratio(): Calculates pixel-to-unit ratio.
- _filter_contours(contours, min_area=100): Filters contours by area.
- _draw_contours(output, contours): Draws contours and annotations.
- process_image(): Processes the image, detects shapes, and annotates them.
- save_output(output_image, output_path): Saves the processed image.
- show_output(output_image): Displays the processed image.

## Example

```bash
from generator import ShapeGenerator
from process import ImageProcessor

def main():
    choice = input("Want to generate shapes? (yes/y or no/n): ").strip().lower()
    if choice in ["yes", "y"]:
        generator = ShapeGenerator()
        shapes_img = generator.generate_shapes()
        processor = ImageProcessor(shapes_img)
    elif choice in ["no", "n"]:
        image_path = input("Please provide the image path: ").strip()
        processor = ImageProcessor(image_path)
    else:
        print("Invalid input. Please enter 'yes/y' or 'no/n'.")
        return

    result, num_shapes = processor.process_image()
    print(f"::::: NUMBER OF SHAPES :: {num_shapes} :::::")
    processor.save_output(result, "Results.png")
    # processor.show_output(result)

# Run the main function
main()
```

## Contributing
Feel free to open issues or submit pull requests for improvements and bug fixes.

## License
This project is licensed under the MIT License.
