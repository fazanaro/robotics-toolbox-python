
import ropy as rp
import spatialmath as sm
import numpy as np
import time

env = rp.PyPlot()
env.launch('Panda Resolved-Rate Motion Control Example')

panda = rp.PandaMDH()
panda.q = panda.qr

Tep = sm.SE3(np.copy(panda.fkine().A))
Tep = Tep * sm.SE3.Tx(-0.2) * sm.SE3.Ty(0.2) * sm.SE3.Tz(0.2)

arrived = False
env.add(panda)

dt = 0.05

while not arrived:

    start = time.time()
    v, arrived = rp.p_servo(panda.fkine(), Tep, 0.1)
    panda.qd = np.linalg.pinv(panda.jacobe()) @ v
    env.step()
    stop = time.time()

    if stop - start < dt:
        time.sleep(dt - (stop - start))

env.hold()
