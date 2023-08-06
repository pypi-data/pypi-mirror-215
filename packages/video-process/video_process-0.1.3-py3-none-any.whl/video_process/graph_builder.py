import ffmpeg


class GraphBuilder:
    def __init__(self, input_file):
        self.input_file = input_file
        self.stream = ffmpeg.input(input_file, vcodec="libvpx-vp9")
        self.audio = self.stream.audio
        self.video_info = ffmpeg.probe(input_file)["streams"][0]
        self.width = int(self.video_info["width"])
        self.height = int(self.video_info["height"])
        print(self.width, self.height)

    def scale_overlay(self, xpos=0.0, ypos=0.0, scale=1.0):
        w_overlay = int(self.width * xpos)
        h_overlay = int(-self.height * ypos)
        iw, ih = trunc_for_wh(self.width, self.height, scale)
        w_overlay += -int((iw - self.width) / 2)
        h_overlay += -int(ih - self.height)
        self.scale(iw, ih)
        return w_overlay, h_overlay

    def scale(self, width, height):
        self.stream = self.stream.filter("scale", width=width, height=height)

    def overlay(self, x, y):
        self.stream = self.stream.filter("pad", width="iw", height="ih", x=x, y=y)

    def add_bg(self, bg, x, y):
        if bg["bg_type"] == "video":
            bg_video = ffmpeg.input(bg["bg_video_path"])
            bg_video = bg_video.filter(
                "scale",
                width=self.width,
                height=self.height,
                force_original_aspect_ratio="decrease",
            )
            self.stream = ffmpeg.overlay(bg_video, self.stream, x=x, y=y)
        elif bg["bg_type"] == "image":
            bg_image = ffmpeg.input(bg["bg_image_path"])
            bg_image = bg_image.filter(
                "scale",
                width=self.width,
                height=self.height,
                force_original_aspect_ratio="decrease",
            )
            self.stream = ffmpeg.overlay(bg_image, self.stream, x=x, y=y)

    def add_overlay(self, layer):
        if layer["type"] == "image":
            overlay = ffmpeg.input(layer["layer_path"])
            self.stream = self.stream.overlay(overlay, x=layer["x"], y=layer["y"])
        elif layer["type"] == "sticker":
            overlay = ffmpeg.input(layer["layer_path"], **{"ignore_loop": "0"})
            self.stream = self.stream.overlay(
                overlay,
                x=layer["x"],
                y=layer["y"],
                shortest=1,
            )

    def add_bg_music(self, bg_music):
        bg_audio = (
            ffmpeg.input(
                bg_music["bg_music_path"],
                stream_loop=-1,
            )
            .audio.filter("volume", bg_music["bg_music_volume"])
            .filter("afade", t="in", st=bg_music["bg_music_st"], d=1)
            .filter("afade", t="out", st=bg_music["bg_music_et"], d=1)
            .filter("atrim", duration=bg_music["bg_music_et"])
        )
        self.audio = ffmpeg.filter([self.audio, bg_audio], "amix", inputs=2)

    def add_subtitle(self, subtitle_path):
        self.stream = self.stream.filter("ass", subtitle_path)

    def build(self, result_path="out.mp4"):
        return ffmpeg.output(
            self.stream,
            self.audio,
            result_path,
            pix_fmt="yuv420p",
        ).overwrite_output()

    def run(self, command):
        command.run(cmd="ffmpeg")
        import shlex

        command = command.compile()
        escaped_command = [shlex.quote(arg) for arg in command]
        print(" ".join(escaped_command))

    def show_graph(self, graph_detail=False):
        ffmpeg.view(self.stream, detail=graph_detail, filename="graph")


def trunc_for_wh(w, h, scale=1.0):
    tw = int(w * scale)
    th = int(h * scale)
    if tw % 2 != 0:
        tw += 1
    if th % 2 != 0:
        th += 1
    return tw, th


if __name__ == "__main__":
    input_file = "sample_data/ing.webm"

    layers = [
        {
            "type": "image",
            "index": 0,
            "layer_path": "sample_data/overlay.png",
            "x": 0,
            "y": 0,
        },
        {
            "type": "image",
            "index": 1,
            "layer_path": "sample_data/overlay1.jpg",
            "x": 100,
            "y": 100,
        },
        {
            "type": "sticker",
            "index": 2,
            "layer_path": "sample_data/sticker.gif",
            "x": 100,
            "y": 0,
        },
    ]
    layers = sorted(layers, key=lambda x: x["index"])

    bg_music = {
        "bg_music_path": "sample_data/bg_music.mp3",
        "bg_music_volume": 0.9,
        "bg_music_st": 1,
        "bg_music_et": 8,
        "bg_music_loop": True,
    }

    bg = {
        "bg_type": "image",
        "bg_image_path": "sample_data/bg_image.jpg",
        "bg_video_path": "sample_data/bg_video.mp4",
    }

    input_srt_file = "sample_data/subtitle.srt"
    output_ass_file = "sample_data/tmp_subtitle.ass"
    from subtitle import convert_to_ass, change_style

    convert_to_ass(input_srt_file, output_ass_file)

    style = dict(
        fontName="Arial",
        fontSize=30,
        angle=0,
        scaleX=50,
        scaleY=50,
    )

    subtitle_path = "sample_data/subtitle.ass"
    change_style(output_ass_file, subtitle_path, style)

    xpos = -0.5
    ypos = 0.5
    scale = 2.0
    graph_builder = GraphBuilder(input_file)
    x, y = graph_builder.scale_overlay(xpos, ypos, scale)
    graph_builder.add_bg(bg, x, y)
    graph_builder.add_overlay(layers[0])
    graph_builder.add_overlay(layers[1])
    graph_builder.add_overlay(layers[2])
    graph_builder.add_bg_music(bg_music)
    graph_builder.add_subtitle(subtitle_path)
    command = graph_builder.build()
    graph_builder.run(command)
    graph_builder.show_graph()
