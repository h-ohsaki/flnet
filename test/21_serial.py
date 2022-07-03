#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

sender = flnet.Sender(sched)
router = flnet.Router(sched)
receiver = flnet.Receiver(sched)
sender.dst = receiver

sender.connect(router, .1)
router.connect(receiver)

ok(not router.queue)
# Foward the message to the router.
sender.advance()
ok(router.queue)

for _ in range(10):
    sched.advance()

ok(not receiver.queue)
# Foward the message to the receiver.
router.advance()
ok(receiver.queue)

ok(not router.queue)
# Foward the message to the sender.
receiver.advance()
ok(router.queue)

ok(not sender.queue)
# Foward the message to the receiver.
router.advance()
ok(sender.queue)

for _ in range(10):
    sched.advance()

ok(sender.w == 1.)
ok(sender.rtt == 0.)
# Process the message at the sender.
sender.advance()
ok(sender.p == 0.)
ok(sender.w > 1.)
