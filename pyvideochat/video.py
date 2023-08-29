# video.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of pyvideochat and is released under
# the MIT License: https://opensource.org/license/mit/

import cv2
import numpy
from .utils import _Logger

FULLSCREEN = 'fullscreen'

class Video(cv2.VideoCapture):
    def __init__(self, win_name, source, resolution:tuple=(640, 480), verbose:bool=False) -> None:
        """
        OpenCV-Python video implementation and tools

        Parameters
        ----------
        win_name: str, optional
            name of the Socket, by default 'Server'
        source : int, optional
            set camera index, by default 0
        resolution : tuple[int, int], optional
            resolution of the video window, pass pyvideochat.FULLSCREEN to set fullscreen mode, by default (640, 480)
        verbose : bool, optional
            get more output, by default False
        """
        self.win_name = win_name
        self.source = source
        self.verbose = verbose
        self.resolution = resolution
        try:
            if self.verbose:
                _Logger.text("Initializing OpenCV...")
            super().__init__(self.source)
            if self.resolution == 'fullscreen':
                self._set_fullscreen()
            if self is None or not self.isOpened():
                _Logger.error(f"Unable to open video source: {self.source}")
                exit()
            if self.verbose:
                _Logger.success(f"OpenCV inizialized!")
        except Exception as error:
            raise(error)

    def _set_fullscreen(self):
        cv2.namedWindow(f"{self.win_name} pyvideochat", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(f"{self.win_name} pyvideochat", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def show(self, frame:numpy.ndarray) -> None:
        """
        Display a video frame

        Parameters
        ----------
        frame : numpy.ndarray
            the frame(image) to display
        """
        cv2.imshow(f"{self.win_name} pyvideochat", frame)
        if cv2.waitKey(30) == 27:
            cv2.destroyAllWindows()
            exit()

    def resize(frame:numpy.ndarray, resolution:tuple) -> numpy.ndarray:
        """
        Resize a video frame

        Parameters
        ----------
        frame : numpy.ndarray
            the frame(image) to display
        resolution : tuple[int, int]
            resolution of the video window

        Returns
        -------
        numpy.ndarray
            returns the resized frames
        """
        try:
            return cv2.resize(src=frame, dsize=resolution)
        except:
            return frame

    def stop():
        """
        Stop OpenCV video instances
        """
        cv2.destroyAllWindows()
