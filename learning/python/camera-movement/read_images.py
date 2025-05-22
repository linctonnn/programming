import cv2 as cv

read_videos = cv.VideoCapture(0)

def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)

def changeRes(width, height):
    read_videos.set(3, width)
    read_videos.set(4, height)

changeRes(1980, 1080)

while True:
    isTrue, frame = read_videos.read()
    frame_resized = rescaleFrame(frame)
    
    cv.imshow('Camera Open', frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break


read_videos.release()
cv.destroyAllWindows()
