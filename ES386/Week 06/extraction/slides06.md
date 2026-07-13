# Extraction: ES386 Slides 06 n DOF lecture 2026 (2).pdf (31 pages, 150 DPI)

## Page 1
Title slide: ES386 Dynamics of Vibrating Systems, Unit 6: Free multiple degree of freedom vibration, undamped lump model. University of Warwick. Decorative images (spring mass ball, chladni pattern). No technical content.

## Page 2
Vevox audience engagement QR code slide. No technical content.

## Page 3
Plan for today: 1. Summary of solving matrix equations. 2. Visualising what they mean. 3. Many degrees of freedom, easy matrix building for simple systems (aka heuristics). 4. Free free systems. Right side image: vertical chain of masses M connected by springs with an orange base block.

## Page 4
Free n DoF vibrations: How do you solve a problem like
$$M\ddot{\mathbf{x}} + K\mathbf{x} = \mathbf{0}$$
(matrix equation of motion, M mass matrix, K stiffness matrix, x displacement vector).

## Page 5
Solving equations of motion, dealing with the 2nd order ODE. Reference Rao 6.9.
Trial solution: $x_i = A_i \cos(\omega t + \varphi)$
Then: $\ddot{x}_i = -\omega^2 A_i \cos(\omega t + \varphi)$
Substitution chain:
$$-\omega^2 M\mathbf{x} + K\mathbf{x} = \mathbf{0}$$
$$-\lambda M\mathbf{x} + K\mathbf{x} = \mathbf{0}$$
$$K\mathbf{x} - \lambda M\mathbf{x} = \mathbf{0}$$
$$M^{-1}K\mathbf{x} = \lambda\mathbf{x}$$
Final solution (boxed): $x_i = \sum_j A_{ij}\cos(\omega_j t + \varphi_j)$ where i and j count degrees of freedom.

## Page 6
Note on matrices and solution. Coupling types:
- Static coupling: K not diagonal (like translational motion of masses with springs)
- Dynamic coupling: M not diagonal (e.g. trolley pendulum system)
Three equivalent eigenproblem forms (Thomson 5.3):
Left: $\lambda = \omega^2$, $K\mathbf{x} - \lambda M\mathbf{x} = \mathbf{0}$, boxed $(M^{-1}K - \lambda I)X = 0$
Centre: $-\omega^2 M\mathbf{x} + K\mathbf{x} = \mathbf{0}$
Right: $(\frac{1}{\omega^2}K - M)X = 0$, $\mu = \frac{1}{\omega^2}$, $D = K^{-1}M$, boxed $(\mu I - D)X = 0$

## Page 7
We can do it in Matlab! Matlab can solve equations of the type $KX - \lambda MX = 0$. The code is [eigvector,eigvalue] = eig(K, M), remember to get omega back from substitution.
System: two masses m1, m2 between three springs k1, k2, k3 fixed at both walls.
For m1 = m2 = 1.0 kg, all k = 1.0 N/m:
$$M = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad K = \begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix}$$
Matlab output: eigvect = [-0.7071 -0.7071; -0.7071 0.7071], eigvalue = [1 0; 0 3].
FIGURE-CROP: page=7 box=990,120,500,190 name=fig01_two_mass_three_spring caption=Two mass three spring system between fixed walls

## Page 8
Matlab solution, what it means. Same system and code. eigvalues = [1 0; 0 3] are $\omega^2$; eigenvectors columns [1 1] and [1 -1] (normalised -0.7071 values scaled). $\omega_1 = 1$ rad/s and $\omega_2 = 1.7$ rad/s (sqrt(3) = 1.7321).

## Page 9
Key statement slide: Eigenvalue defines mode frequency. Eigenvector defines mode shape.

## Page 10
2 inertia system demo, spring and carts. eigval = [1 0; 0 3], omega = [1.0000 0; 0 1.7321], eigvect columns circled: [1.0000 1.0000] and [1.0000 -1.0000].
Mode shape sketches: mode 1 both amplitudes A1, A2 equal and in phase (horizontal line); mode 2 A1 up, A2 down (crossing line, out of phase).
General solution:
$$\{x\} = \begin{Bmatrix} x_1(t) \\ x_2(t) \end{Bmatrix} = C_1 \begin{Bmatrix} A_1^{(1)} \\ A_2^{(1)} \end{Bmatrix}\cos(\omega_1 t - \varphi_1) + C_2 \begin{Bmatrix} A_1^{(2)} \\ A_2^{(2)} \end{Bmatrix}\cos(\omega_2 t - \varphi_2)$$
FIGURE-CROP: page=10 box=740,240,560,530 name=fig02_mode_shape_sketch caption=Mode shape sketches for the two cart system, in phase and out of phase

## Page 11
2 inertia, free free. Start with very simple example: 2 disks on a shaft (hand sketch: disks I1, I2 joined by shaft stiffness K). Twist in opposite directions, then let go. Isolated so momentum (H) conserved; disks move opposite ways; they come to origin at the same times; ONE natural frequency, one node. (Second mode frequency = 0.) Zero frequency mode: Tongue 4.15. Thought bubble: 2 inertias, so where is the 2nd mode?
FIGURE-CROP: page=11 box=1210,300,450,420 name=fig03_two_disk_shaft caption=Two disks on a shaft with stiffness K, hand sketch

## Page 12
3 inertia system demo, rope! For m1 = m2 = m3 = 1.0 kg, all k = 1.0 N/m:
eigval diag = [0.5858, 2.0000, 3.4142]; omega = [0.7654, 1.4142, 1.8478];
eigvect columns = [0.7071 -1.0000 -0.7071; 1.0000 0.0000 1.0000; 0.7071 1.0000 -0.7071] (first column circled).
Mode shape sketches for three masses A1, A2, A3: mode 1 all same side with A2 largest; mode 2 A1 up through zero at A2 to A3 down (node at middle mass); mode 3 A1 and A3 same side, A2 opposite (two nodes).
FIGURE-CROP: page=12 box=870,170,600,800 name=fig04_three_mass_modes caption=Mode shapes of the three mass rope demo

## Page 13
Coupled Air Carts demo slide: photo of an air track apparatus. Video link https://youtu.be/zlzns5PjmJ4. No further technical content.

## Page 14
Physical intuitions:
- Number of modes = Degrees of Freedom.
- Finite number of degrees of freedom means a finite number of basic stable patterns of motion; but many forms of transient motion are possible.
- A stable motion requires all inertias have the same oscillatory frequency.
- If all inertias have the same stable frequency, then they must move in phase or antiphase, or the spring forces change their balance and the motion will alter.
- For similar amplitudes, more energy is needed to create a mode with more nodes.
- At most one node between two adjacent inertias (or inertia and wall). With n modes, n-1 nodes.

## Page 15
Superposition principle:
- Stable patterns happen only at certain natural frequencies.
- If the system is (modelled as) linear, these simple patterns can be superposed to show other patterns.
- Natural frequency and mode shapes depend only on the particular configuration of stiffness and inertias; independent of initial conditions (within reason, too much energy and it breaks, linearity breaks down).
Right figure: low frequency envelope + fast oscillation = amplitude modulated sum (three stacked amplitude vs t plots).

## Page 16
Initial conditions! Actual motion depends on initial conditions. Initial conditions specify available energy (work). Can reinforce one of the modes (and suppress others).
$$\{x\} = \begin{Bmatrix} x_1(t) \\ x_2(t) \end{Bmatrix} = C_1\begin{Bmatrix} A_1^{(1)} \\ A_2^{(1)} \end{Bmatrix}\cos(\omega_1 t - \varphi_1) + C_2\begin{Bmatrix} A_1^{(2)} \\ A_2^{(2)} \end{Bmatrix}\cos(\omega_2 t - \varphi_2)$$
with the two column vectors labelled Eigenvector (1) and Eigenvector (2).

## Page 17
2 inertia system, full solution. Same content as page 10 (eigval [1 0; 0 3], omega [1.0000 0; 0 1.7321], eigvect columns [1 1] and [1 -1] circled, mode sketches, general solution equation). Repeat slide, no new content.

## Page 18
Mode superposition, what if omega1 is approximately omega2. The sum of two cosines can be rewritten as product:
$$\cos\omega_1 t + \cos\omega_2 t = 2\cos\frac{\omega_1+\omega_2}{2}\cos\frac{\omega_1-\omega_2}{2}$$
(second factor highlighted: the slow envelope). Photo: two pendulums hanging from a common support (video http://youtu.be/RoSYKPTdlxs). Right: two near identical sine traces overlaid (http://goo.gl/zCcteh, by Adjwilley CC BY SA 3.0), note "Starting from omega1 = omega2, increase difference up to 25 percent".

## Page 19
Mode superposition, beat. Two stacked plots over t = 0 to 32 pi: fast oscillation (blue) inside slow envelope (red), envelope cos((omega1-omega2)t/2) in the top plot and sin((omega1-omega2)t/2) in the bottom plot; omega_{1,2} = (1 +/- 0.05) rad/s. Illustrates beating when frequencies are close.
FIGURE-CROP: page=19 box=200,180,1180,760 name=fig05_beat_envelopes caption=Beat phenomenon, fast oscillation inside slow cosine and sine envelopes

## Page 20
Summary (Unit 6 part 1):
- Free vibration in modes.
- A mode: all inertias same frequency, same phase, fixed amplitude ratios.
- Some modes have nodes.
- Generally we get a superposition of normal modes.
- Superposition: part of mode 1, part of mode 2, phase.
- Initial conditions: positions and velocities $x_1(t_0), \dot{x}_1(t_0), x_2(t_0), \dot{x}_2(t_0)$ determine how much of each mode.

## Page 21
Vevox join slide (vevox.app, ID 169-231-965). No technical content.

## Page 22
Heuristics (definition, highlighted): "Heuristics are the strategies derived from previous experiences with similar problems." Caption: patterns emerging.

## Page 23
Free Axial Vibration, general case setup. Diagram: three masses m1, m2, m3 between four springs k1..k4, walls both ends, displacements x1, x2, x3. "3 DoF is enough to show the general patterns for n DoF."
Energy terms:
$$T = \tfrac{1}{2}m_1\dot{x}_1^2 + \tfrac{1}{2}m_2\dot{x}_2^2 + \tfrac{1}{2}m_3\dot{x}_3^2$$
$$V = \tfrac{1}{2}k_1 x_1^2 + \tfrac{1}{2}k_2(x_1-x_2)^2 + \tfrac{1}{2}k_3(x_2-x_3)^2 + \tfrac{1}{2}k_4 x_3^2$$
General patterns: $T = \sum_{i=1}^{n}\tfrac{1}{2}m_i\dot{x}_i^2$, $V = \sum_{i=1}^{n}\tfrac{1}{2}k_i(x_i - x_{i-1})^2$
FIGURE-CROP: page=23 box=460,170,890,270 name=fig06_three_mass_four_spring caption=Three mass four spring axial system, the general 3 DoF setup

## Page 24
Free axial vibration, matrix form. For 3 DoF (Thomson 5.1):
$$\begin{bmatrix} m_1 & 0 & 0 \\ 0 & m_2 & 0 \\ 0 & 0 & m_3 \end{bmatrix}\begin{Bmatrix} \ddot{x}_1 \\ \ddot{x}_2 \\ \ddot{x}_3 \end{Bmatrix} + \begin{bmatrix} (k_1+k_2) & -k_2 & 0 \\ -k_2 & (k_2+k_3) & -k_3 \\ 0 & -k_3 & (k_3+k_4) \end{bmatrix}\begin{Bmatrix} x_1 \\ x_2 \\ x_3 \end{Bmatrix} = 0$$

## Page 25
Stiffness matrices for multi DOF mass spring system (heuristic rules, highlighted box):
- Diagonal element $K_{ii}$: the sum of stiffnesses of all springs connected to $M_i$.
- Other elements $K_{ij}$: negative stiffness of springs directly connected between $M_i$ and $M_j$; if there are two or more springs, take the equivalent element.
Shows the 2 DoF and 3 DoF matrix forms side by side as examples.

## Page 26
Same rules work for damping matrices:
- Diagonal element $C_{ii}$: the sum of damping coefficients of all damping elements connected to $M_i$.
- Other element $C_{ij}$: negative damping coefficients of dampers directly connected between $M_i$ and $M_j$; two or more dampers, take the equivalent element.
"We will build some on Friday."

## Page 27
Summary 3 DoF: from patterns for the 3 DoF axial system we derived rules for writing out energy terms; rules for m, k and c matrices; the same works for torsional motion.

## Page 28
Section divider: Torsional systems. No technical content.

## Page 29
Torsional Vibration, mode shapes (Rao 5.4, Thomson 5.1). The torsional lumped system: hand sketch of disks I1..In on a shaft with torsional stiffnesses K1..K(n+1), angles theta1..thetan, fixed at both ends. "Corresponds exactly to the axial one" (matching axial mass spring sketch below).
Generic energy terms:
$$T = \sum_{i=1}^{n}\tfrac{1}{2}I_i\dot{\theta}_i^2, \qquad V = \sum_{i=1}^{n}\tfrac{1}{2}K_i(\theta_i - \theta_{i-1})^2$$
FIGURE-CROP: page=29 box=430,230,1150,270 name=fig07_torsional_lumped caption=Torsional lumped system, disks on a shaft, corresponds exactly to the axial chain

## Page 30
Summary: free n DoF vibrations. Systems with n degrees of freedom have n modes. Modes characterised by frequency and amplitude ratios (modal shape). We can use the heuristic approach to build M, K and C matrices. Lagrange needs to be used for complex systems (linked motions). (Slide numbering in the deck jumps here; released PDF omits some slides.)

## Page 31
For the next class: equivalence problem via Lagrange and heuristics, build matrices for more complex systems with past exam papers, revisit equivalent damping, practice calculating number of DoF. Watch the videos. Challenge task reading: Rao example 6.11 (p.629) finding frequencies and mode shapes in 3 DoF; Rao 6.14 (p.641) free free translational system 3 DoF; Rao 6.15 (p.644) using initial conditions for example 6.11.

<!-- EXTRACTION COMPLETE: 31 pages -->
