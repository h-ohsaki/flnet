#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

n1 = flnet.Sender(sched)
n2 = flnet.Sender(sched)
r = flnet.Router(sched)
sink = flnet.Receiver(sched)
n1.dst = sink
n2.dst = sink

n1.connect(r, .1)
n2.connect(r, .1)
r.connect(sink)

ok(r.in_rate == 0.)

m1 = flnet.Message(src=n1, dst=sink, rate=1.)
r.enqueue(m1)
m2 = flnet.Message(src=n2, dst=sink, rate=1.)
r.enqueue(m2)
r.advance()
ok(r.in_rate == 1. + 1.)
ok(r.q > 0.)
ok(r.p == 0.)