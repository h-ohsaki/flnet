#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

n1 = flnet.Sender(sched)
n2 = flnet.Receiver(sched)
# Set link delay to 1ms.
n1.connect(n2, .1)
n1.dst = n2

# Override the window size to 10.
n1.w = 10.
ok(n1.p == 0.)

n1.advance()

# advance 0.01ms by default.
for _ in range(10):
    sched.advance()

n2.advance()

# Check the validity of the message.
msg = n1.queue[0]
ok(msg.w == 10.)
ok(msg.p == 0.)

# advance 0.01ms by default.
for _ in range(10):
    sched.advance()

# Overwrite the loss rate in the message.
msg.p = .5
n1.advance()

# Sender knows the current loss rate.
ok(n1.p == .5)
# Must have shrunk the window size.
ok(n1.w < 10.)
