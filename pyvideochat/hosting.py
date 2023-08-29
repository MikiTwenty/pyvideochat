# hosting.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of pyvideochat and is released under
# the MIT License: https://opensource.org/license/mit/

import socket, pickle, struct, time, numpy
from .utils import _Logger
from .video import Video

class _Socket():
    def __init__(self, name, show_ip, capture_video,
                 video_source, verbose, screen_resolution) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.capture_video = capture_video
        self.screen_resolution = screen_resolution
        self.video_source = video_source
        self.verbose = verbose
        self.timed_out = False
        if show_ip:
            _Logger.info(f"IP address: {self.host_ip}")
        if self.capture_video:
            _Logger.info(f"Capture video enabled.")
            self.video = Video(name, video_source, screen_resolution, verbose)

    def _set_port(self):
        while True:
            port = _Logger.input(f"Select {self.socket_type} port")
            if len(port) == 4:
                try:
                    port = int(port)
                    break
                except:
                    _Logger.warning("Port must be an int!")
            else:
                _Logger.warning("Port must be an int of length 4!")
        return port

    def send(self, frame:numpy.ndarray=None, resolution:tuple=(640, 480), show:bool=False) -> None:
        """
        Send a frame to the connected socket

        Parameters
        ----------
        frame : numpy.ndarray, optional
            the frame to send, by default None
        resolution : tuple[int, int], optional
            the frame resolution, by default (640, 480)
        show : bool, optional
            display the video, by default False
        """
        try:
            frame_check = list(frame)
        except:
            frame_check = frame
        if self.capture_video and frame_check == None:
            capturing, frame = self.video.read()
        elif frame_check != None:
            capturing = True
        else:
            capturing = False
        if capturing:
            try:
                frame = Video.resize(frame, resolution)
                serialized_frame = pickle.dumps(frame)
                message = struct.pack("Q", len(serialized_frame)) + serialized_frame
                if show:
                    frame = Video.resize(frame, resolution=self.screen_resolution)
                    self.video.show(frame)
                self.client_socket.sendall(message)
            except:
                pass

    def receive(self, show:bool=True) -> tuple:
        """
        Receive a frame from the connected socket

        Parameters
        ----------
        show : bool, optional
            display the video, by default True

        Returns
        -------
        tuple[bool, numpy.ndarray]
            returns (True, numpy.ndarray) while receiving data, (False, None) otherwise
        """
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(payload_size)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(msg_size)
                if not data:
                    break
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            if show:
                frame = Video.resize(frame, resolution=self.screen_resolution)
                self.video.show(frame)
            return True, frame
        except:
            pass

    def is_connected(self) -> socket.socket:
        """
        Check if a client is connected with the server

        Returns
        -------
        numpy.ndarray
            None if no socket is connected, socket.socket otherwise
        """
        if self.client_socket:
            return True
        else:
            return False

    def close(self) -> None:
        """
        Interrupt the connection and close the socket
        """
        self.socket.close()
        try:
            Video.stop()
        except:
            pass
        _Logger.text(f"{self.socket_type} stopped!")

class Server(_Socket):
    def __init__(self, name:str='Server', show_ip:bool=True, capture_video:bool=True,
                 screen_resolution:tuple=(640,480), video_source:int=0, verbose:bool=False) -> None:
        """
        Streaming server socket

        Parameters
        ----------
        name : str, optional
            name of the Socket, by default 'Server'
        show_ip : bool, optional
            print server IP address, by default True
        capture_video : bool, optional
            enable video capturing with cameras, by default True
        screen_resolution : tuple[int, int], optional
            resolution of the video window, pass pyvideochat.FULLSCREEN to set fullscreen mode, by default (640, 480)
        video_source : int, optional
            set camera index, by default 0
        verbose : bool, optional
            get more output, by default False
        """
        super().__init__(name=name, show_ip=show_ip, capture_video=capture_video,
                         screen_resolution=screen_resolution, video_source=video_source, verbose=verbose)
        self.server_socket = self.socket

    def connect(self, port:int=None, timeout:int=0) -> None:
        """
        Wait for a client socket connection

        Parameters
        ----------
        port : int, optional
            set the port to open for connections, if None get input, by default None
        timeout : int, optional
            set timeout to check for connections, if set to 0 the fucntion call is blocking, by default 0
        """
        if timeout == 0:
            blocking = True
        else:
            blocking = False
            self.server_socket.settimeout(timeout)
        if not self.timed_out:
            if not port:
                port = self._set_port()
            socket_address = (self.host_ip, port)
            try:
                self.server_socket.bind(socket_address)
            except Exception as error:
                raise(error)
            _Logger.text(f"Listening at {self.host_ip}:{str(port)}...")
        self.server_socket.listen(5)
        try:
            self.client_socket, address = self.server_socket.accept()
            if not self.timed_out:
                _Logger.success(f"Got connection from {address[0]}")
        except:
            self.timed_out = True
            if not blocking:
                _Logger.error("Timed out!")
            else:
                time.sleep(1)
                self.connect(port, timeout)

    def start(self):
        """
        Start default pyvideochat server loop cycle
        """
        while self.is_connected():
            receiving, _ = self.receive(show=True)
            if receiving:
                self.send(show=False)

class Client(_Socket):
    def __init__(self, name:str='Client', show_ip:bool=True, capture_video:bool=True,
                 screen_resolution:tuple=(640,480), video_source:int=0, verbose:bool=False) -> None:
        """
        Streaming client socket

        Parameters
        ----------
        name : str, optional
            name of the Socket, by default 'Server'
        show_ip : bool, optional
            print server IP address, by default True
        capture_video : bool, optional
            enable video capturing with cameras, by default True
        screen_resolution : tuple[int, int], optional
            resolution of the video window, pass pyvideochat.FULLSCREEN to set fullscreen mode, by default (640, 480)
        video_source : int, optional
            set camera index, by default 0
        verbose : bool, optional
            get more output, by default False
        """
        super().__init__(name=name, show_ip=show_ip, capture_video=capture_video,
                         screen_resolution=screen_resolution, video_source=video_source, verbose=verbose)
        self.client_socket = self.socket

    def _set_ip(self):
        return _Logger.input(f"Select {self.socket_type} ip")

    def connect(self, host_ip:str=None, port:int=None, timeout:int=0) -> None:
        """
        Connect to the server socket

        Parameters
        ----------
        host_ip : str, optional
            set the host ip, if None get input, by default None
        port : int, optional
            set the host port, if None get input, by default None
        timeout : int, optional
            set timeout to check for connections, if set to 0 the fucntion call is blocking, by default 0
        """
        if timeout == 0:
            blocking = True
        else:
            blocking = False
            self.client_socket.settimeout(timeout)
        if not self.timed_out:
            if not host_ip:
                host_ip = self._set_ip()
            if not port:
                port = self._set_port()
            _Logger.text(f"Connecting to {host_ip}:{port}...")
        try:
            self.client_socket.connect((host_ip, port))
            if not self.timed_out:
                _Logger.success(f"Connected to {host_ip}")
            return True
        except:
            self.timed_out = True
            if not blocking:
                _Logger.error("Timed out!")
            else:
                time.sleep(1)
                self.connect(host_ip, port, timeout)

    def start(self):
        """
        Start default pyvideochat client loop cycle
        """
        while self.is_connected():
            self.send(show=False)
            receiving, _ = self.receive(show=True)
            if not receiving:
                break