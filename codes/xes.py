import math
import numpy as np

mphE = 77
bat = 133
servo = 16
rr = 9
lg = 12

bfs = 50.54 #39
ph = 7.78

ts = 21.23 #12
wm = 25 #14

cbar = .206
lh = .98
lv = .88
l = 1.192

Wwing = 119
Wempty = 462
Wpay = 50
W = Wempty+Wpay

xnose = -.2

S = .4
Sh = .042
AR = 9.45
ARh = 6.44
aw = 2*math.pi/(1+2/AR)
ah = 2*math.pi/(1+2/ARh)
dh = lh
CLwnom = .75
CMwnom = -.15

fe = .6
zeta = math.acos(1-2*fe)
ae = 2*(math.pi-zeta+math.sin(zeta))/(1+2/ARh)
# 0 at wing tip

nose = (mphE+lg) * xnose # plane vanilla nose
tail = ts * (l+xnose)
wing = (Wwing) * .25*cbar
misc = (rr+bat+wm) * .5*cbar
s = servo * 1.5*cbar
fuse = bfs * (l/2+xnose)
other = ph * ((l+xnose)+.25*cbar)/2

xcgempt = (nose+tail+wing+misc+s+fuse+other)/Wempty
print(xcgempt)

xcgnom = .093

xpay = (xcgnom * (Wempty+Wpay) - (nose+tail+wing+misc+s+fuse+other))/Wpay
print(xpay)

xnp = ((cbar/4)*(S/Sh)*(aw/ah)+(dh+cbar/4))/((S/Sh)*(aw/ah)+1)
print(xnp)

coeffs = np.array([[1, Sh/S], [xcgempt-(cbar/4), (Sh/S)*(xcgempt-dh-(cbar/4))]])
ans = np.array([(Wempty/W)*CLwnom, -cbar*CMwnom])
CLwempt, CLhempt = np.linalg.solve(coeffs, ans)

alpha = (CLwempt-CLwnom)/aw
alphae = (CLhempt-ah*alpha)/ae
print(alphae, alphae*180/math.pi)
