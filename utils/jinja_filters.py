import re


def discord_to_html(input):
    temp_text = input
    discord_emoji = "(<|&lt;)(a?):([^:]+):(\d+)(&gt;|>)"

    test_data = re.sub(discord_emoji, "", temp_text)
    add_jumbo = "" if test_data else " jumboable"

    new_data = re.sub(discord_emoji, lambda g: f'<img class="emoji{add_jumbo}" src="https://cdn.discordapp.com/emojis/{g.group(4)}.{"gif" if g.group(2) else "png"}" alt="{g.group(3)}"/>', temp_text)
    temp_text = new_data

    new_data = re.sub("\`\`\`([a-z]*)\n([\s\S]*?)(|\n)\`\`\`", '<pre class="highlight"><code>\g<2></code></pre>', temp_text)
    temp_text = new_data

    return temp_text


def match_url(input):
    temp_input = input.replace("&lt;", "<").replace("&gt;", ">")

    finding = re.sub(
        "((http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?)",
        lambda g: f'<a class="link" href="{g.group(0)}" target="_blank">{g.group(0)}</a>',
        temp_input
    )

    return finding


def detect_file(file):
    image = ["jpeg", "jpg", "png", "gif"]
    video = ["mp4"]
    music = ["mp3"]
    file_ext = file["filename"].split(".")[-1]
    if file_ext in image:
        return f'<div class="image-container"><img class="upload" src="{file["content"]}" alt="{file["filename"]}" data-enlargable></div>'
    elif file_ext in video:
        return f'<div class="video-container"><video class="upload" width="420" controls><source src="{file["content"]}" type="video/mp4"></video></div>'
    elif file_ext in music:
        return f'<div class="music-container"><audio controls><source src="{file["content"]}" type="audio/mpeg"></audio></div>'
    else:
        return f'<div class="file-container"><a class="upload" href="{file["content"]}" alt="{file["filename"]}">📂 {file["filename"]}</a></div>'
