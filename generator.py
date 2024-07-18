import cv2
import numpy as np
import random


class ShapeGenerator:
    def __init__(
        self,
        img_size=(568, 569),
        background_color=(200, 200, 200),
        max_shapes=50,
        max_attempts=2000,
    ):
        self.img_size = img_size
        self.background_color = background_color
        self.img = np.ones(img_size + (3,), dtype=np.uint8) * 200
        self.max_shapes = max_shapes
        self.max_attempts = max_attempts
        self.existing_shapes = []
        self.attempts = 0

    def rotate_shape(self, shape, angle):
        center = tuple(map(lambda x: int(round(x)), shape.mean(axis=0)))
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.transform(shape.reshape(-1, 1, 2), rot_mat).reshape(-1, 2)

    def random_shape(self, min_size=50, max_size=80):
        shape_type = random.choice(["rectangle", "triangle", "square"])
        if shape_type == "rectangle":
            width = random.randint(min_size, max_size)
            height = random.randint(min_size, max_size)
            shape = np.array(
                [(0, 0), (width, 0), (width, height), (0, height)], dtype=np.int32
            )
        elif shape_type == "square":
            side = random.randint(min_size, max_size)
            shape = np.array(
                [(0, 0), (side, 0), (side, side), (0, side)], dtype=np.int32
            )
        else:
            base = random.randint(min_size, max_size)
            height = random.randint(min_size, max_size)
            shape = np.array([(0, 0), (base, 0), (base // 2, height)], dtype=np.int32)

        angle = random.uniform(0, 360)
        return self.rotate_shape(shape, angle).astype(np.int32)

    def check_overlap(self, new_shape, min_distance=10):
        x, y, w, h = cv2.boundingRect(new_shape)
        expanded_rect = np.array(
            [
                [x - min_distance, y - min_distance],
                [x + w + min_distance, y - min_distance],
                [x + w + min_distance, y + h + min_distance],
                [x - min_distance, y + h + min_distance],
            ],
            dtype=np.int32,
        )

        for shape in self.existing_shapes:
            if cv2.intersectConvexConvex(expanded_rect, shape)[0] > 0:
                return True
        return False

    def generate_shapes(self):
        while (
            self.attempts < self.max_attempts
            and len(self.existing_shapes) < self.max_shapes
        ):
            shape = self.random_shape()
            x = random.randint(0, self.img_size[1] - 100)
            y = random.randint(0, self.img_size[0] - 100)
            new_shape = shape + (x, y)

            if not self.check_overlap(new_shape):
                cv2.fillPoly(self.img, [new_shape], (255, 0, 0))
                self.existing_shapes.append(new_shape)

            self.attempts += 1

        print(
            f"Image generated with {len(self.existing_shapes)} shapes and saved as 'generated_shapes.png'"
        )
        return self.img


if __name__ == "__main__":
    generator = ShapeGenerator()
    shapes_img = generator.generate_shapes()
