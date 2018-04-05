# Python RTL-SDR Playground

Just some tests with binding RTL-SDR to Python programs

## NumPy Demod

```bash
$ python numpy_fm_demod.py
$ aplay wbfm-mono-50000.0.raw -r 50000 -f S16_LE -t raw -c 1
```

Note that the final sample rate can never really be 44.1kHz.
