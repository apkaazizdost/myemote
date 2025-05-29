import cv2

# Open the default webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Show the frame in a window
    cv2.imshow("Webcam Feed - Press 'q' to quit", frame)

    # Wait for 1ms and break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
