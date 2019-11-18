# Age of Triggers
This is an api for python 3.4. You can read and write Age of Empires 2 scenario map files for AOE2 Definitive Edition.

It was initially a fork from agescx [https://github.com/dderevjanik/agescx].

How to install:

pip3 install git+https://github.com/ncarrara/aoe2-meta-triggers.git


# TODO
- [DONE] support DE files
- [WIP] clean code and make it pep8
- [DONE] encoding with strings. String send by message, or trigger name etc are display wrongly on the editor. And might disapear when playing the game (sendChat for example, sed an invisible text)
- [DONE] Inverse condition not supported (for aoe2scenario).
