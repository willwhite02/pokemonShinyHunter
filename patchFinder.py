import cv2

image = cv2.imread("capture_test.png")

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"x={x}, y={y}")

        temp = image.copy()
        cv2.circle(temp, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", temp)

cv2.imshow("Image", image)
cv2.setMouseCallback("Image", mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()