#author Ryan Bailey

import pyaudio
import wave
import threading

def test():
    ar = AudioRecorder()
    while True:
        print("Type \"start\" to start recording: ", end="")
        inp = input()
        if inp.lower() == "start":
            break
    ar.start_recording()
    
    while True:
        print("Type \"stop\" to stop recording: ", end="")
        inp = input()
        if inp.lower() == "stop":
            break
    ar.stop_recording()

    print("Enter a filename (file will be saved as [filename].wav): ", end="")
    inp = input()
    ar.save_data(inp + ".wav")

class AudioRecorder():
    def __init__(self):
        self.__stream = None
        self.__p = pyaudio.PyAudio()
        self.__frames = []
        self.__stop_recording_signal = True #recording hasn't started yet
        self.__data_cleared = True #true to begin with as no data recorded yet

        self.__CHUNK = 1024
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 1
        self.__RATE = 16000
        self.__RECORD_SECONDS = 5

        self.__event = threading.Event()
        self.__recording_thread = threading.Thread(target=self.recording_thread_function, args=())
        
    def recording_thread_function(self):
        self.__p = pyaudio.PyAudio()
        
        self.__stream = self.__p.open(format=self.__FORMAT,
                                      channels=self.__CHANNELS,
                                      rate=self.__RATE,
                                      input=True,
                                      frames_per_buffer=self.__CHUNK)
        
        self.__frames = []
        self.__data_cleared = False
        self.__stop_recording_signal = False
        while True:
            if self.__event.is_set():
                self.__stop_recording_signal = True
                break
            
            data = self.__stream.read(self.__CHUNK)
            self.__frames.append(data)

    def start_recording(self):
        self.__recording_thread.start()
        print("Recording is starting.")

    def stop_recording(self):
        self.__event.set()
        
        while self.__recording_thread.is_alive():
            pass
        
        print("Recording is stopping.")

        self.__stream.stop_stream()
        self.__stream.close()
        self.__p.terminate()

    def save_data(self, file_name):
        if self.__data_cleared:
            print("Nothing to save.")
        elif not self.__stop_recording_signal:
            print("Cannot save data while recording.")
        else:
            wf = wave.open(file_name, 'wb')
            wf.setnchannels(self.__CHANNELS)
            wf.setsampwidth(self.__p.get_sample_size(self.__FORMAT))
            wf.setframerate(self.__RATE)
            wf.writeframes(b''.join(self.__frames))
            wf.close()

    def clear_data():
        if not self.__stop_recording_signal:
            print("Cannot clear data while recording.")
        self.__frames = []
        self.__data_cleared = True

if __name__ == "__main__":
    test()
