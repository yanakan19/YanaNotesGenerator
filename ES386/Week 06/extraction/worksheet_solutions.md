# Extraction: Mode shapes worksheet solutions (1).pdf (3 pages, 150 DPI)

ES386 Dynamics of Vibrational Systems, example sheet "Mode shapes" with full solutions. University of Warwick, School of Engineering.

## Page 1 — Exercise 1 (2 DoF, mode shapes)
**Question.** A 2 DoF vibration system is described by $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$ with
$$M = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}\ \mathrm{kg}, \quad K = \begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}\ \mathrm{N\,m^{-1}}$$
Verify that $\omega_1 = \sqrt{2}$ rad/s and $\omega_2 = 2$ rad/s are natural frequencies, determine and sketch the mode shapes, and comment on the number of nodes in each mode.

**Solution.** Natural frequencies are the square roots of the eigenvalues of $A = M^{-1}K$. Since $M = I$, $A = K = \begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}$. Verify the given frequencies by finding the eigenvectors (mode shapes) of A: with $\lambda_1 = \omega_1^2 = 2$ and $\lambda_2 = \omega_2^2 = 4$, the eigenvector equations
$$\begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}\begin{pmatrix} x_1 \\ x_2 \end{pmatrix} = 2\begin{pmatrix} x_1 \\ x_2 \end{pmatrix}, \qquad \begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}\begin{pmatrix} x_1 \\ x_2 \end{pmatrix} = 4\begin{pmatrix} x_1 \\ x_2 \end{pmatrix}$$
yield normalised eigenvectors $\begin{pmatrix} 1 \\ 1 \end{pmatrix}$ and $\begin{pmatrix} 1 \\ -1 \end{pmatrix}$ respectively. Check the consistency of the two equations per mode to confirm $\omega_1^2$ and $\omega_2^2$ are eigenvalues. Sketches show that $\omega_1$ (the fundamental mode) has no nodes, while the $\omega_2$ mode has a single node between $x_1$ and $x_2$.

## Page 2 — mode sketches, Exercise 2 (free free drivetrain)
Mode sketches for Exercise 1: $\omega_1 = \sqrt{2}$ rad/s both masses move together (horizontal line, no node); $\omega_2 = 2$ rad/s masses move in opposite directions (sloped line crossing zero, one node between $x_1$ and $x_2$).

**Exercise 2.** A drivetrain is modelled as a free free system:
$$\begin{pmatrix} I_1 & 0 & 0 \\ 0 & 2I_2 & 0 \\ 0 & 0 & I_1 \end{pmatrix}\begin{pmatrix} \ddot{\theta}_1 \\ \ddot{\theta}_2 \\ \ddot{\theta}_3 \end{pmatrix} + \begin{pmatrix} k_1 & -k_1 & 0 \\ -k_1 & 2k_1 & -k_1 \\ 0 & -k_1 & k_1 \end{pmatrix}\begin{pmatrix} \theta_1 \\ \theta_2 \\ \theta_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}$$
(i) The drivetrain has a natural mode with angular frequency $\omega = 0$; describe the motion of the inertias for this mode (no need to solve the EoM).
(ii) It is reported the system can freely vibrate at $\omega_1 = \sqrt{k_1/I_1}$; demonstrate whether the model is consistent and give the relative motions of the equivalent inertias at this frequency.
(iii) Do you expect further modes of free vibration? If yes, sketch the mode shape(s) and compare their frequency qualitatively to $\omega_1$.

**Solution 2.**
(i) The $\omega = 0$ mode is the free wheel (rigid body) mode: all equivalent inertias rotate with the same angular velocity. This is a fundamental property of all free free systems.
(ii) Assuming modes of the form $\theta_i = A_i\sin(\omega_n t)$ and substituting $\omega_1 = \sqrt{k_1/I_1}$ into the three equations:
$$-\omega_1^2 I_1 A_1 + k_1 A_1 - k_1 A_2 = 0 \Rightarrow k_1 A_2 = 0 \Rightarrow A_2 = 0$$
$$-2\omega_1^2 I_2 A_2 - k_1 A_1 + 2k_1 A_2 - k_1 A_3 = 0 \Rightarrow -k_1 A_1 - k_1 A_3 = 0 \Rightarrow A_1 = -A_3$$
$$-\omega_1^2 I_1 A_3 - k_1 A_2 + k_1 A_3 = 0 \Rightarrow k_1 A_2 = 0$$
So $\omega_1$ is a solution: $I_1$ and $I_3$ move equally in opposite directions while $I_2$ is at rest (one node).

## Page 3 — Exercise 2 (iii), Exercise 3 (torsional three inertia)
**Solution 2 (iii).** As the system has three degrees of freedom, three modes of free vibration are expected. Two are found so far, at frequencies $0$ and $\sqrt{k_1/I_1}$ with zero and one nodes, so one mode is missing. It must have two nodes, one between each pair of inertias: the first and last move in the same direction, the middle one opposite. More nodes mean higher frequency, so $\omega_2 > \omega_1$.

**Exercise 3.** A light shaft carries three inertias. In consistent units:
$$\begin{pmatrix} \ddot{\theta}_1 \\ \ddot{\theta}_2 \\ \ddot{\theta}_3 \end{pmatrix} + \begin{pmatrix} 2 & -2 & 0 \\ -2 & 3 & -1 \\ 0 & -1 & 1 \end{pmatrix}\begin{pmatrix} \theta_1 \\ \theta_2 \\ \theta_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}$$
The two natural frequencies of torsional oscillation are $\omega_n^2 = 3 \pm \sqrt{3}$. Find the mode shapes, normalising to unit amplitude for $\theta_1$, and comment on the number of modes.

**Solution 3.** Eigenvectors give the mode shapes and eigenvalues are $\omega_n^2$. Setting $A_1 = 1$:
$$\begin{pmatrix} 2 & -2 & 0 \\ -2 & 3 & -1 \\ 0 & -1 & 1 \end{pmatrix}\begin{pmatrix} 1 \\ A_2 \\ A_3 \end{pmatrix} = (3 \pm \sqrt{3})\begin{pmatrix} 1 \\ A_2 \\ A_3 \end{pmatrix}$$
Read $A_2$ from the top row, then $A_3$ from the bottom row.
Mode 1: $\left(1, \frac{\sqrt{3}-1}{2}, -\frac{\sqrt{3}-1}{2(2-\sqrt{3})}\right)$. Mode 2: $\left(1, -\frac{\sqrt{3}+1}{2}, \frac{\sqrt{3}+1}{2(2+\sqrt{3})}\right)$.
Three inertias in a freely rotating (free free) system give only two vibrations; the third mode is the rigid body rotation, equivalent to $\omega_n = 0$.

<!-- EXTRACTION COMPLETE: 3 pages -->
