#!/usr/bin/env python3

from test_more import ok, eq
import flnet

sched = flnet.Scheduler()

n1 = flnet.Sender(sched)
n2 = flnet.Receiver(sched)
# Set link delay to 0.1ms.
n1.connect(n2, .1)
n1.dst = n2

# Forward a message from sender to receiver.
n1.advance()
ok(not n1.queue)
ok(n2.queue)
# Mssage is not ready yet.
ok(not n2.msg_ready())
n2.advance()
ok(not n1.queue)
ok(n2.queue)

# advance 0.01ms by default.
for _ in range(10):
    sched.advance()

# Mssage is now ready to go.
ok(n2.msg_ready())
n2.advance()
ok(n1.queue)
ok(not n2.queue)

# advance 0.01ms by default.
for _ in range(10):
    sched.advance()

n1.advance()
ok(n1.rtt >= 2 * .1)
