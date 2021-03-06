#!/usr/bin/env pypy3
#
#
# Copyright (c) 2022, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: dumbbell.py,v 1.2 2022/07/01 15:44:46 ohsaki Exp ohsaki $
#

# example: dumbbell.py 10 | rplot -x1

import sys

import flnet

try:
    nsenders = int(sys.argv[1])
except IndexError:
    nsenders = 10

sched = flnet.Scheduler(max_time=10000)
monitor = flnet.Monitor(sched)

senders = [flnet.Sender(sched) for _ in range(nsenders)]
router = flnet.Router(sched)
receiver = flnet.Receiver(sched)
for sender in senders:
    sender.dst = receiver
    sender.connect(router, delay=1)
router.connect(receiver, delay=1)
# 100 [Mbit/s] with 1,500 byte packet
router.bandwidth = 8.33
router.qsize = 10

while sched.is_running():
    for sender in senders:
        if sched.time > 100 * sender.id_:
            sender.advance()
    router.advance()
    receiver.advance()
    sched.advance()
    monitor.display([senders[0], senders[1], router])
