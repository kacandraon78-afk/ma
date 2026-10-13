import ctypes, wave, sys
import espeakng_loader as e
lib = ctypes.CDLL(e.get_library_path())
CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
buf = bytearray()
def cb(wav, n, ev):
    if wav and n > 0:
        buf.extend(ctypes.string_at(wav, n * 2))
    return 0
_cb = CB(cb)
lib.espeak_Initialize.restype = ctypes.c_int
sr = lib.espeak_Initialize(2, 0, e.get_data_path().encode(), 0)
lib.espeak_SetSynthCallback(_cb)
def say(text, path, voice=b"ko", rate=135, pitch=45):
    buf.clear()
    assert lib.espeak_SetVoiceByName(voice) == 0, "voice"
    lib.espeak_SetParameter(1, rate, 0)   # rate
    lib.espeak_SetParameter(3, pitch, 0)  # pitch
    b = text.encode() + b"\0"
    lib.espeak_Synth(b, len(b), 0, 0, 0, 1, None, None)
    lib.espeak_Synchronize()
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(bytes(buf)); w.close()
    return len(buf) / 2 / sr
if __name__ == "__main__":
    print(say("이천이십칠년 정미년, 뱀띠 닭띠 소띠에게는 월살이 찾아옵니다.", "t.wav"))
