import cv2
import numpy as np
from generator import ShapeGenerator


class ImageProcessor:
    def __init__(self, image_input):
        if isinstance(image_input, str):
            self.image = cv2.imread(image_input)
        elif isinstance(image_input, np.ndarray):
            self.image = image_input
        else:
            raise ValueError(
                "image_input should be either a file path or a numpy array"
            )

        if self.image is None:
            raise ValueError(
                "Image could not be loaded. Check the path or the array provided."
            )

        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.binary = self._threshold_image(self.gray)
        self.cal_shape = self._find_calibration_shape(self.binary)
        self.pixel_to_unit = (
            self._calculate_calibration_ratio() if self.cal_shape is not None else None
        )

    def _threshold_image(self, gray):
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return binary

    def _find_calibration_shape(self, binary):
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:  # Assuming the calibration shape is a rectangle
                return approx
        return None

    def _calculate_calibration_ratio(self):
        width = np.linalg.norm(self.cal_shape[0][0] - self.cal_shape[1][0])
        height = np.linalg.norm(self.cal_shape[1][0] - self.cal_shape[2][0])
        return (210 + 268) / (width + height)  # Average of both dimensions

    def _filter_contours(self, contours, min_area=100):
        return [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    def _draw_contours(self, output, contours):
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw edges and corners
            for i in range(len(approx)):
                cv2.line(
                    output,
                    tuple(approx[i][0]),
                    tuple(approx[(i + 1) % len(approx)][0]),
                    (0, 255, 0),
                    2,
                )
                cv2.circle(output, tuple(approx[i][0]), 3, (0, 0, 255), -1)

            # Calculate and display edge lengths
            for i in range(len(approx)):
                pt1 = approx[i][0]
                pt2 = approx[(i + 1) % len(approx)][0]
                pixel_distance = np.linalg.norm(pt1 - pt2)
                unit_distance = pixel_distance * self.pixel_to_unit
                mid_point = ((pt1 + pt2) / 2).astype(int)
                cv2.putText(
                    output,
                    f"{unit_distance:.1f}",
                    tuple(mid_point),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    (0, 0, 0),
                    1,
                )

    def process_image(self):
        if self.cal_shape is None:
            print("Calibration shape not found")
            return self.image, 0

        contours, _ = cv2.findContours(
            self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        filtered_contours = self._filter_contours(contours)

        num_shapes = len(filtered_contours)

        output = self.image.copy()
        self._draw_contours(output, filtered_contours)

        cv2.putText(
            output,
            f"Number of shapes: {num_shapes}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            4,
        )

        return output, num_shapes

    def save_output(self, output_image, output_path):
        cv2.imwrite(output_path, output_image)

    def show_output(self, output_image):
        cv2.imshow("Output Image", output_image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()  # Close the image window


# Usage


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
