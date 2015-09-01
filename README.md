# Scoring
A Raspberry Pi game scoring project.

This project keeps score on card games like Racing Demons. It can be used in any game where you have players and rounds and each players score changes each round.

To enter scores on this program you use an infrared remote control.

## Hardware:
To use this program you will need a Raspberry Pi (any model), an infrared remote reciever (see http://www.modmypi.com/blog/raspberry-pis-remotes-ir-receivers) and an IR remote with numbers (A TV remote would work).

## Software:
#####You need LIRC set up:

```sudo apt-get install lirc```

and then see http://www.modmypi.com/blog/raspberry-pis-remotes-ir-receivers.

Then copy lircrc from this repsitory to /etc/lirc/.

#####You will also need:
- pylirc: https://pypi.python.org/pypi/pylirc
- pygame: http://www.pygame.org/download.shtml

##Usage:
Run scoring/scoring.py.

It should be easy to work out.
Remote numbers to enter scores, volume up and down buttons for positive/negative, OK to submit.
