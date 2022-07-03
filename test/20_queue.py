#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

r = flnet.Router(sched)
r.bandwidth = 2.
r.qsize = 5

# Sink node.
n = flnet.Node()

r.connect(n)

ok(r.q == 0)
ok(r.p == 0.)

# Below the bandwidth.
m = flnet.Message(rate=1.)
r.enqueue(m)
r.advance()

# Queue will not build up.
ok(r.q == 0)
ok(r.p == 0.)

# Departure rate must be equal to incoming rate.
m = n.queue[-1]
ok(m.rate == 1.)

# Same as the the bandwidth.
m = flnet.Message(rate=2.)
r.enqueue(m)
r.advance()

# Again, queue will not build up.
ok(r.q == 0)
ok(r.p == 0.)

# Departure rate must be equal to incoming rate.
m = n.queue[-1]
ok(m.rate == 2.)

# Arrival rate exceess the bandwidth
m = flnet.Message(rate=3.)
r.enqueue(m)
r.advance()

# The queue grows but no packet loss yet.
ok(r.q > 0)
ok(r.p == 0.)

m = flnet.Message(rate=6. * 1000)
r.enqueue(m)
r.advance()

ok(r.q == r.qsize)
ok(r.p > 0.)
