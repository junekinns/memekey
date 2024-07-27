import random
import base64


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def add_emoji(text):
    emoji_dict = {
        'Title': ['🎵', '🎶', '🎸', '🎤'],
        'Lyrics': ['🗣️', '📢', '🎼'],
        'Word': ['📖', '💬', '🔤'],
        'Definition': ['📚', '🧠', '💡'],
        'Read': ['👀', '👁️', '🔍'],
        'confidence': ['💪', '🦾', '🏋️'],
        'cool': ['😎', '🆒', '👌'],
        'awesome': ['🤩', '🌟', '💯'],
        'love': ['❤️', '💖', '😍'],
        'happy': ['😊', '😄', '🙂'],
        'sad': ['😢', '😞', '😔'],
        'angry': ['😠', '😡', '🤬'],
        'surprise': ['😮', '😲', '🤯'],
        'work': ['💼', '👨‍💼', '👩‍💼'],
        'music': ['🎵', '🎶', '🎹'],
        'dance': ['💃', '🕺', '🩰'],
    }

    for key, emojis in emoji_dict.items():
        if key.lower() in text.lower():
            return f"{random.choice(emojis)} {text}"
    return f"{text}"  # 기본 이모지


def format_response(text):
    lines = text.split('\n')
    formatted_lines = []

    for line in lines:
        if line.startswith('Title:'):
            line = f'<b>{line}</b>'
        elif line.startswith('Word:') or line.startswith('Definition:'):
            line = f'<b>{line}</b>'
        elif line.startswith('Lyrics:'):
            line = f'<i>{line}</i>'

        line = add_emoji(line)
        formatted_lines.append(line)

    return '<br>'.join(formatted_lines)
