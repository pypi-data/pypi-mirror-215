import argparse
import queue
import sys
import threading

import sounddevice as sd
import soundfile as sf


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def play_short_file(filename, device=None):
    data, fs = sf.read(filename)
    sd.play(data, fs, device=device)
    sd.wait()


def play_long_file(filename, device=None, blocksize=2048, buffersize=20):
    q = queue.Queue(maxsize=buffersize)
    event = threading.Event()

    def callback(outdata, frames, time, status):
        assert frames == blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = q.get_nowait()
        except queue.Empty as e:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort from e
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):].fill(0)
            raise sd.CallbackStop
        else:
            outdata[:] = data

    try:
        with sf.SoundFile(filename) as f:
            for _ in range(buffersize):
                data = f.read(blocksize)
                if not len(data):
                    break
                q.put_nowait(data)  # Pre-fill queue
            stream = sd.OutputStream(
                samplerate=f.samplerate, blocksize=blocksize,
                device=device, channels=f.channels,
                callback=callback, finished_callback=event.set)
            with stream:
                timeout = blocksize * buffersize / f.samplerate
                while len(data):
                    data = f.read(blocksize)
                    q.put(data, timeout=timeout)
                event.wait()  # Wait until playback is finished
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        sys.exit(0)
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
        sys.exit(1)


def play_audio_file(filename, device=None, short_duration_threshold=10.0, blocksize=2048, buffersize=20):
    try:
        duration = sf.info(filename).duration
    except Exception as e:
        print(f"Error: Failed to get audio file duration - {str(e)}")
        sys.exit(1)

    if duration <= short_duration_threshold:
        # print(f"Playing short audio file: {filename}")
        try:
            play_short_file(filename, device=device)
        except KeyboardInterrupt:
            print('\nInterrupted by user')
            sys.exit(0)
        except Exception as e:
            print(f"Error: {type(e).__name__} - {str(e)}")
            sys.exit(1)
    else:
        # print(f"Playing long audio file: {filename}")
        play_long_file(filename, device=device, blocksize=blocksize, buffersize=buffersize)

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', metavar='FILENAME', help='audio file to be played back')
    parser.add_argument('-d', '--device', type=int_or_str, help='output device (numeric ID or substring)')
    parser.add_argument('-b', '--blocksize', type=int, default=2048, help='block size (default: %(default)s)')
    parser.add_argument('-q', '--buffersize', type=int, default=20, help='number of blocks used for buffering (default: %(default)s)')
    args = parser.parse_args()

    play_audio_file(args.filename, device=args.device, blocksize=args.blocksize, buffersize=args.buffersize)

if __name__ == '__main__':
    main()