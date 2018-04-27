# Break Glass with Resonant Frequency

Breaking A Wine Glass By Detecting Resonant Frequency in Python

Accompanies a blog post at [Make Art with Python](https://www.makeartwithpython.com/blog/break-glass-with-resonant-frequency/)

![Breaking](https://github.com/burningion/break-glass-with-resonant-frequency/raw/master/images/animate.gif)

## Running this Program

You'll need to have `Music21`, `PyAudio`, `NumPy`, `Pygame`, `aubio` and Python 3 installed. All of these are installable with `pip`.

Once that's setup, you'll run the program, strike your wine glass, and then press spacebar to begin playing back the detected frequency. If your speakers are loud enough, your wine glass should break!


## macOS

If you want to run this program with `pygame` and other related packages on macOS, you'll need to install [libsdl](https://www.libsdl.org/) and [PortAudio](http://portaudio.com/docs/v19-doxydocs/index.html), which you can install using [Homebrew](https://brew.sh/).

```
brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
brew install portaudio
```

`pygame` has also been known to not detect key events when running from the terminal in a Python 3 virtualenv. See [pygame/issues/359](https://github.com/pygame/pygame/issues/359#issuecomment-351988455), and [anaconda-issues/issues/199](https://github.com/ContinuumIO/anaconda-issues/issues/199#issuecomment-350534918).

The workaround for this is that if you have Python 3 installed on your device, then you should `pip3 install` the aforementioned libraries, where `pip3` links back to your Python 3.x installation.

