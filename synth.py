import math
import numpy
import pyaudio


def sine(frequency, seconds, sampling_rate):
    """factor = cycles/sec / bits/sec

    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.
    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # Angular frequency of a wave.
    angular_freq = float(frequency) * (math.pi * 2)

    # Normalized frequency, or the frequency in radians divided by sampling
    # rate.
    cycles_per_sample = angular_freq / sampling_rate
    
    # The sampling period, expressed as a discrete interval of time 
    # [0, seconds).
    values = numpy.arange(length)
    return numpy.sin(cycles_per_sample * values)

def triangle(frequency, seconds, sampling_rate):
    """A triangle wave.

    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.

    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # Angular frequency of a wave.
    angular_freq = float(frequency) * (math.pi * 2)

    # Normalized frequency, or the frequency in radians divided by sampling
    # rate.
    cycles_per_sample = angular_freq / sampling_rate
    
    # The sampling period, expressed as a discrete interval of time 
    # [0, seconds).
    values = numpy.arange(length)
    # from wolframalpha: http://mathworld.wolfram.com/TriangleWave.html
    return 2 * numpy.arcsin(numpy.sin(values * cycles_per_sample))


def square(frequency, seconds, sampling_rate):
    """A square wave.

    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.

    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # The period of the square wave.
    period = sampling_rate / float(frequency)
    values = numpy.arange(length)
    def squaregen(period, length, amplitude):
        x = 0
        y = -amplitude
        half_period = round(float(period) / 2)
        while x < length:
            # An acceptable epsilon value. Flip signs every half period.
            if x % half_period <= 0.5:
                y *= -1
            yield y 
            x += 1
    values = numpy.fromiter(squaregen(period, length, 0.5), "d")
    return values


def play_tone(stream, frequency=440, seconds=1, rate=44100):
    """Play a tone, as expressed by a waveform.

    Args:
        stream: the audio stream to write to.
        frequency: the frequency of the tone, in Hz.
        seconds: the length of the tone in seconds.
        rate: the sampling rate of the audio stream.
    """
    chunks = []
    sine_tone = sine(frequency, seconds, rate)
    triangle_tone = triangle(frequency, seconds, rate)
    square_tone = square(frequency, seconds, rate)
    chunks.append(sine_tone)
    chunks.append(triangle_tone)
    chunks.append(square_tone)

    chunk = numpy.concatenate(chunks)

    stream.write(chunk.astype(numpy.float32).tostring())


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)

    play_tone(stream)

    stream.close()
    p.terminate()
