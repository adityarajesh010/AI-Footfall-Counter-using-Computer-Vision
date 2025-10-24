# AI Footfall Counter using Computer Vision

AI-powered video footfall counting application using YOLOv8 for person detection and tracking in predefined zones.

## Important Note

This application uses zone-based detection with predefined polygon coordinates. **You must use the specific test videos provided below** as the zones are calibrated for these videos only.

## Test Videos (Required)

Download the test videos from Google Drive:

**All Videos Folder:** [https://drive.google.com/drive/folders/1fdfjB237R5CHkej_A7-A31xOd0vEEFdi?usp=drive_link](https://drive.google.com/drive/folders/1fdfjB237R5CHkej_A7-A31xOd0vEEFdi?usp=drive_link)

**Individual Videos:**
- **Grocery Store:** [Download Video](https://drive.google.com/file/d/1bbnGeOpsKlXq--6WW5uJqwCfuH-QFUAe/view?usp=drive_link)
- **Market Square:** [Download Video](https://drive.google.com/file/d/1J1aH3KdruJFXLiiRGg2HwR925Adqhv3z/view?usp=drive_link)
- **Subway:** [Download Video](https://drive.google.com/file/d/1HzbU-OumykCLCCC_n8Nw6V6_ZfAzCOA7/view?usp=drive_link)

## Prerequisites

Before starting, ensure you have:
- Python 3.10 or higher installed
- Git installed
- Internet connection (for downloading YOLOv8 model on first run)

## Step-by-Step Installation

### Step 1: Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/adityarajesh010/AI-Footfall-Counter-using-Computer-Vision.git
cd AI-Footfall-Counter-using-Computer-Vision
```

### Step 2: Install Required Dependencies

Navigate to the backend folder and install all required packages:

```bash
cd backend
pip install fastapi uvicorn opencv-python numpy ultralytics supervision python-multipart
```

**Package Details:**
- `fastapi` - Web framework for the API
- `uvicorn` - ASGI server to run the application
- `opencv-python` - Video processing and computer vision
- `numpy` - Numerical operations for arrays
- `ultralytics` - YOLOv8 model for person detection
- `supervision` - Detection utilities and zone tracking
- `python-multipart` - File upload support

### Step 3: Download Test Videos

Before running the application, download the test videos from the links provided above. Save them in a location you can easily access.

## Running the Application

### Step 1: Start the Backend Server

From the backend directory, run:

```bash
python -m uvicorn main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Open the Application in Browser

Open your web browser and navigate to:

```
http://localhost:8000/static/index.html
```

### Step 3: Upload and Process Videos

1. Select the video type from the dropdown:
   - Market Square
   - Grocery Store
   - Subway

2. Click "Choose File" and select the corresponding test video you downloaded

3. Click the "Upload" button

4. Wait for processing (this may take a few minutes depending on video length)

5. Once complete, you will see:
   - Total person count
   - "Download Video" button to get the annotated result

## How It Works

### Detection Process

1. **Video Upload:** Selected video is uploaded to the FastAPI backend
2. **Frame Processing:** Each frame is processed using YOLOv8 for person detection
3. **Zone Tracking:** Detected persons are tracked within predefined polygon zones
4. **Annotation:** Bounding boxes and zone overlays are drawn on frames
5. **Output Generation:** Annotated video is saved with a unique ID
6. **Download:** Processed video is available for download

### Zone Configurations

**Market Square:**
- 7 different polygonal zones covering various areas
- Multi-zone tracking with color-coded annotations
- Confidence threshold: 0.5

**Grocery Store:**
- Single zone focusing on the checkout/main area
- Includes confidence scores on detection labels
- Detailed bounding box annotations

**Subway:**
- Vertical corridor zone for tracking movement
- Simplified annotation for clear visualization
- Tracks people passing through defined area

## Project Structure

```
AI-Footfall-Counter-using-Computer-Vision/
├── backend/
│   └── main.py              # FastAPI application with all endpoints
├── frontend/
│   ├── index.html           # User interface
│   └── progress.js          # Upload and progress handling
└── README.md                # This file
```

## Understanding the Results

### Person Count

The count displayed represents **total detections across all frames**, not unique individuals.

**Example:**
- Video with 150 frames
- 30 people detected per frame
- Total count = 150 × 30 = 4,500 detections

This is cumulative detection count, useful for understanding overall traffic/activity.

## Troubleshooting

### Server Won't Start

**Check Python version:**
```bash
python --version
```
Should be 3.10 or higher.

**Check if port 8000 is in use:**
- Close any other applications using port 8000
- Or change the port: `python -m uvicorn main:app --reload --port 8001`

**Reinstall dependencies:**
```bash
pip install --upgrade fastapi uvicorn opencv-python numpy ultralytics supervision python-multipart
```

### Video Upload Fails

- Ensure the video file is in MP4 format
- Check that the backend server is running (terminal should show "Application startup complete")
- Try a smaller video file first to test
- Verify you downloaded the correct test video from Google Drive

### Processing Takes Too Long

- Processing time depends on video length and your computer's performance
- Typical processing: 1-3 minutes for a 30-second video
- YOLOv8s inference takes ~280ms per frame
- Be patient and do not refresh the page during processing

### Download Button Not Appearing

- Wait until processing is 100% complete
- Check browser console for errors (F12)
- Ensure the backend didn't crash (check terminal for errors)
- Try uploading again

### 404 Error on Download

- Do not restart the server after processing
- Result files are automatically cleaned up on next upload
- If you need the file again, reprocess the video

## API Endpoints

### POST /upload/{video_type}

Upload and process a video.

**Parameters:**
- `video_type` - One of: `market_square`, `grocery_store`, `subway`

**Body:**
- Multipart form data with video file

**Response:**
```json
{
  "count": 4500,
  "logs": ["10 persons detected", "12 persons detected", ...],
  "image": "data:image/jpeg;base64,...",
  "video_url": "/download/result_abc123.mp4",
  "video_filename": "result_abc123.mp4"
}
```

### GET /download/{video_name}

Download a processed video.

**Parameters:**
- `video_name` - Filename of the result video

**Response:**
- Video file (MP4 format)

## Features

- Real-time person detection using YOLOv8
- Multi-zone polygon-based tracking
- Automatic file cleanup on new uploads
- Unique filename generation for results
- Single-server architecture (no CORS issues)
- Progress indication during upload
- Annotated video output with bounding boxes and zones

## Technical Details

- **Model:** YOLOv8s (automatically downloaded on first run)
- **Input Resolution:** 1280px (for inference)
- **Video Codec:** MP4V for output videos
- **Detection Class:** Person (class_id = 0)
- **Framework:** FastAPI + Uvicorn
- **Frontend:** HTML + JavaScript + Bootstrap

## Important Limitations

1. **Zone-Specific:** The polygon zones are hardcoded for the provided test videos only
2. **Not Real-Time:** Processing happens after upload, not during streaming
3. **Cumulative Count:** Total detections, not unique person tracking
4. **Single Video:** Can only process one video at a time

## License

This project is open source and available for educational purposes.

## Credits

- YOLOv8 by Ultralytics
- Supervision library by Roboflow
- FastAPI by Sebastián Ramírez
