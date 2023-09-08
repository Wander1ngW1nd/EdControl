import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


import cv2
import numpy as np
import polars as pl
from attrs import define, field
from deepface import DeepFace


class VideoInputException(IOError):
    pass


@define(slots=True, auto_attribs=True)
class VideoEmotionRecognizer:
    filepath: str
    _analyzed_frames: pl.DataFrame = field(init=False)

    def __attrs_post_init__(self):
        self._analyzed_frames = self._analyze()

    def _analyze(self) -> pl.DataFrame:
        cap: cv2.VideoCapture = cv2.VideoCapture(self.filepath)
        if cap.isOpened() == False:
            raise VideoInputException("Video opening error")

        analyzed_frames_data: dict = {"timestamp": [], "emotion": [], "probability": []}
        while cap.isOpened():
            return_flag: bool
            frame: np.ndarray
            return_flag, frame = cap.read()
            if return_flag:
                result = DeepFace.analyze(
                    frame, actions="emotion", enforce_detection=False, silent=True
                )[0]
                analyzed_frames_data["timestamp"] += [
                    cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                ] * len(result["emotion"].keys())
                analyzed_frames_data["emotion"] += list(
                    map(str, result["emotion"].keys())
                )
                analyzed_frames_data["probability"] += list(
                    map(float, result["emotion"].values())
                )
            else:
                raise VideoInputException("No video frame returned")

        return pl.DataFrame(analyzed_frames_data)

    def emotions_summary(self) -> dict:
        emotions_summary: pl.DataFrame = (
            self._analyzed_frames.groupby("emotion")
            .agg(pl.col("probability").sum())
            .sort("probability", descending=True)
        )

        emotions_summary = emotions_summary.with_columns(
            (pl.col("probability") / pl.sum("probability")).alias("probability")
        )

        output: dict = dict(
            zip(
                emotions_summary["emotion"].to_list(),
                emotions_summary["probability"].to_list(),
            )
        )

        return output
