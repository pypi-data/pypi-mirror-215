# =============================================================================
# Import third-party libraries
from numpy import ndarray
from skimage import io, transform, exposure
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from typing import Union, Tuple


# Create a bbox class
class BBoxes:
    """Class to calculate and represent bounding boxes from a mask file"""
    bbox: np.ndarray

    # Constructor
    def __init__(self, bboxes, mask=None, image=None) -> None:
        """

        :type bboxes: np.ndarray
        :type mask: np.ndarray
        :param bboxes: A numpy array with the bounding boxes.
        :param mask: A numpy array with the mask.
        :return: Object of type BBoxes.
        """
        # Read in the mask file
        self.mask = mask
        self.bboxes = bboxes
        self.image = image

    @classmethod
    def from_mask(cls,
                  file: Union[str, Path]) -> object:
        """
        Calculates the bounding boxes from the mask file.
        :param file: A numpy array with the mask.
        :return: Object of type BBoxes.
        """

        # Read in the mask file
        mask = io.imread(file)

        # Get indexes of nonzero elements
        nonzero = np.array(np.nonzero(mask)).T

        # Get cell identities of nonzero matrix
        identities = np.array(list(map(lambda x: mask[x[0]][x[1]], nonzero)))

        # Stack identities with the nonzero matrix
        stacked = np.column_stack((identities, nonzero))

        # sort them by identity
        stacked = stacked[stacked[:, 0].argsort()]

        # Group them by identity
        grouped = np.split(stacked[:, 1:], np.unique(stacked[:, 0], return_index=True)[1][1:])

        # Get the bounding boxes for each identity
        bboxes = np.array(list(map(lambda x: np.array([min(x[:, 0]), max(x[:, 0]), min(x[:, 1]), max(x[:, 1])]),
                                   np.array(grouped, dtype=object))))

        # Since the bounding boxes are calculated from the group identities we can add column with the identities
        bboxes = np.column_stack((np.unique(stacked[:, 0]), bboxes))

        return cls(bboxes, mask)

    @staticmethod
    def iou(box1: np.array,
            box2: np.array) -> float:
        """
        Calculates the IoU for two bounding boxes.
        :param box1: Numpy array with the first bounding box.
        :param box2: Numpy array with the second bounding box.
        :return: A float with the IoU value between the two bounding boxes.
        """
        # Calculate the intersection box
        x1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y1 = max(box1[3], box2[3])
        y2 = min(box1[4], box2[4])

        # Calculate intersection area
        intersection = max(0, x2 - x1) * max(0, y2 - y1)

        # If intersection is 0 IoU is 0
        if intersection == 0:
            return 0

        # Calculate union area
        area1 = (box1[2] - box1[1]) * (box1[4] - box1[3])
        area2 = (box2[2] - box2[1]) * (box2[4] - box2[3])
        union = area1 + area2 - intersection

        # Calculate and return IoU
        iou = intersection / union

        if intersection > union:
            print(intersection, union, iou)

        return iou

    @property
    def iou_matrix(self) -> np.array:
        """
        Returns the IoU matrix for the bounding boxes.
        :return: A numpy array with the IoU values for each bounding box pair.
        """
        n = self.__len__()
        # compute the size of the matrix based on the length of the array
        size = n * (n - 1) // 2

        # create a 1D array of zeros to hold the upper triangular matrix
        triangular = np.zeros(size)

        # fill the upper triangular matrix with elements from the original array
        k = 0
        for i in range(n):
            for j in range(i + 1, n):
                triangular[k] = self.iou(self.bboxes[i], self.bboxes[j])
                k += 1

        # convert the 1D array to a 2D matrix
        matrix: ndarray = np.zeros((n, n))
        matrix[np.triu_indices(n, k=1)] = triangular

        return matrix

    # Bounding box IoU operations
    def are_overlapping(self) -> np.array:
        """
        Returns a boolean array indicating whether the bounding boxes are overlapping.
        :return: A numpy array with boolean values for each bounding box pair.
        """
        # Get the IoU matrix
        overlapping = np.where(self.iou_matrix > 0)

        # Get the identities from the overlapping indexes
        identities = self.bboxes[np.unique(overlapping), 0]

        return identities

    def overlapping_pairs(self) -> (np.array, np.array):
        """
        Returns the overlapping pairs of bounding boxes. The first array contains the identities, the second the IoU
        values.
        :return: A tuple of two numpy arrays.
        """
        # Get the IoU matrix
        iou_matrix = self.iou_matrix

        # Get elements that are not zero
        x, y = np.where(iou_matrix > 0)
        v = iou_matrix[x, y]
        x = self.bboxes[x, 0]
        y = self.bboxes[y, 0]

        return np.array([x, y]).T, v

    # Magic methods
    def __len__(self) -> int:
        return self.bboxes.shape[0]

    def __getitem__(self, item) -> ndarray:
        return self.bboxes[item]

    def __str__(self):
        return str(self.bboxes)

    def __setattr__(self, key: str, value: object) -> None:
        if key == 'image':
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str) or isinstance(value, Path):
                self.__dict__[key] = io.imread(value)
            elif value is None:
                self.__dict__[key] = value
            else:
                raise TypeError("Image must be of type numpy array or string.")

        elif key == 'mask':
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str):
                self.__dict__[key] = io.imread(value)
            elif value is None:
                self.__dict__[key] = value
            else:
                raise TypeError("Mask must be of type numpy array or string.")

        else:
            self.__dict__[key] = value

    # Bounding box operations
    def expand(self,
               n: int = 0) -> object:
        """
        Expands the bounding boxes by n pixels.
        :param n: Integer with the number of pixels to expand the bounding boxes.
        :return: Object of type BBoxes with the expanded bounding boxes.
        """
        # Expand the bounding boxes by n pixels, but not beyond the image size.
        expanded = np.array(list(map(lambda x: np.array([x[0],
                                                         max(x[1] - n, 0),
                                                         min(x[2] + n, self.mask.shape[0]),
                                                         max(x[3] - n, 0),
                                                         min(x[4] + n, self.mask.shape[1])]), self.bboxes)))
        return BBoxes(expanded, self.mask, self.image)

    def identities(self) -> np.array:
        """
        Returns the identities of the bounding boxes.
        :return: numpy array with the identities of the bounding boxes.
        """
        return self.bboxes[:, 0]

    def idx(self) -> np.array:
        """
        Returns the indexes of the bounding boxes.
        :return: numpy array with the indexes of the bounding boxes.
        """
        return self.bboxes[:, 0] - 1

    # Bounding box properties
    def get_sides(self) -> np.array:
        """
        Returns the sides of the bounding boxes.
        :return: numpy array with the sides of the bounding boxes.
        """
        # Get the sides of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         self.bboxes[:, 2] - self.bboxes[:, 1],
                         self.bboxes[:, 4] - self.bboxes[:, 3]]).T

    def get_areas(self) -> np.ndarray:
        """
        Returns the areas of the bounding boxes.
        :return: numpy array with the areas of the bounding boxes.
        """
        # Get the areas of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         (self.bboxes[:, 2] - self.bboxes[:, 1]) *
                         (self.bboxes[:, 4] - self.bboxes[:, 3])]).T

    def get_ratios(self) -> np.ndarray:
        """
        Returns the aspect ratios of the bounding boxes.
        :return: numpy array with the aspect ratios of the bounding boxes.
        """
        # Get the aspect ratios of the bounding boxes
        ratios = np.array((self.bboxes[:, 2] - self.bboxes[:, 1]) / (self.bboxes[:, 4] - self.bboxes[:, 3]))

        return np.array(([self.bboxes[:, 0], ratios]))

    def get_centers(self) -> np.ndarray:
        """
        Returns the centers of the bounding boxes.
        :return: numpy array with the centers of the bounding boxes.
        """
        # Get the centers of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         (self.bboxes[:, 2] + self.bboxes[:, 1]) // 2,
                         (self.bboxes[:, 4] + self.bboxes[:, 3]) // 2]).T

    def get(self,
            by: str = "area") -> np.ndarray:
        """
        Returns the values of the bounding boxes based on the given parameter.
        :param by: Mode to use for getting the values of the bounding boxes [default="area"].
        :return:
        """
        # Get the values of the bounding boxes
        if by == 'area':
            values = self.get_areas()
        elif by == 'ratio':
            values = self.get_ratios()
        elif by == 'center':
            values = self.get_centers()
        elif by == 'sides':
            values = self.get_sides()
        else:
            raise NotImplementedError('Invalid filter parameter, please select from area, ratio, center or sides.')

        return values

    # Bounding box filters
    def filter(self,
               by: str = "area",
               operator: np.ufunc = np.greater_equal,
               value: Union[float, Tuple[float, float]] = 0) -> object:
        """
        Filter the bounding boxes based on the given parameters
        :param by: Choose between area, ratio, center or dims to filter the bounding boxes [default="area"].
        :param operator: Numpy comparison operator to use [default=np.greater_equal]
        :param value: Value to be used for filtering [default=0].
        :return: np.ndarray
        """

        # Get the values of the bounding boxes that are filtered
        values = self.get(by)

        # Filter the bounding boxes based on the given parameters
        if by == "sides":
            idx = np.where(operator(values[:, 1], value[0]) & operator(values[:, 2], value[1]))[0]
        else:
            idx = np.where(operator(values[:, 1], value))[0]

        return BBoxes(self.bboxes[idx], self.mask, self.image)

    def remove_from_edge(self) -> object:
        """
        Removes the bounding boxes that are on the edge of the image.
        :return: BBoxes object with the bounding boxes that are not on the edge of the image.
        """
        # Removes the bounding boxes that are on the edge of the image
        idx = np.where((self.bboxes[:, 1] > 0) &
                       (self.bboxes[:, 2] < self.mask.shape[0]) &
                       (self.bboxes[:, 3] > 0) &
                       (self.bboxes[:, 4] < self.mask.shape[1]))[0]

        # Returns the bounding boxes
        return BBoxes(self.bboxes[idx], self.mask)

    # Plotting
    def plot_to_mask(self,
                     output_file: Union[str, None, Path] = None) -> None:
        """
        Plots the bounding boxes on the mask.
        :param output_file: Path to the output file [default=None].
        :return: None
        """
        # Get the ratio of the mask
        mask_ratio = self.mask.shape[0] / self.mask.shape[1]

        # Draw the bounding boxes on the mask
        fig, ax = plt.subplots(1, 1, figsize=(10, mask_ratio * 10))
        ax.imshow(self.mask, cmap="gray")

        # Draw the bounding boxes
        for bbox in self.bboxes:
            ax.plot([bbox[3], bbox[4]], [bbox[1], bbox[1]], color="red")  # Top
            ax.plot([bbox[3], bbox[4]], [bbox[2], bbox[2]], color="red")  # Bottom
            ax.plot([bbox[3], bbox[3]], [bbox[1], bbox[2]], color="red")  # Left
            ax.plot([bbox[4], bbox[4]], [bbox[1], bbox[2]], color="red")  # Right
        ax.axis("off")
        fig.tight_layout()

        # If not path is given, show the plot
        if output_file is not None:
            plt.savefig(output_file)
        else:
            plt.show()

    def plot_to_image(self,
                      output_file: Union[str, None, Path] = None) -> None:
        """
        Plots the bounding boxes on the image instead of on the mask.
        :param output_file: Path to the output file [default=None].
        :return: None
        """
        # Get the ratio of the mask
        mask_ratio = self.mask.shape[0] / self.mask.shape[1]

        # Draw the bounding boxes on the mask
        fig, ax = plt.subplots(1, 1, figsize=(10, mask_ratio * 10))
        ax.imshow(self.image, cmap="gray")

        # Draw the bounding boxes
        for bbox in self.bboxes:
            ax.plot([bbox[3], bbox[4]], [bbox[1], bbox[1]], color="red", linewidth=1)  # Top
            ax.plot([bbox[3], bbox[4]], [bbox[2], bbox[2]], color="red", linewidth=1)  # Bottom
            ax.plot([bbox[3], bbox[3]], [bbox[1], bbox[2]], color="red", linewidth=1)  # Left
            ax.plot([bbox[4], bbox[4]], [bbox[1], bbox[2]], color="red", linewidth=1)  # Right
        ax.axis("off")
        fig.tight_layout()

        # If not path is given, show the plot
        if output_file is not None:
            plt.savefig(output_file)
        else:
            plt.show()

    # Isolation
    def calculate_resizing_factor(self,
                                  desired_ratio: float,
                                  size: int) -> np.ndarray:
        """
        Calculates the resizing factor for each bounding box to get the desired image size / cell size ratio

        :param desired_ratio: Desired image size / cell size ratio.
        :param size: Desired image size.
        :return: List of resizing factors for each bounding box.
        """
        return np.array(list(map(lambda x: desired_ratio / (max(x[2] - x[1], x[4] - x[3]) / size), self.bboxes)))

    @staticmethod
    def _pad_crop(sc: np.ndarray,
                  size: Tuple[int, int]) -> np.ndarray:
        """
        Makes an image square to a desire size without changing the ratio

        :param size: Final desired size
        :return: Image of the desired sized, with added padding where needed
        """
        ox = sc.shape[0]
        oy = sc.shape[1]

        # Get the difference between the current size and the desired size
        dif_x = size[0] - sc.shape[0]
        dif_y = size[1] - sc.shape[1]

        # Getting the difference for each size of the image
        dif_x1 = dif_x // 2
        dif_x2 = dif_x // 2 + dif_x % 2
        dif_y1 = dif_y // 2
        dif_y2 = dif_y // 2 + dif_y % 2
        diffs = np.array([dif_x1, dif_x2, dif_y1, dif_y2])

        # Get crop differences
        dif_crop = np.where(diffs < 0, -diffs, 0)

        # Get pad differences
        dif_pad = np.where(diffs >= 0, diffs, 0)

        # Remove pixels from image if difference is negative
        sc = sc[0 + dif_crop[0]:ox - dif_crop[1], 0 + dif_crop[2]:oy - dif_crop[3]]

        # Assuming the image is smaller than the desired size
        sc = np.pad(sc, [(dif_pad[0], dif_pad[1]), (dif_pad[2], dif_pad[3])], mode="constant")

        return sc

    def extract(self,
                resize_factors: list,
                size: Tuple[int, int],
                output: Union[str, Path]) -> None:
        """
        Isolates the bounding boxes from the image and saves them to the given output folder.

        :param resize_factors: Desired ratio of the bounding box, takes the maximum of the width and height and resizes
        the image to the desired proportion (compared to the size value) while keeping the original aspect ratio.
        :param size: Desired size of the bounding box, final size of the image.
        :param output: Output folder to save the images to.
        """
        if isinstance(output, str):
            output = Path(output)

        # Iterate over the bounding boxes to get the single cell images
        for ds, (k, x1, x2, y1, y2) in zip(resize_factors, self.bboxes):
            sc = self.image[x1:x2, y1:y2]
            sc = transform.rescale(sc, ds, anti_aliasing=True)
            sc = self._pad_crop(sc, size)
            sc = exposure.rescale_intensity(sc, out_range=(0, 255)).astype(np.uint8)

            # Save the sc image
            output.mkdir(parents=True, exist_ok=True)
            io.imsave(f"{output}_{k}.png", sc)

    # Saving
    def save_iou(self,
                 output_file: str) -> None:
        """
        Saves the IoU matrix to a csv file.
        :param output_file: Path to the output file.
        :return: None
        """
        pairs, values = self.overlapping_pairs()

        # Save the IoU matrix to a csv file
        np.savetxt(output_file, pairs, delimiter=",", fmt="%d")

    def save_csv(self,
                 output_file: str) -> None:
        """
        Saves the bounding boxes to a csv file.
        :param output_file: Path to the output file.
        :return:
        """
        # Save the bounding boxes to a csv file
        np.savetxt(output_file, self.bboxes, delimiter=",", fmt="%d")
