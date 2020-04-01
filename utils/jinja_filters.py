import re


discord_regex_to_html = [
    ("&lt;(a?):([^:]+):(\d+)&gt;", lambda g: f'<img class="emoji" src="https://cdn.discordapp.com/emojis/{g.group(3)}.{"gif" if g.group(1) else "png"}" alt="{g.group(2)}"/>'),
    ("```([a-z]*)\n([\s\S]*?)\n```", '<pre class="highlight"><code>\g<2></code></pre>')
]


def discord_to_html(input):
    temp_text = input

    for reg, result in discord_regex_to_html:
        new_data = re.sub(reg, result, temp_text)
        temp_text = new_data

    return temp_text


def match_url(input):
    finding = re.sub(
        "((http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?)",
        lambda g: f'<a class="link" href="{g.group(0)}" target="_blank">{g.group(0)}</a>',
        input
    )

    return finding
