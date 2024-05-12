import re


def convert_code_blocks(text):
    pattern = r"```(\w+)?\s*([^`]+?)```"

    def replace(match):
        language = match.group(1)
        code = match.group(2)
        if language:
            return f"<pre><code class=\"{language}\">{code.strip()}</code></pre>"
        else:
            return f"<pre><code>{code.strip()}</code></pre>"
    converted_text = re.sub(pattern, replace, text, flags=re.DOTALL)
    return converted_text


def convert_html_to_markdown(html_text):
    pattern = r"<pre><code(?: class=\"(\w+)\")?>(.*?)</code></pre>"

    def replace(match):
        language = match.group(1)
        code = match.group(2)
        if language:
            return f"```{language}\n{code.strip()}\n```"
        else:
            return f"```\n{code.strip()}\n```"

    converted_text = re.sub(pattern, replace, html_text, flags=re.DOTALL)
    return converted_text


def replace_newlines(md_text):
    code_blocks = re.findall(r"```.*?```", md_text, flags=re.DOTALL)
    non_code_blocks = re.split(r"```.*?```", md_text, flags=re.DOTALL)

    transformed_text = non_code_blocks[0].replace("\n", "<br>")
    for i in range(1, len(non_code_blocks)):
        transformed_part = non_code_blocks[i].replace("\n", "<br>")
        if i - 1 < len(code_blocks):
            transformed_text += convert_code_blocks(code_blocks[i - 1])
        transformed_text += transformed_part

    return transformed_text
