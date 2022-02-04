from nanoid import generate
import random
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

if API_URL == "http://localhost:8000":
    os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'

COLORS = (
    '#F44336',
    '#E91E63',
    '#9C27B0',
    '#673AB7',
    '#3F51B5',
    '#2196F3',
    '#03A9F4',
    '#00BCD4',
    '#009688',
    '#4CAF50',
    '#8BC34A',
)


def get_initials(text):
    words = text.split(" ")

    initials = [word[0] for word in words]

    return "".join(initials)


AVATAR_SVG_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">
  <rect width="100%" height="100%" fill="{color}" />
   <text text-anchor="middle" y="50%" x="50%" dy="0.35em" fill="#fff" font-family="sans-serif" font-size="500">{initials}</text>
</svg>

""".strip()


def create_avatar(name):
    from cairosvg import svg2png

    svg = AVATAR_SVG_TEMPLATE.format(color=random.choice(COLORS), initials=get_initials(name))

    file_path = f"avatars/{generate()}.png"

    svg2png(bytestring=svg, write_to=file_path)

    return f"{API_URL}/{file_path}"
