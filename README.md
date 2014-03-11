## Push based syncing based on directory events

### Introduction

This code is currently WIP and is intended as a proof of concept for the push based syncing idea that would be useful for FTP mirror syncing between master and slave nodes in the OSL FTP Syncing architecture.

I initially experimented with [lsyncd](http://code.google.com/p/lsyncd/) which does just that,
but at [OSL](osuosl.org) we need the ability to tweak the way we carry out the sync,
possibily defining a sync priority for certain files to sync before others are synced.

### Idea

Idea: Inotify is an interesting utility that allows us to track directory events.
Inotify wrapper `pyinotify` coupled with `rsync` can be used to initiate push based
syncing whenever new content is available at the master server or a file is updated, etc.
(Multiple directory events can be tracked)

The exact file name can be caught in the events that will allow us to check whether
the currently added file is to be included / excluded and whether it has a higher sync priority
than other files in the queue.

### Todo:

* Allowing include / exclude options
* Allowing user to define priority and use of priority queues.
* Add docs for usage
