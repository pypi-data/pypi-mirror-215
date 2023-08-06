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

    def drop_first_frame(self):
        self.stream = self.stream.filter("select", "not(eq(n,0))")

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
