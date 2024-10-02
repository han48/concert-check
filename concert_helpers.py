import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips


def bright_max(input):
    results = list()
    for threshold in range(0, 255):
        # Đọc ảnh
        image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
        # Tạo mặt nạ cho các điểm sáng
        _, bright_points = cv2.threshold(
            image, threshold, 255, cv2.THRESH_BINARY)
        # Tìm các đường viền (contours) của các cụm sáng
        contours, _ = cv2.findContours(
            bright_points, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Đếm số cụm sáng
        num_clusters = len(contours)
        print(f'{threshold}: {num_clusters}')
        results.append(num_clusters)
    max_value = max(results)
    max_index = results.index(max_value)
    print(f'{max_index}: {max_value}')
    return max_index, max_value


audio = 'audio/is-epical.mp3'


def create_video_counter(input, input2):
    output_counter = input + '.counter.mp4'
    output = input + '.mp4'
    # Đọc ảnh
    image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)

    # Ngưỡng để xác định điểm sáng
    threshold, max_count = bright_max(input)

    # Tạo mặt nạ cho các điểm sáng
    _, bright_points = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Tìm các đường viền (contours) của các cụm sáng
    contours, _ = cv2.findContours(
        bright_points, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Đếm số cụm sáng
    num_clusters = len(contours)

    print(f'Bright count: {num_clusters}')

    # Thiết lập video writer
    height, width = image.shape
    video_writer = cv2.VideoWriter(
        output_counter, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    oimage = cv2.imread(input2)
    # Vẽ contour và ghi vào video
    for i in range(1, 30):
        video_writer.write(oimage)
    oimage = cv2.imread(input)
    # Vẽ contour và ghi vào video
    for i in range(1, 30):
        video_writer.write(oimage)
    for i, contour in enumerate(contours):
        frame = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, f'Point {i+1}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        video_writer.write(frame)

    video_writer.release()
    # Chèn nhạc vào video
    video_clip = VideoFileClip(output_counter)
    audio_clip = AudioFileClip(audio)

    # Lặp lại audio để khớp với độ dài video
    audio_duration = audio_clip.duration
    video_duration = video_clip.duration
    repeated_audio_clips = []

    while sum([clip.duration for clip in repeated_audio_clips]) < video_duration:
        repeated_audio_clips.append(audio_clip)

    final_audio_clip = concatenate_audioclips(
        repeated_audio_clips).subclip(0, video_duration)
    final_clip = video_clip.set_audio(final_audio_clip)
    final_clip.write_videofile(output, codec='libx264', audio_codec='aac')

    cv2.destroyAllWindows()
