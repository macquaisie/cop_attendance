import os
import pickle5 as pickle
from datetime import datetime
import cv2
import face_recognition
import cvzone
import numpy as np
import sqlite3
import time

# Constants and Configuration
ENCODE_FILE_PATH = "EncodeFile.p"
BACKGROUND_IMAGE_PATH = "Resources/background.png"
MODES_FOLDER_PATH = "Resources/Modes"

# Initialize SQLite database
conn = sqlite3.connect('attendance_database.db')
conn.execute('PRAGMA foreign_keys=ON')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,
        member_id INTEGER,
        member_name TEXT,
        status TEXT
    )
''')
conn.commit()

cap = cv2.VideoCapture(0)
cap.set(3, 620)
cap.set(4, 450)
imgBackground = cv2.imread(BACKGROUND_IMAGE_PATH)

# Load the encoding file
try:
    with open(ENCODE_FILE_PATH, 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
        encodeListKnown, memberIds = encodeListKnownWithIds
    print("Encode File Loaded")
except FileNotFoundError:
    print("Error: Encode file not found.")
    exit(1)

# Load the mode images into a list
imgModeList = [cv2.imread(os.path.join(MODES_FOLDER_PATH, path)) for path in os.listdir(MODES_FOLDER_PATH)]
imgModeList = [cv2.resize(img, (414, 633)) for img in imgModeList]

modeType = 0
counter = 0
id = -1
imgMember = []

while True:
    success, img = cap.read()

    if not success:
        print("Error: Could not read frame.")
        break

    # Face recognition preprocessing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    img = cv2.resize(img, (620, 460))

    # Update background image
    imgBackground[160:160 + 460, 39:39 + 620] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    # Face recognition
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = memberIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("COP Dumfries Assembly Face Attendance", imgBackground)
                    cv2.waitKey(1)  # Wait for 500 milliseconds (0.5 seconds)
                    counter = 1
                    modeType = 1
                    

        # Update student information
        if counter != 0:
            if counter == 1:
                # Retrieve member information from SQLite.
                cursor.execute('SELECT * FROM Members WHERE id = ?', (id,))
                memberInfo = cursor.fetchone()

                # Assuming your images are stored in a local folder named 'Images'
                image_path = f'Images/{id}.png'

                # Load the image from the local folder
                try:
                    with open(image_path, 'rb') as file:
                        array = np.frombuffer(file.read(), np.uint8)
                        imgMember = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                        print("Image Loaded")
                except FileNotFoundError:
                    print(f"Error: Image file {image_path} not found.")
                    # Handle the error as needed (e.g., display a placeholder image)
                    imgMember = np.zeros((216, 216, 3), dtype=np.uint8)

                datetimeObject = datetime.strptime(str(memberInfo[5]), "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                
                
                if secondsElapsed > 30:
                    # Update attendance
                    new_total_attendance = memberInfo[4] + 1
                    cursor.execute('''
                        UPDATE Members
                        SET total_attendance = ?,
                            last_attendance_time = ? 
                        WHERE id = ?
                    ''', (new_total_attendance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))

                    # Store attendance in SQLite
                    attendance_data = (None, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id, memberInfo[1], 'Present')
                    cursor.execute('''
                        INSERT INTO attendance VALUES (?, ?, ?, ?, ?)
                    ''', attendance_data)
                    conn.commit()
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # Draw member information on the background
                    cv2.putText(imgBackground, str(memberInfo[4]), (885, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
                    cv2.putText(imgBackground, str(memberInfo[2]), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(imgBackground, str(id), (1006, 474),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)

                    # Draw member name
                    (w, h), _ = cv2.getTextSize(memberInfo[1], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(memberInfo[1]), (808 + offset, 420),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    # Display member image
                    imgBackground[145:145 + 216, 908:908 + 216] = imgMember

                    counter += 1
                    time.sleep(3)
                    

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    memberInfo = []
                    imgMember = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("COP Dumfries Assembly Face Attendance", imgBackground)
    # Wait for a key press (1 means wait for 1 millisecond)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cursor.close()
conn.close()
cap.release()
cv2.destroyAllWindows()
time.sleep(1)
