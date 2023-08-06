import ffmpeg


def convert_to_ass(input_srt_file, output_ass_file):
    ffmpeg.input(input_srt_file).output(
        output_ass_file, format="ass"
    ).overwrite_output().run()


def change_style(input_ass_file, output_ass_file, style):
    import pyass

    new_style = pyass.Style()

    for key, value in style.items():
        setattr(new_style, key, value)

    with open(input_ass_file, encoding="utf_8_sig") as f:
        script = pyass.load(f)

    script.styles.append(new_style)
    with open(output_ass_file, "w", encoding="utf_8_sig") as f:
        pyass.dump(script, f)
