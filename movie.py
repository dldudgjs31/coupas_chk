import moviepy.editor as mp
from moviepy.video.VideoClip import TextClip
import requests
from PIL import Image
from io import BytesIO
# print(TextClip.list('font'))
import numpy as np


video = mp.VideoFileClip("background.mp4")

## TextClip에서 size 통해서 Width를 먼저 정한다.
# subtitle = mp.TextClip("안녕하세요", fontsize=70, color='black', font='Malgun-Gothic-Bold', size=(50, None))


# titles = [
#     {"text": "첫 번째 타이틀", "start_time": 5, "end_time": 10},  # 5초부터 10초까지
#     {"text": "두 번째 타이틀", "start_time": 15, "end_time": 20},  # 15초부터 20초까지
#     # 필요한 만큼 추가 가능
# ]
#
# # 각 타이틀에 대한 TextClip 만들기
# text_clips = []
# for title_info in titles:
#     subtitle = mp.TextClip(title_info["text"], fontsize=70, color='black', font='Malgun-Gothic-Bold', size=(200, None))
#     subtitle = subtitle.set_position((30, 100))
#     subtitle = subtitle.set_start(title_info["start_time"]).set_end(title_info["end_time"])
#     subtitle = subtitle.set_duration(title_info["end_time"] - title_info["start_time"])  # 지속 시간 수정
#     text_clips.append(subtitle)
#
# # 비디오에 타이틀 삽입
# video_with_subtitles = mp.CompositeVideoClip([video] + text_clips)
#
# video_with_subtitles.write_videofile("자막추가된동영상.mp4")


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Failed to download the image.")
        return None


# 비디오 파일 로드
video = mp.VideoFileClip("background.mp4")

# 타이틀 및 시간 설정
titles = [
    {"text": "첫 번째 타이틀", "start_time": 5, "end_time": 10},  # 5초부터 10초까지
    {"text": "두 번째 타이틀", "start_time": 15, "end_time": 20},  # 15초부터 20초까지
    # 필요한 만큼 추가 가능
]

# 각 타이틀에 대한 TextClip 및 ImageClip 만들기
clips = []
for title_info in titles:
    # 텍스트 생성
    text_clip = mp.TextClip(title_info["text"], fontsize=70, color='black', font='Malgun-Gothic-Bold')
    text_clip = text_clip.set_position((30, 100))
    text_clip = text_clip.set_start(title_info["start_time"]).set_end(title_info["end_time"])
    text_clip = text_clip.set_duration(title_info["end_time"] - title_info["start_time"])  # 지속 시간 수정

    # 이미지 다운로드
    image_url = "https://img4a.coupangcdn.com/image/vendor_inventory/7d7b/5a607714d81cf2f17a2ae230eabe8f3164b2861895468a6657e6c6c5c155.jpg"
    image = download_image(image_url)
    if image:
        # 이미지를 100x100 크기로 리사이징하고 numpy 배열로 변환
        image.thumbnail((300, image.size[1]))
        image_array = np.array(image)
        # 이미지를 ImageClip으로 변환
        image_clip = mp.ImageClip(image_array)
        # 이미지를 오른쪽 아래로 배치
        image_clip = image_clip.set_position(("right", "bottom"))
        image_clip = image_clip.set_start(title_info["start_time"]).set_end(title_info["end_time"])
        image_clip = image_clip.set_duration(title_info["end_time"] - title_info["start_time"])  # 지속 시간 수정

        clips.append(image_clip)

    clips.append(text_clip)

# 비디오에 타이틀 삽입
video_with_subtitles = mp.CompositeVideoClip([video]+clips)

# 결과 비디오 저장
video_with_subtitles.write_videofile("자막_이미지_동영상.mp4",fps=60)


#
# subtitle = subtitle.set_position((30,100)).set_duration(video.duration)
#
# video_with_subtitle = mp.CompositeVideoClip([video, subtitle])
#
# video_with_subtitle.write_videofile("자막추가된동영상.mp4")