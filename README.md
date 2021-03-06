# Pulling Radio Waves out of Thin Air

Code and slides for my [PyCon Israel 2018 talk](https://il.pycon.org/2018/schedule/presentation/34/)

Video of the talk is online at https://www.youtube.com/watch?v=xJOFaOM2wUc

## Content

 - [Talk Slides](talk.ipynb)
 - [Naive async FM demodulation](async_fm_demod.py)
 - [Offline numpy FM demodulation](numpy_fm_demod.py)
 - [FM demod GNU Radio Companion Flowgraph](fm.grc)

### NumPy Demod

```bash
$ python numpy_fm_demod.py capture
$ aplay wbfm-mono-50000.0.raw -r 50000 -f S16_LE -t raw -c 1
```

Note that the final sample rate can never really be 44.1kHz.

Alternatively dump and load samples:

```bash
$ python numpy_fm_demod.py dump out.npy
$ python numpy_fm_demod.py load out.npy
$ aplay wbfm-mono-50000.0.raw -r 50000 -f S16_LE -t raw -c 1
```
