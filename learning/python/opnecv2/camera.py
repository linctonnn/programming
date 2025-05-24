import cv2 as cv

livePreview = cv.VideoCapture(0)

while True:
    isTrue, frame = livePreview.read()
    if not isTrue:
        break

    flipped = cv.flip(frame, 1)

    # Changed the color to gray
    gray = cv.cvtColor(flipped, cv.COLOR_BGR2GRAY)

    # Blur
    blur = cv.GaussianBlur(gray, (7, 7), cv.BORDER_DEFAULT)

    cv.imshow('Open Camera', blur)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

livePreview.release()
cv.destroyAllWindows()
