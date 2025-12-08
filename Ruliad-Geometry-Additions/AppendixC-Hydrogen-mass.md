# Appendix C: Hydrogen and the Next Harmonic Level

## C.1 Overview

Appendix B showed that fundamental particle masses, in units of the electron mass, follow simple harmonic formulas built from π and e.

Hydrogen is the next nontrivial scale: the first bound atom, the minimal persistent object made from a proton and an electron.

In standard atomic physics, the hydrogen mass is
in electron mass units ($m_e = 1$):

$$
\frac{m_H}{m_e} = \frac{m_p}{m_e} + 1 - \frac{E_{\text{bind}}}{m_e c^2}
$$

The ground-state binding energy of hydrogen is

$$
E_{\text{bind}} = \frac{1}{2}\alpha^2 m_e c^2
$$

so

$$
\frac{m_H}{m_e} = \frac{m_p}{m_e} + 1 - \frac{1}{2}\alpha^2
$$

Appendix B already fixed:

- Proton:  $$\frac{m_p}{m_e} = 6\pi^5$$  
- Fine-structure constant:  $$\alpha = \frac{1}{8 \cdot 2\pi \cdot e} = \frac{1}{16\pi e}$$

Substituting this $\alpha$ into the hydrogen formula shows that hydrogen also follows the same $\pi$–$e$ harmonic structure, one level up in scale.

---

## C.2 Hydrogen Mass from $\pi$ and $e$

With $\alpha = 1/(16\pi e)$ we have

$$
\alpha^2 = \frac{1}{(16\pi e)^2} = \frac{1}{256\pi^2 e^2}
$$

so

$$
\frac{1}{2}\alpha^2 = \frac{1}{512\pi^2 e^2}
$$

Then

$$
\frac{m_H}{m_e}
= 6\pi^5 + 1 - \frac{1}{2}\alpha^2
= 6\pi^5 + 1 - \frac{1}{512\pi^2 e^2}
$$

Numerically:

- $6\pi^5 \approx 1836.1181$
- $\dfrac{1}{512\pi^2 e^2} \approx 2.68 \times 10^{-5}$

so

$$
\frac{m_H}{m_e} \approx 1836.1181 + 1 - 0.0000268 = 1837.1181
$$

Using $m_H/m_e \approx 1837.15$ from experiment, the relative error is

$$
\text{Error} \approx 0.002\%
$$

the same level of precision seen for the proton formula.

---

## C.3 Hydrogen in the Harmonic Table

Extending the mass table from Appendix B:

| Particle  | Measured ($m_e$ units) | Formula                                           | Calculated | Error   | Stability         |
|-----------|------------------------|---------------------------------------------------|-----------:|--------:|-------------------|
| Electron  | 1.00                   | 1 (reference)                                     | —          | —       | Stable            |
| Proton    | 1836.15                | $6\pi^5$                                          | 1836.12    | 0.002%  | Stable            |
| **Hydrogen** | **1837.15**        | $6\pi^5 + 1 - \dfrac{1}{512\pi^2 e^2}$            | **1837.12**| **0.002%** | Stable (bound atom) |

Hydrogen mass can be written compactly as

$$
m_H = m_e \left( 6\pi^5 + 1 - \frac{1}{512\pi^2 e^2} \right)
$$

with all structure expressed in terms of $\pi$ and $e$, using the same constants that already fixed the fine-structure constant and proton mass.

---
## C.4 Pattern Repetition at the Atomic Scale

The pattern from Appendix B repeats at the atomic scale.

Hydrogen mass in electron units is

$$
\frac{m_H}{m_e} = 6\pi^5 + 1 - \frac{1}{2}\alpha^2
$$

with

$$
\alpha = \frac{1}{16\pi e}.
$$

So we can read the hydrogen mass as:

- $6\pi^5$: the pure proton harmonic (single-term $\pi$-mode)
- $+1$: one electron mass unit
- $-\dfrac{1}{2}\alpha^2$: the binding correction built from the same $\pi$ and $e$ via $\alpha$

In words:

> Hydrogen = proton mode + electron unit − a small binding term,  
> and all three pieces are determined by the same $\pi$–$e$ geometry.

This mirrors the harmonic logic at the particle level:

- pure $\pi$-mode → perfectly stable (proton)
- simple additive unit → builds a bound structure (hydrogen)
- small geometric correction → binding energy from $\alpha$

Hydrogen is thus the next harmonic level selected by the same constants that already fixed $\alpha$ and the proton mass.

## C.5 Verification Code

```python
import math
pi = math.pi
e  = math.e

alpha = 1/(16*pi*e)

mp_over_me = 6*pi**5
mH_over_me = mp_over_me + 1 - 0.5*alpha**2

measured_H = 1837.15  # hydrogen mass in m_e units

error = abs(mH_over_me - measured_H) / measured_H * 100

print("Proton (6*pi^5):", mp_over_me)
print("Hydrogen formula:", mH_over_me)
print("Measured H (m_e units):", measured_H)
print("Relative error (%):", error)
