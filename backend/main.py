
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import os


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../frontend", html=True), name="static")

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

# --- Grocery Store ---
def process_grocery_store(file_path, result_path):
    polygon = np.array([
        [1725, 1550],
        [2725, 1550],
        [3500, 2160],
        [1250, 2160]
    ])
    zone = sv.PolygonZone(polygon=polygon)
    box_annotator = sv.BoxAnnotator(thickness=4)
    label_annotator = sv.LabelAnnotator(text_thickness=4, text_scale=2)
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4)
    cap = cv2.VideoCapture(file_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Robust fallback for invalid video properties
    if frame_width <= 0 or frame_height <= 0:
        ret, frame = cap.read()
        if ret:
            frame_height, frame_width = frame.shape[:2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if fps is None or fps <= 0:
        fps = 25.0
    out = cv2.VideoWriter(result_path, fourcc, fps, (frame_width, frame_height))
    total_count = 0
    logs = []
    last_frame = None
    frame_written = False
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        results = model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[detections.class_id == 0]
        zone.trigger(detections=detections)
        labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, _, confidence, class_id, _, _ in detections]
        frame = box_annotator.annotate(scene=frame, detections=detections)
        frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)
        frame = zone_annotator.annotate(scene=frame)
        if frame is not None:
            out.write(frame)
            frame_written = True
            last_frame = frame.copy()
        total_count += len(detections)
        log_str = f"{len(detections)} persons detected"
        logs.append(log_str)
    cap.release()
    out.release()
    # Remove result video if no frames were written
    if not frame_written and os.path.exists(result_path):
        os.remove(result_path)
    # Save inference image
    img_path = None
    if last_frame is not None:
        img_path = result_path.replace('.mp4', '_inference.jpg')
        cv2.imwrite(img_path, last_frame)
    return total_count, logs, img_path

# --- Subway ---
def process_subway(file_path, result_path):
    polygon = np.array([
        [200, 3840],
        [1300, 600],
        [1325, 600],
        [550, 3840]
    ])
    zone = sv.PolygonZone(polygon=polygon)
    box_annotator = sv.BoxAnnotator(thickness=4)
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4)
    cap = cv2.VideoCapture(file_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if frame_width <= 0 or frame_height <= 0:
        ret, frame = cap.read()
        if ret:
            frame_height, frame_width = frame.shape[:2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if fps is None or fps <= 0:
        fps = 25.0
    out = cv2.VideoWriter(result_path, fourcc, fps, (frame_width, frame_height))
    total_count = 0
    logs = []
    last_frame = None
    frame_written = False
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        results = model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[detections.class_id == 0]
        zone.trigger(detections=detections)
        frame = box_annotator.annotate(scene=frame, detections=detections)
        frame = zone_annotator.annotate(scene=frame)
        if frame is not None:
            out.write(frame)
            frame_written = True
            last_frame = frame.copy()
        total_count += len(detections)
        log_str = f"{len(detections)} persons detected"
        logs.append(log_str)
    cap.release()
    out.release()
    if not frame_written and os.path.exists(result_path):
        os.remove(result_path)
    # Save inference image
    img_path = None
    if last_frame is not None:
        img_path = result_path.replace('.mp4', '_inference.jpg')
        cv2.imwrite(img_path, last_frame)
    return total_count, logs, img_path

# --- Market Square ---
def process_market_square(file_path, result_path):
    colors = sv.ColorPalette.DEFAULT
    polygons = [
        np.array([
            [540,  985 ],
            [1620, 985 ],
            [2160, 1920],
            [1620, 2855],
            [540,  2855],
            [0,    1920]
        ], np.int32),
        np.array([
            [0,    1920],
            [540,  985 ],
            [0,    0   ]
        ], np.int32),
        np.array([
            [1620, 985 ],
            [2160, 1920],
            [2160,    0]
        ], np.int32),
        np.array([
            [540,  985 ],
            [0,    0   ],
            [2160, 0   ],
            [1620, 985 ]
        ], np.int32),
        np.array([
            [0,    1920],
            [0,    3840],
            [540,  2855]
        ], np.int32),
        np.array([
            [2160, 1920],
            [1620, 2855],
            [2160, 3840]
        ], np.int32),
        np.array([
            [1620, 2855],
            [540,  2855],
            [0,    3840],
            [2160, 3840]
        ], np.int32)
    ]
    zones = [sv.PolygonZone(polygon=polygon) for polygon in polygons]
    zone_annotators = [
        sv.PolygonZoneAnnotator(
            zone=zone,
            color=colors.by_idx(index),
            thickness=6,
            text_thickness=8,
            text_scale=4
        )
        for index, zone in enumerate(zones)
    ]
    box_annotators = [
        sv.BoxAnnotator(
            color=colors.by_idx(index),
            thickness=4,
        )
        for index in range(len(polygons))
    ]
    cap = cv2.VideoCapture(file_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if frame_width <= 0 or frame_height <= 0:
        ret, frame = cap.read()
        if ret:
            frame_height, frame_width = frame.shape[:2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if fps is None or fps <= 0:
        fps = 25.0
    out = cv2.VideoWriter(result_path, fourcc, fps, (frame_width, frame_height))
    total_count = 0
    logs = []
    last_frame = None
    frame_written = False
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        results = model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[(detections.class_id == 0) & (detections.confidence > 0.5)]
        frame_log = []
        for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
            mask = zone.trigger(detections=detections)
            detections_filtered = detections[mask]
            frame = box_annotator.annotate(scene=frame, detections=detections_filtered)
            frame = zone_annotator.annotate(scene=frame)
            frame_log.append(f"{len(detections_filtered)} persons in zone")
            total_count += len(detections_filtered)
        logs.append(", ".join(frame_log))
        if frame is not None:
            out.write(frame)
            frame_written = True
            last_frame = frame.copy()
    cap.release()
    out.release()
    if not frame_written and os.path.exists(result_path):
        os.remove(result_path)
    # Save inference image
    img_path = None
    if last_frame is not None:
        img_path = result_path.replace('.mp4', '_inference.jpg')
        cv2.imwrite(img_path, last_frame)
    return total_count, logs, img_path



from fastapi.responses import FileResponse
import time
import glob

def cleanup_old_files():
    """Clean up all temporary and result files"""
    for old_file in glob.glob("temp_*.*") + glob.glob("result_*.*"):
        try:
            os.remove(old_file)
        except:
            pass

# @app.on_event("startup")
# async def startup_event():
#     """Clean up on startup"""
#     cleanup_old_files()

@app.post("/upload/{video_type}")
async def upload_video(video_type: str, file: UploadFile = File(...)):
    import uuid
    
    # Clean up old files before processing new upload
    cleanup_old_files()
    
    file_ext = os.path.splitext(file.filename)[-1] or ".mp4"
    unique_id = str(uuid.uuid4())[:8]
    temp_path = f"temp_{unique_id}{file_ext}"
    result_path = f"result_{unique_id}{file_ext}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    count, logs, img_path = None, None, None
    if video_type == "grocery_store":
        count, logs, img_path = process_grocery_store(temp_path, result_path)
    elif video_type == "subway":
        count, logs, img_path = process_subway(temp_path, result_path)
    elif video_type == "market_square":
        count, logs, img_path = process_market_square(temp_path, result_path)
    else:
        os.remove(temp_path)
        return JSONResponse({"error": "Invalid video type"}, status_code=400)
    
    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    # Wait for file to be written and closed
    for _ in range(10):
        if os.path.exists(result_path) and os.path.getsize(result_path) > 0:
            break
        time.sleep(0.2)
    if not os.path.exists(result_path) or os.path.getsize(result_path) == 0:
        return JSONResponse({"error": "Result video not generated correctly."}, status_code=500)
    import base64
    image_data = None
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")
    # Serve video directly from backend
    from fastapi.responses import FileResponse
    video_url = f"/download/{os.path.basename(result_path)}" if os.path.exists(result_path) else None
    response = {"count": count, "logs": logs, "image": f"data:image/jpeg;base64,{image_data}" if image_data else None, "video_url": video_url, "video_filename": os.path.basename(result_path)}
    return JSONResponse(response)
# Robust video download endpoint
@app.get("/download/{video_name}")
def download_video(video_name: str):
    if not os.path.exists(video_name):
        return JSONResponse({"error": "Video not found."}, status_code=404)
    return FileResponse(video_name, media_type="video/mp4", filename=video_name)
