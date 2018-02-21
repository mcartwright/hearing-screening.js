import logging
import os
import random
import scipy.io.wavfile
import numpy as np
import click

AUDIOFILEDTYPE = 'int16'
OUTPUT_DIR = 'hearing_screening/static/audio/'

@click.group()
def cli():
    pass

def wavread(filename):
    '''
    Wrapper to get a numpy array from -1 to 1 from a wav file
    '''
    wavdata = scipy.io.wavfile.read(filename)
    x = wavdata[1].astype('float64') / np.iinfo(wavdata[1].dtype).max
    return (wavdata[0],x)


def wavwrite(filename,rate,data,type=AUDIOFILEDTYPE):
    '''
    Wrapper to write from a -1 to 1 numpy array to a wavfile
    '''
    data = data * np.iinfo(type).max
    data = data.astype(type)
    scipy.io.wavfile.write(filename, rate, data)


def midi_note_num(freq):
    if freq==0:
        return 0.
    else:
        x = freq / 261.63
        x = np.log10(x) / np.log10(2)
        return (x * 12) + 60


def freq(midi_note_num):
    if midi_note_num==0:
        return 0.
    else:
        return 261.63 * (2**((midi_note_num - 60)/12.0))


def amp_scale(midi_note_num, midi_min=33, midi_max=123):
    max = 12.0
    return 10.0**((-((midi_note_num - midi_min) / float(midi_max - midi_min))) * max / 20.0)


@cli.command('gen_hearing_screening_audio_files')
@click.argument('midi_min', type=click.INT)
@click.argument('midi_max', type=click.INT)
@click.argument('repeats', type=click.INT)
@click.option('--output-dir', nargs=1, type=click.Path(exists=True), default=OUTPUT_DIR)
def gen_hearing_screening_audio_files(midi_min=33, midi_max=123, repeats=4, fs=22050, output_dir=OUTPUT_DIR):
    """
    Create the hearing screening audio files. 

    Parameters
    ----------
    fs : float
    midi_min : int
    midi_max : int
    repeats : int
    output_dir : str
    """
    tone_length = int(0.75 * fs)
    pause_length = int(0.25 * fs)
    attack_length = int(0.05 * fs)
    release_length = int(0.05 * fs)
    sustain_length = tone_length - attack_length - release_length
    release = np.hanning(2 * release_length)
    release = release[len(release)/2:]
    attack = np.hanning(2 * attack_length)
    attack = attack[0:len(attack)/2]
    sustain = np.ones(sustain_length)
    window = np.hstack([attack, sustain, release])

    stimuli_js = []

    for num_tones in range(2,9):
        for j in range(repeats):
            tone_list = [midi_min,midi_max]+[random.randrange(midi_min,midi_max) for _i in range(num_tones-2)] + ([0] * (8 - num_tones))
            random.shuffle(tone_list)

            # make sure there isn't too much silence in the beginning
            while tone_list[0]==0 and tone_list[1]==0:
                random.shuffle(tone_list)

            output = np.array([])
            for mn in tone_list:
                f = freq(mn)
                a = amp_scale(mn, midi_min, midi_max)
                output = np.hstack([output, a*window*np.sin(2*np.pi*(f/fs)*np.arange(tone_length)), np.zeros(pause_length)])

            output = 0.5 * output 
            filename = "tones{}_{}.wav".format(num_tones, j)
            wavwrite(os.path.join(output_dir, filename), fs, output)

            if len(stimuli_js)==0:
                stimuli_js.append("var stimuli=[{{'filename':'{}', 'num_tones': {}}}".format("tones{}_{}.mp3".format(num_tones, j), num_tones))
            else:
                stimuli_js.append(",\n             {{'filename':'{}', 'num_tones': {}}}".format("tones{}_{}.mp3".format(num_tones, j), num_tones))
    stimuli_js[-1] += "];\n"

    with open('src/static/js/src/stimuli.js', 'wb') as f:
        f.writelines(stimuli_js)


@cli.command('gen_calibration_file')
@click.argument('freq', type=click.FLOAT)
@click.argument('fs', type=click.INT)
@click.option('--output-dir', nargs=1, type=click.Path(exists=True), default=OUTPUT_DIR)
def gen_calibration_file(freq=1000, fs=22050, output_dir=OUTPUT_DIR):
    """
    Generate a single tone file.

    Parameters
    ----------
    fs : int
    freq : float
    output_dir : str
    """
    tone_length = int(10.0 * fs)
    attack_length = int(0.05 * fs)
    release_length = int(0.05 * fs)
    sustain_length = tone_length - attack_length - release_length
    release = np.hanning(2 * release_length)
    release = release[len(release)/2:]
    attack = np.hanning(2 * attack_length)
    attack = attack[0:len(attack)/2]
    sustain = np.ones(sustain_length)
    window = np.hstack([attack, sustain, release])          

    a = amp_scale(midi_note_num(freq))
    output = a*window*np.sin(2*np.pi*(float(freq)/fs)*np.arange(tone_length))

    output = 0.5 * output 
    filename = "{}Hz.wav".format(int(freq))
    wavwrite(os.path.join(output_dir, filename), fs, output)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    cli()
