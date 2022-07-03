#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler(max_time=10000)
monitor = flnet.Monitor(sched)

sender = flnet.Sender(sched)
sender2 = flnet.Sender(sched)
router = flnet.Router(sched)
receiver = flnet.Receiver(sched)
sender.connect(router, delay=1.)
sender2.connect(router, delay=2.)
router.connect(receiver, delay=.1)
sender.dst = receiver
sender2.dst = receiver

router.bandwidth = 3.
router.qsize = 2

while sched.is_running():
    sender.advance()
    if sched.time >= 100:
        sender2.advance()
    router.advance()
    receiver.advance()
    sched.advance()
    monitor.display([sender, sender2, router])
