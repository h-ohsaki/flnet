#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

n1 = flnet.Sender(sched)
n2 = flnet.Receiver(sched)
n1.connect(n2)
n1.dst = n2

# Forward from sender to receiver.
ok(not n2.queue)
n1.advance()
ok(n2.queue)

# Peek the message in the queue.
m = n2.queue[0]
ok(not m.ack)
ok(m.src == n1)
ok(m.dst == n2)
ok(m.tstamp == 0.)
ok(m.w == 1)
ok(m.p == 0.)
ok(m.rate == 0.)

# Send the message back to the sender.
ok(not n1.queue)
n2.advance()
ok(not n2.queue)
ok(n1.queue)
# Peek the message in the queue.
m = n1.queue[0]
ok(m.ack)
ok(m.src == n2)
ok(m.dst == n1)
ok(m.tstamp == 0.)
ok(m.w == 1)
ok(m.p == 0.)

# Pretend for sender to see high packet loss.
n1.p = 1.
ok(n1.p == 1.)

# Receiving the message updates the sender status.
n1.advance()
ok(not n1.queue)
# n1 still observes zero RTT.
ok(n1.rtt == 0.)
# Thus, window size does never change.
ok(n1.w == 1.)
ok(n1.p == 0.)
