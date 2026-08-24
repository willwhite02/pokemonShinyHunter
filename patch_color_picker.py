import cv2
import numpy as np

IMAGE_PATH = "registeel/shinyRegisteel.png"
WINDOW_NAME = "Select Patch"

image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

clicks = []
display = image.copy()


def draw_selection() -> None:
    global display
    display = image.copy()

    for point in clicks:
        cv2.circle(display, point, 5, (0, 0, 255), -1)

    if len(clicks) == 2:
        (x1, y1), (x2, y2) = clicks
        left, right = sorted((x1, x2))
        top, bottom = sorted((y1, y2))
        cv2.rectangle(display, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow(WINDOW_NAME, display)


def mouse_click(event, x, y, flags, param) -> None:
    global clicks

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if len(clicks) == 2:
        clicks = []

    clicks.append((x, y))
    print(f"Clicked: x={x}, y={y}")

    if len(clicks) == 2:
        (x1, y1), (x2, y2) = clicks

        left, right = sorted((x1, x2))
        top, bottom = sorted((y1, y2))

        # OpenCV slices exclude the ending coordinate, so add 1 to include
        # the second clicked pixel in the selected rectangle.
        patch = image[top:bottom + 1, left:right + 1]

        if patch.size == 0:
            print("The selected patch is empty. Choose two different corners.")
        else:
            average_bgr = np.mean(patch, axis=(0, 1))

            print("\nSelected patch")
            print(f"Top-left:     x={left}, y={top}")
            print(f"Bottom-right: x={right}, y={bottom}")
            print(f"OpenCV slice: image[{top}:{bottom + 1}, {left}:{right + 1}]")
            print(f"Patch size:   {patch.shape[1]} x {patch.shape[0]} pixels")
            print(f"Average BGR:  {average_bgr}")

    draw_selection()


print("Click two opposite corners of the patch.")
print("After two clicks, the coordinates and average color will print.")
print("Click again to start a new selection. Press Q or Esc to quit.")

cv2.imshow(WINDOW_NAME, display)
cv2.setMouseCallback(WINDOW_NAME, mouse_click)

while True:
    key = cv2.waitKey(20) & 0xFF
    if key in (ord("q"), 27):
        break

cv2.destroyAllWindows()
