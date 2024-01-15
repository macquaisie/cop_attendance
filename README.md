# cop_attendance
# Face Attendance System
This project implements a Face Attendance System using Python with OpenCV, face_recognition, and cvzone libraries. The system recognizes faces in a live video stream, matches them with known faces, and maintains attendance records in an SQLite database.

## Features

- **Face Recognition:** Utilizes the face_recognition library to recognize faces in real-time.
- **Background Modification:** Dynamically updates the background with the video feed and mode images.
- **Attendance Tracking:** Records attendance in an SQLite database with member details and attendance status.
- **Mode Switching:** Switches between different display modes for a better user experience.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/face-attendance-system.git
   cd face-attendance-system

2. Install the required dependencies:

  ```bash
  pip install opencv-python numpy face_recognition cvzone
  Download the required resources:

3. Download and place the background image in the "Resources" folder.
  Place mode images in the "Resources/Modes" folder.
  Ensure an encoding file (EncodeFile.p) is available.

## Usage
1. Run the script:

  ```bash
  python main.py
  The system will capture the live video feed, recognize faces, and update the attendance database.
  
  Press 'q' to exit the application.

## Configuration
Adjust the following constants in the script for customization:

** ENCODE_FILE_PATH: ** Path to the encoding file.
** BACKGROUND_IMAGE_PATH: ** Path to the background image.
** MODES_FOLDER_PATH: ** Path to the folder containing mode images.

## Database
The system uses an SQLite database to store attendance records. The database is initialized with a table named "attendance," including columns for id, datetime, member_id, member_name, and status.

## License
This project is licensed under the MIT License.

## Acknowledgments
OpenCV
face_recognition
cvzone
Feel free to contribute, report issues, or provide suggestions!
