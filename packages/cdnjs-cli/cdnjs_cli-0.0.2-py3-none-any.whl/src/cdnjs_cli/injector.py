# SPDX-FileCopyrightText: 2023-present woidzero <woidzeroo@gmail.com>
#
# SPDX-License-Identifier: MIT


def inject(file, content):
    with open(file, "w") as f:
        f.writelines(content)


def add(src, file):
    with open(file, "r") as f:
        content = f.readlines()

    tag = f"<script src='{src}'></script>"
    body_end_index = -1

    for i, line in enumerate(content):
        if line.strip() == "</body>":
            body_end_index = i
            break
        elif line.strip() == "<body></body>":
            content[i] = "<body>\n\n</body>\n"
            inject(file, content)
            add(src, file=file)
            return

    if body_end_index == -1:
        raise ValueError("The HTML file does not contain a closing </body> tag.")

    previous_line_indentation = ""

    if body_end_index > 0:
        previous_line = content[body_end_index - 1]
        if previous_line.strip() != "":
            previous_line_indentation = previous_line[: len(previous_line) - len(previous_line.lstrip())]
    if previous_line_indentation == "":
        previous_line_indentation = "\t"

    tag = previous_line_indentation + tag + "\n"

    content.insert(body_end_index, tag)

    inject(file, content)
