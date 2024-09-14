# app/utils/video_processing.py

from moviepy.editor import VideoFileClip

# def convert_video_to_gif(input_input_video_path: str, output_gif_path: str):
#     clip = VideoFileClip(input_video_path)
#     clip.write_gif(output_gif_path)
#     clip.close()


def convert_video_to_gif(input_video_path: str, output_gif_path: str, gif_duration: int = 5):
    clip = VideoFileClip(input_video_path)
    video_duration = clip.duration
    gifs = []
    
    # Create GIFs in chunks of gif_duration
    for start in range(0, int(video_duration), gif_duration):
        end = min(start + gif_duration, video_duration)
        gif_clip = clip.subclip(start, end)
        gif_file = f"{output_gif_path}/gif_{start}_{end}.gif"
        gif_clip.write_gif(gif_file)
        gifs.append(gif_file)
        # break
    
    return gifs
