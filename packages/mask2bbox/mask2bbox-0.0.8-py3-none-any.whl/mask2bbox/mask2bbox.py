# Import libraries
import time
import argparse
from _bboxes import BBoxes
from pathlib import Path
import matplotlib.pyplot as plt

# Import third-party libraries
from skimage import io, exposure, transform, restoration
# from aicsimageio import AICSImage
import numpy as np
from tqdm import tqdm


# Get arguments
def get_arguments():
    # Start with the description
    description = "Converts all the masks in a folder to bounding boxes."

    # Add parser
    parser = argparse.ArgumentParser(description=description)

    # Add a group of arguments for input
    input = parser.add_argument_group(title="Input", description="Input arguments for the script.")
    input.add_argument("-m", "--mask", dest="mask", action="store", type=str, required=True,
                       help="Path to the mask file.")
    input.add_argument("-i", "--image", dest="image", action="store", type=str, required=False, default=None,
                       help="Path to the image file.")

    # Add a group of arguments with the tool filters
    filters = parser.add_argument_group(title="Options", description="Arguments for filtering boundign boxes.")
    filters.add_argument("-e", "--expand", dest="expand", action="store", type=int, required=False, default=0,
                         help="Number of pixels to expand the bounding boxes.")
    filters.add_argument("-fv", "--filter-value", dest="filter_value", action="store", type=float, required=False,
                         default=0.0, nargs="+", help="Filter bounding boxes with a given value value.")
    filters.add_argument("-fo", "--filter-operator", dest="filter_operator", action="store", type=str, required=False,
                         choices=["less_equal", "greater_equal", "equal", "not_equal"], default="greater_equal",
                         help="Filter operator. Options =  [less_equal, greater_equal, equal, not_equal]")
    filters.add_argument("-ft", "--filter-type", dest="filter_type", action="store", type=str, required=False,
                         choices=["area", "ratio", "center", "sides"], default="area",
                         help="Filter type. Options =  [area, ratio, center, sides]")
    filters.add_argument("-fe", "--filter-edge", dest="filter_edge", action="store_true", required=False,
                         default=False, help="Filter bounding boxes on the edge of the image.")

    # Add a group of arguments for re-sizing
    single_cell = parser.add_argument_group(title="Single Cell", description="Arguments that modify the behaviour for "
                                                                             "the single cell crops.")
    single_cell.add_argument("-s", "--size", dest="size", action="store", type=int, required=False, default=256,
                             help="Final image size for the single cell crops.")
    single_cell.add_argument("-rf", "--resize-factor", dest="resize_factor", action="store", type=float, required=False,
                             default=1.0, help="Resize factor for the single cell crops.")

    # Add a group of arguments for output
    output = parser.add_argument_group(title="Output", description="Output arguments for the script.")
    # output.add_argument("-o", "--output", dest="output", action="store", type=str, required=False, default=None,
    #                     help="Path to the output file with the bounding boxes.")
    # output.add_argument("-p", "--plot", dest="plot", action="store", type=str, required=False, default=None,
    #                     help="Path to the output file with the bounding boxes.")
    # output.add_argument("-iou" "--save-iou", dest="save_iou", action="store", type=str, required=False, default=None,
    #                     help="Path to the output file for the intersection over union (IoU) matrix.")
    output.add_argument("-osc", "--output-single-cells", dest="output_single_cells", action="store", type=str,
                        required=False, default=None, help="Path to the output file with the single cells.")

    # Parse arguments
    arg = parser.parse_args()

    # Choose filter type
    if arg.filter_operator == "less_equal":
        arg.filter_operator = np.less_equal
    elif arg.filter_operator == "greater_equal":
        arg.filter_operator = np.greater_equal
    elif arg.filter_operator == "equal":
        arg.filter_operator = np.equal
    elif arg.filter_operator == "not_equal":
        arg.filter_operator = np.not_equal
    else:
        raise ValueError(f"Filter type {arg.filter_operator} not recognized.")

    # If filter type is sides then the filter value must be a tuple
    # if arg.filter_type == "sides":
    #     arg.filter_value = (arg.filter_value, arg.filter_value)

    # Convert size to tuple
    arg.size = (arg.size, arg.size)

    # Standardize paths
    arg.mask = Path(arg.mask).resolve()
    arg.output = Path(arg.output).resolve() if arg.output is not None else None
    arg.image = Path(arg.image).resolve() if arg.image is not None else None
    arg.save_iou = Path(arg.save_iou).resolve() if arg.save_iou is not None else None
    arg.plot = Path(arg.plot).resolve() if arg.plot is not None else None
    arg.output_single_cells = Path(arg.output_single_cells).resolve() if arg.output_single_cells is not None else None

    # Return arguments
    return arg


def main(args):
    # Create a BBoxes object and get the bounding boxes
    print(f"Reading bounding boxes from        = {args.mask}")
    mask_boxes = BBoxes.from_mask(args.mask)
    print(f"Total number of bounding boxes     = {len(mask_boxes)}")

    if args.image is not None:
        print(f"Adding image file                  = {args.image}")
        mask_boxes.image = args.image

    # Get the resizing factor from the original bounding boxes
    print(f"Resizing factor                    = {args.resize_factor}")
    rf = mask_boxes.calculate_resizing_factor(args.resize_factor, args.size)

    # Filter edge
    print(f"Filtering bounding boxes on edge   = {args.filter_edge}")
    if args.filter_edge:
        mask_boxes = mask_boxes.filter_edge()

    # Filter bounding boxes by a given type, operator and value
    print(f"Filtering bounding boxes by        = {args.filter_type} {args.filter_operator} {args.filter_value}")
    mask_boxes = mask_boxes.filter(args.filter_type, args.filter_operator, args.filter_value)

    # Expand the bounding boxes
    print(f"Expanding bounding boxes by        = {args.expand}")
    mask_boxes = mask_boxes.expand(args.expand)

    # Save single cell bounding boxes
    if args.output_single_cells is not None:
        print(f"Saving single cell bounding boxes  = {args.output_single_cells}")
        mask_boxes.extract(rf[mask_boxes.idx()], args.size, args.output_single_cells)
    print(f"# of bounding boxes                = {len(mask_boxes)}")


# Run main
if __name__ == "__main__":
    # Get arguments
    args = get_arguments()

    # Run main and time it
    st = time.time()
    main(args)
    rt = time.time() - st
    print(f"Script finish in {rt // 60:.0f}m {rt % 60:.0f}s")