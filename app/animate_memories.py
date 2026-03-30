import cv2
import os
import json
import numpy as np
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, AudioFileClip
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_BASE = os.path.join(SCRIPT_DIR, "..", "photos")
if not os.path.isdir(PHOTOS_BASE):
    PHOTOS_BASE = "/home/eberrik/app/photos"

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "assets")
CARTOON_DIR = os.path.join(OUTPUT_DIR, "cartoon_photos")
VIDEO_OUTPUT = os.path.join(OUTPUT_DIR, "our_cartoon_story.mp4")
DURATION_PER_IMAGE = 4
TARGET_SIZE = (1280, 720)

TIMELINE_CAPTIONS = {
    "2nd April, 2025 (our 1st meet)": "Our 1st Meet — April 2, 2025",
    "4th April, 2025 (Random meet)": "Random Meet — April 4, 2025",
    "7th April, 2025 (Random meet)": "Random Meet — April 7, 2025",
    "8th April, 2025 (our 1st Shopping)": "Our 1st Shopping — April 8, 2025",
    "11th April, 2025 (Random meet)": "Random Meet — April 11, 2025",
    "12th April, 2025 (Kalighat)": "Kalighat — April 12, 2025",
    "1st May, 2025 (Our 1st Month Anniversery)": "1st Month Anniversary — May 1, 2025",
    "4th May, 2025 (She came to my home 1st time)": "She Came to My Home — May 4, 2025",
    "6th May, 2025 (Random meet)": "Random Meet — May 6, 2025",
    "18th May, 2025 (Her Parents came to my Place 1st time)": "Her Parents Visited — May 18, 2025",
    "28th May, 2025 (i went to her place 1st time)": "I Went to Her Place — May 28, 2025",
    "8th June, 2025 (my parents went to her place 1st time)": "My Parents Visited Her — June 8, 2025",
    "14th June, 2025 (1st Movie date)": "1st Movie Date — June 14, 2025",
    "24th June, 2025 (Belurmath)": "Belurmath — June 24, 2025",
    "25th June, 2025 (Ecopark)": "Ecopark — June 25, 2025",
    "26th Sept, 2025 (1st Durga Puja Pandal Hopping)": "1st Pandal Hopping — Sept 26, 2025",
    "28th Sept, 2025 (2nd day of Durga Puja)": "Durga Puja Day 2 — Sept 28, 2025",
    "2nd Oct, 2025 (at her place Durga Puja)": "Durga Puja at Her Place — Oct 2, 2025",
}

os.makedirs(CARTOON_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def cartoonify(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    img = cv2.resize(img, TARGET_SIZE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)


def make_typewriter_clip(full_text, duration):
    try:
        txt = TextClip(
            full_text,
            fontsize=32,
            color="white",
            font="DejaVu-Sans-Mono-Bold",
            bg_color="rgba(0,0,0,0.6)",
            size=(TARGET_SIZE[0] - 40, None),
            method="caption",
        )
        return txt.set_duration(duration).set_position(("center", "bottom"))
    except Exception:
        return None


def main():
    print("🚀 Starting Cartoon Transformation Pipeline...")
    exts = (".jpg", ".jpeg", ".png", ".webp")
    clips = []

    for folder_name, caption in TIMELINE_CAPTIONS.items():
        folder_path = os.path.join(PHOTOS_BASE, folder_name)
        if not os.path.isdir(folder_path):
            continue

        photos = sorted(
            f for f in os.listdir(folder_path) if f.lower().endswith(exts)
        )
        if not photos:
            continue

        print(f"📂 Processing: {folder_name} ({len(photos)} photos)")

        for photo in photos:
            img_path = os.path.join(folder_path, photo)
            cartoon_rgb = cartoonify(img_path)
            if cartoon_rgb is None:
                continue

            save_name = f"{folder_name}_{photo}"
            for ch in [",", "(", ")", " "]:
                save_name = save_name.replace(ch, "_")
            save_path = os.path.join(CARTOON_DIR, save_name)
            cv2.imwrite(
                save_path, cv2.cvtColor(cartoon_rgb, cv2.COLOR_RGB2BGR)
            )

            img_clip = ImageClip(cartoon_rgb).set_duration(DURATION_PER_IMAGE)
            txt_clip = make_typewriter_clip(caption, DURATION_PER_IMAGE)

            if txt_clip:
                final = CompositeVideoClip([img_clip, txt_clip.set_start(0.5)])
            else:
                final = img_clip

            clips.append(final.crossfadein(0.8).crossfadeout(0.8))
            print(f"  ✅ {photo}")

    if not clips:
        print("❌ No photos found! Add photos to the date folders first.")
        return

    print(f"🎬 Stitching {len(clips)} frames into video...")
    final_video = concatenate_videoclips(clips, method="compose")

    bg_music = os.path.join(OUTPUT_DIR, "background_music.mp3")
    if os.path.isfile(bg_music):
        audio = AudioFileClip(bg_music).subclip(0, final_video.duration)
        final_video = final_video.set_audio(audio)
        print("🎵 Background music added!")

    final_video.write_videofile(VIDEO_OUTPUT, fps=24, codec="libx264")
    print(f"✨ SUCCESS: Video saved to {VIDEO_OUTPUT}")


if __name__ == "__main__":
    main()
