NestBot
=======

A twitter bot that controls the Nest thermostat by the owner of the Nest sending it direct messages on twitter.

Status
======

This is in the prototype stage.

Running it
==========

- Create a Twitter account and register an app id to list on it.
- Update settings file with the Twitter app info and the Nest user name and password.
- Communicate with the NestBot via direct messages from your personal Twitter account.

Longer Term Features
====================

- Support multiple nest devices.
- Allow users to use a NestBot as a service by following an account, and registering their nest device.

Used Libraries
==============

- pynest - with modifications to change it from a command line tool to an Python package.
- tweepy - for interacting with Twitter.
