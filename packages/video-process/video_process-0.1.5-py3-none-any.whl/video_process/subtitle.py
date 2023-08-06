import ffmpeg


def convert_to_ass(input_srt_file, output_ass_file):
    ffmpeg.input(input_srt_file).output(
        output_ass_file, format="ass"
    ).overwrite_output().run()


def change_style(input_srt_file, output_ass_file, style):
    import pyass

    tmp_ass_file = "/tmp/tmp.ass"
    convert_to_ass(input_srt_file, tmp_ass_file)

    new_style = pyass.Style()

    for key, value in style.items():
        setattr(new_style, key, value)

    with open(tmp_ass_file, encoding="utf_8_sig") as f:
        script = pyass.load(f)

    script.styles[0] = new_style
    with open(output_ass_file, "w", encoding="utf_8_sig") as f:
        pyass.dump(script, f)


if __name__ == "__main__":
    input_srt_file = "sample_data/subtitle.srt"
    output_ass_file = "sample_data/ing.ass"
    # name: str = "Default"
    # fontName: str = "Arial"
    # fontSize: int = 48
    # primaryColor: = "&H000000FF"
    # secondaryColor:
    # outlineColor:
    # backColor:
    # isBold: bool = False
    # isItalic: bool = False
    # isUnderline: bool = False
    # isStrikeout: bool = False
    # scaleX: int = 100
    # scaleY: int = 100
    # spacing: int = 0
    # angle: float = 0.0
    # borderStyle: BorderStyle
    # outline: float = 2.0
    # shadow: float = 2.0
    # alignment: Alignment
    # marginL: int = 10
    # marginR: int = 10
    # marginV: int = 10
    # encoding: int = 1

    # class BorderStyle(Enum):
    #     BORDER_STYLE_OUTLINE_DROP_SHADOW = 1
    #     BORDER_STYLE_OPAQUE_BOX = 3

    # class Alignment(Enum):
    #     TOP_LEFT = 7
    #     TOP = 8
    #     TOP_RIGHT = 9
    #     CENTER_LEFT = 4
    #     CENTER = 5
    #     CENTER_RIGHT = 6
    #     BOTTOM_LEFT = 1
    #     BOTTOM = 2
    #     BOTTOM_RIGHT = 3
    style = {
        "Name": "Default",
        "fontName": "Arial",
        "fontSize": 13,
        "primaryColor": "&H000000FF",
    }

    change_style(input_srt_file, output_ass_file, style)
