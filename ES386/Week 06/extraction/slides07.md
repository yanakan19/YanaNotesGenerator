# Extraction: ES386_unit_07_slides_MFF_released (1).pdf (55 pages, 150 DPI)

## Page 1
Title slide: ES386 Dynamics of Vibrating Systems, Part II: Multiple DoF systems (Units 7 to 12), Dr Michael Faulkner. No technical content.

## Page 2
Practical arrangements. Contact: discussion forum on the ES386 Moodle page; email michael.faulkner@warwick.ac.uk. Office hours: Tuesdays and Fridays 14:00 to 15:00 in D211. In person sessions: lectures Tuesdays and Thursdays; worked examples on Fridays; all on Moodle or LectureCapture; lecture videos of the previous lecturer also available.

## Page 3
Moodle resources: PDFs of lecture slides; PDFs of what is written in lectures and example sessions; weekly activities (quizzes, example questions); other resources (MATLAB examples, simulations); MATLAB is NOT on the exam but is used for the computational assignment; previous lecture videos in 15 to 20 minute chunks; some units have non examinable example sheets with solutions; past exam papers. Reading list: Rao textbook (as in Part I). Assignment: the computational assignment requires modal analysis (Units 7 and 10), forced vibration (Unit 8), convolution method (Unit 9), the material of the first three weeks.

## Page 4
Overview of Part II. Week 20: Unit 7 modal analysis for multiple DOF systems. Week 21: Unit 8 forced vibration and applications. Week 22: Unit 9 non periodic vibration, Unit 10 modal analysis for forced and damped systems. Week 23: Unit 11 continuous systems, Unit 12 approximate methods (Rayleigh and Dunkerley approaches).

## Page 5
Notation. Scalars: $x, x_1$. Angles: $\theta, \theta_1$. Matrices: bold $\mathbf{A}, \mathbf{B}, \mathbf{A}^T, \mathbf{A}^{-1}$ (some textbooks $[A], [B], [A]^T, [A]^{-1}$). Vectors: bold $\mathbf{x}, \mathbf{q}, \mathbf{x}_1$, column braces $\{1\ 2\ 3\}^T$ (some textbooks $\{x\}, \{q\}, \{x_1\}$). Time derivatives: $\dot{x}, \dot{\theta}, \dot{\mathbf{x}}, \ddot{\mathbf{x}}$. Complex numbers: $x + jy$, $j = \sqrt{-1}$ (some textbooks use i).

## Page 6
Unit 7 title slide: Modal analysis for multiple DoF systems, Dr Michael Faulkner. No technical content.

## Page 7
Transition slide: "So what do we mean by a mode?" No technical content.

## Page 8
Introduction and motivation. For any object, each natural frequency and the corresponding vibrational shape (its eigenvector) defines one of its normal modes; each normal mode is often simply called a mode.

## Page 9
Introduction and motivation: animation still of the (1, 2) mode of a circular disc with fixed boundaries (video by Oleg Alexandrov). Mesh disc figure. No further technical content.

## Page 10
Introduction and motivation (full slide, deck footer MFF7:12; the released PDF omits some animation frames so PDF pages and footer numbers diverge from here). Natural frequency + eigenvector = normal mode; each normal mode is simply called a mode. Important because: if a mechanical structure is excited by an oscillating external force near one of its natural frequencies, very small force magnitudes can cause significant deformation. This can damage the structure (e.g. Tacoma Bridge) so resonant vibrations typically need avoiding in engineering. The key goal of modal analysis: identify the natural frequencies and modal shapes, then model the responses of the object to external resonant forces.

## Page 11
Important: modes are inherent properties! Modes are inherent physical properties: they depend on the material structure, composition and boundary conditions, and are INDEPENDENT of the initial conditions. The initial conditions decide which modes are excited and when (their amplitude of vibration and phase). But each mode is always present, even if the ICs mean its amplitude is negligible.

## Page 12
Transition slide: before modelling, some important examples of resonance. No technical content.

## Page 13
Tacoma bridge. The bridge collapsed in November 1940, a few months after opening, due to wind induced vibrational twisting. Two historical photos (twisting deck; deck failing). Due to: failure to predict the twisting mode of vibration (they successfully predicted the undulating mode but missed the twisting mode at a DIFFERENT natural frequency).

## Page 14
Aeroplane flutter: NASA Dryden Flight Research Center video still, PA-30 Twin Comanche tail flutter test (5 April 1966). Video: https://www.youtube.com/watch?v=iTFZNrTYp3k. No further technical content.

## Page 15
Testing and modelling (aeroplane flutter). Wings can be subject to flutter phenomena during flight, so before a new aeroplane is released, testing and modelling must detect the possible onset of flutter. Wind tunnel testing under similar flight conditions is possible but expensive; even a few input parameters affect hundreds of parts of the wing structure, so it is important to estimate and model resonant frequencies and damping ratios beforehand. This does not eliminate test flights but saves time and money and gives deeper understanding of the prototype. Photo: instrumented wing model in a wind tunnel.

## Page 16
Ferrybridge Power Station. Three cooling towers collapsed on 1 November 1965 due to wind induced vibration in 85 mph storm conditions. Individual towers were designed and wind tunnel tested to withstand this, but modes due to GROUPING effects were missed. Two historical photos.

## Page 17
Modes, introductory summary (Rao Chapter 6). Modes are inherent physical properties: determined by the fundamental material properties (mass m, damping b, stiffness k) and boundary conditions of the structure. Each mode is defined by a natural frequency (eigenvalue squared) and mode shape (eigenvector). Modes are independent of the ICs, but the ICs decide when and if each mode activates.

## Page 18
Section divider: 7.1 Standard eigenvalue approach. No technical content.

## Page 19
Recap: matrix methods for multi DoF systems. Diagram: three equal masses m, four equal springs k between walls, displacements x1, x2, x3. 3 DoFs is enough to show the general pattern of an n DoF system:
$$T = \tfrac{1}{2}m\dot{x}_1^2 + \tfrac{1}{2}m\dot{x}_2^2 + \tfrac{1}{2}m\dot{x}_3^2$$
$$V = \tfrac{1}{2}kx_1^2 + \tfrac{1}{2}k(x_1-x_2)^2 + \tfrac{1}{2}k(x_2-x_3)^2 + \tfrac{1}{2}kx_3^2$$
From Lagrange's equation, problems of this type can be written with mass M and stiffness K matrices, $\mathbf{x} = (x_1, x_2, x_3)^T$:
$$\mathbf{M}\ddot{\mathbf{x}} + \mathbf{K}\mathbf{x} = 0$$

## Page 20
Recap continued. System equations for the equal m, equal k chain:
$$\mathbf{M} = \begin{bmatrix} m & 0 & 0 \\ 0 & m & 0 \\ 0 & 0 & m \end{bmatrix}, \quad \mathbf{K} = \begin{bmatrix} 2k & -k & 0 \\ -k & 2k & -k \\ 0 & -k & 2k \end{bmatrix}$$
No dynamical coupling and equal masses, so $\mathbf{M} = m\mathbf{I}$. $K_{ii}$ = sum of spring constants connected to mass i (the $x_i^2$ terms); $K_{ij}$ = value of the spring constant connecting masses $i \neq j$ (interaction terms).

## Page 21
Recap continued (same system). This system is statically coupled (masses coupled via the stiffness matrix K). The solution is a standard eigenvalue problem (as the matrix equation is symmetric). The standard approach is to substitute $\mathbf{A} = \mathbf{M}^{-1}\mathbf{K}$.

## Page 22
Transition: modes may still seem abstract, so look at the mode shapes of that 3 DoF system (for m = 1, k = 1 without loss of generality). No further content.

## Page 23
Mode shapes of the 3 DoF system (m = 1, k = 1). Using eig in MATLAB: $\lambda_1 = 0.5858$, $\lambda_2 = 2.000$, $\lambda_3 = 3.4142$, eigenvectors (columns, colour coded to the three mode shape plots):
$$V = \begin{bmatrix} 0.5000 & -0.7071 & -0.5000 \\ 0.7071 & 0.0000 & 0.7071 \\ 0.5000 & 0.7071 & -0.5000 \end{bmatrix}$$
$$\omega_1 = 0.76, \quad \omega_2 = 1.41, \quad \omega_3 = 1.85\ \mathrm{rad/s}$$
Three stacked plots show the mode shapes across positions 1 to 5 (walls at 1 and 5): mode 1 all masses same side (half sine), mode 2 antisymmetric with node at the middle mass, mode 3 alternating with two nodes.
FIGURE-CROP: page=23 box=95,270,570,510 name=fig08_three_dof_mode_shapes caption=MATLAB mode shapes of the 3 DoF chain, modes 1 to 3 top to bottom

## Page 24
Summary: standard eigenvalue problem.
1. Trial solution: $\mathbf{x}(t) = \mathbf{x}_0\cos(\omega t + \phi)$
2. Substituting into the matrix equation gives $(-\omega^2\mathbf{M} + \mathbf{K})\mathbf{x} = \mathbf{0}$
3. $\mathbf{A} = \mathbf{M}^{-1}\mathbf{K}$ gives the standard eigenvalue problem $(\mathbf{A} - \omega^2\mathbf{I})\mathbf{x} = \mathbf{0}$
4. An n by n diagonalisable matrix A has n eigenvalue eigenvector pairs $\{\lambda_i = \omega_i^2, \mathbf{v}_i : i = 1,\dots,n\}$ (the normal modes)
5. General solution is a superposition of the n normal modes:
$$\mathbf{x}(t) = \sum_{i=1}^{n} A_i\mathbf{v}_i\cos(\omega_i t + \phi)$$
where the amplitude $A_i$ and phase $\phi_i$ of mode i are set by the ICs.

## Page 25
But asymmetric systems pose a huge limitation. Suppose M and K are still symmetric but $m_2 = 2m_1$, $m_3 = 3m_1$. Only slightly different, but the standard approach fails. With $m_1 = 1, k = 1$:
$$\mathbf{M} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{bmatrix}, \quad \mathbf{K} = \begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix}$$
$$\Rightarrow \mathbf{A} = \mathbf{M}^{-1}\mathbf{K} = \begin{bmatrix} 2 & -1 & 0 \\ -\tfrac{1}{2} & 1 & -\tfrac{1}{2} \\ 0 & -\tfrac{1}{3} & \tfrac{2}{3} \end{bmatrix} \neq \mathbf{A}^T$$
A is not symmetric so its eigenvalues are not necessarily real, and the standard eigenvalue method fails.

## Page 26
BUT if we can transform our coordinate system such that the analogous matrix A in the new system is symmetric, we have circumvented the problem.

## Page 27
Transition: this is the topic of Thursday's lecture. No technical content.

## Page 28
Recap of Tuesday's lecture. The standard eigenvalue approach writes the simultaneous equations of motion as a single matrix equation, then defines A to transform to an eigenvalue equation. It works beautifully for symmetric systems (equal masses and spring stiffnesses) but fails even for non equal masses, because A becomes asymmetric even if M and K are symmetric. But the problem can be circumvented by transforming the coordinate system so the analogous A is symmetric.

## Page 29
Section divider: 7.2 Generalised eigenvalue problems. No technical content.

## Page 30
Generalised eigenvalue problems. Equation of motion $\mathbf{M}\ddot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{0}$ can be alternatively solved as a generalised eigenvalue problem:
$$-\omega^2\mathbf{M}\mathbf{x} + \mathbf{K}\mathbf{x} = \mathbf{0}$$
(with the same trial solution $\mathbf{x} = \mathbf{x}_0\cos(\omega t + \phi)$). Solvable by hand or in MATLAB. Key point: this retains the symmetry of the symmetric matrices M and K. Things would be even easier with a single symmetric matrix, so next: properties of eigenvalues and symmetric matrices.

## Page 31
Eigenvalue and eigenvector theorems.
- Theorem 1: if B is an n by n triangular matrix (upper, lower or diagonal), the eigenvalues of B are the diagonal entries of B.
- Theorem 2: $\lambda = 0$ is an eigenvalue of B if B is a singular (non invertible) matrix.
- Theorem 3: B and $B^T$ have the same eigenvalues.
- Theorem 4: eigenvalues of a real symmetric matrix are real.
- Theorem 5: eigenvectors of a real symmetric matrix are orthogonal, but only for distinct eigenvalues.
- Theorem 6: $|\det(\mathbf{B})| = \left|\prod_{i=1}^{n}\lambda_i\right|$, the product of the absolute values of the eigenvalues.

## Page 32
Properties of real symmetric matrices ($\mathbf{B} = \mathbf{B}^T$, real components):
1. Eigenvalues of B are all real numbers.
2. Eigenvectors of B are all real valued vectors.
3. Eigenvectors $\{\mathbf{v}_i\}$ are orthogonal: $\mathbf{v}_i \cdot \mathbf{v}_j = 0\ \forall i \neq j$.
4. Eigenvalues are positive if and only if B is positive definite ($\mathbf{v}^T\mathbf{B}\mathbf{v} > 0\ \forall \mathbf{v} \neq 0$); needed because natural frequencies are roots of eigenvalues, always assumed unless otherwise stated.
5. Eigenvectors form a basis which can expand arbitrary functions (the basis of modal expansion).
6. Goal: transform to a coordinate system such that the single matrix in the EoM is symmetric.

## Page 33
Matrix square root of M. $\mathbf{M} = \mathbf{M}^{1/2}\mathbf{M}^{1/2}$ and for diagonal M:
$$\mathbf{M}^{1/2} = \mathrm{diag}(\sqrt{m_1}, \sqrt{m_2}, \sqrt{m_3}), \qquad \mathbf{M}^{-1/2} = \mathrm{diag}(1/\sqrt{m_1}, 1/\sqrt{m_2}, 1/\sqrt{m_3})$$
with $\mathbf{M}^{1/2}\mathbf{M}^{-1/2} = \mathbf{I}$.

## Page 34
Section divider: 7.3 Matrix transformation I: mass normalised stiffness matrix (worked on the OHP). No further content.

## Page 35
Summary: mass normalised stiffness. EoM $\mathbf{M}\ddot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{0}$. Problem: $\mathbf{M}^{-1}\mathbf{K}$ is not symmetric for all M, K (eigenvalues therefore not necessarily real). Change to mass normalised coordinates:
$$\mathbf{q} := \mathbf{M}^{1/2}\mathbf{x} \iff \mathbf{x} = \mathbf{M}^{-1/2}\mathbf{q}$$
Substituting gives $\mathbf{M}^{-1/2}\mathbf{M}\mathbf{M}^{-1/2}\ddot{\mathbf{q}} + \mathbf{M}^{-1/2}\mathbf{K}\mathbf{M}^{-1/2}\mathbf{q} = \mathbf{0}$, which reduces to
$$\ddot{\mathbf{q}} + \widetilde{\mathbf{K}}\mathbf{q} = \mathbf{0}, \qquad \widetilde{\mathbf{K}} := \mathbf{M}^{-1/2}\mathbf{K}\mathbf{M}^{-1/2}$$
the mass normalised stiffness matrix. Key point: $\widetilde{\mathbf{K}}$ is symmetric for ALL symmetric M, K, so the EoM is written in terms of a single symmetric matrix.

## Page 36
Section divider: 7.4 Matrix transformation I example (in your own time). No further content.

## Page 37
Worked example (in your own time). For the 2 DOF system with $m_1 = 9$ kg, $m_2 = 1$ kg, $k_1 = 24$ N/m, $k_2 = 3$ N/m:
$$\begin{bmatrix} 9 & 0 \\ 0 & 1 \end{bmatrix}\begin{Bmatrix} \ddot{x}_1 \\ \ddot{x}_2 \end{Bmatrix} + \begin{bmatrix} 27 & -3 \\ -3 & 3 \end{bmatrix}\begin{Bmatrix} x_1 \\ x_2 \end{Bmatrix} = \begin{Bmatrix} 0 \\ 0 \end{Bmatrix}$$
(a) Solve the generalised eigenvalue problem $\det(-\omega^2\mathbf{M} + \mathbf{K}) = 0$ to determine the natural frequencies and mode shapes. Are they orthogonal?
(b) Construct the mass normalised stiffness matrix $\widetilde{\mathbf{K}} = \mathbf{M}^{-1/2}\mathbf{K}\mathbf{M}^{-1/2}$ and compute its eigenvalues and eigenvectors. Are the new eigenvectors orthogonal?
(c) Are the natural frequencies the same with both approaches?

## Page 38
Transition: the EoM is now in terms of a single symmetric matrix BUT the components of q are still coupled; hard to understand the dynamics, so can they be decoupled via an additional transformation?

## Page 39
Section divider: 7.5 Matrix transformation II: normal coordinates (on the OHP). No further content.

## Page 40
Summary: normal coordinates. EoM $\ddot{\mathbf{q}} + \widetilde{\mathbf{K}}\mathbf{q} = \mathbf{0}$ with $\widetilde{\mathbf{K}} := \mathbf{M}^{-1/2}\mathbf{K}\mathbf{M}^{-1/2}$. Problem: still coupled (each component of q depends on others). Define P, the matrix of eigenvectors of $\widetilde{\mathbf{K}}$, and transform to normal coordinates:
$$\mathbf{r} := \mathbf{P}^T\mathbf{q} \iff \mathbf{q} = (\mathbf{P}^T)^{-1}\mathbf{r} = \mathbf{P}\mathbf{r}$$
Substituting gives
$$\ddot{\mathbf{r}} + \boldsymbol{\Lambda}\mathbf{r} = \mathbf{0}, \qquad \boldsymbol{\Lambda} := \mathrm{diag}(\lambda_i)$$
the eigenvalue matrix of $\widetilde{\mathbf{K}}$. This gives $\ddot{r}_i + \omega_i^2 r_i = 0$ for every i, so $r_i(t) = A_i\cos(\omega_i t + \phi_i)$. Key point: $\widetilde{\mathbf{K}}$ is real symmetric so its eigenvectors are orthogonal; the matrix EoM is DECOUPLED into n independent EoMs (the modal equations).

## Page 41
Summary of coordinate systems (table):
| Property | Original coordinates x(t) | Mass normalised coordinates q(t) | Normal coordinates r(t) |
| Symmetric matrices (in general) | no | yes | yes |
| Orthogonal eigenvectors (in general) | no | yes | yes |
| Decoupled equations of motion (in general) | no | no | yes |

## Page 42
Transition: nice animations on Thursday if time allows. No technical content.

## Page 43
On Friday: 1. define one last matrix that performs both transforms at once; 2. work through an example problem. No further content.

## Page 44
Recap of Thursday's lecture. EoM $\mathbf{M}\ddot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{0}$. Problem: $\mathbf{M}^{-1}\mathbf{K}$ not symmetric for all symmetric M, K. Change to mass normalised coordinates $\mathbf{q} := \mathbf{M}^{1/2}\mathbf{x}$, giving $\ddot{\mathbf{q}} + \widetilde{\mathbf{K}}\mathbf{q} = \mathbf{0}$ with $\widetilde{\mathbf{K}} := \mathbf{M}^{-1/2}\mathbf{K}\mathbf{M}^{-1/2}$; $\widetilde{\mathbf{K}}$ symmetric but q still coupled. Define P (eigenvectors of $\widetilde{\mathbf{K}}$), transform to normal coordinates $\mathbf{r} := \mathbf{P}^T\mathbf{q}$, giving $\ddot{r}_i + \omega_i^2 r_i = 0$, $r_i(t) = A_i\cos(\omega_i t + \phi_i)$: the EoM is decoupled into n independent EoMs.

## Page 45
Plan for today (Friday): 1. define one last matrix performing both transforms at once; 2. animation of original and normal coordinates (Unit 7.6); 3. example problem. No further content.

## Page 46
Transition: define and manipulate the modal matrix on the OHP (Unit 7.5 continued). No technical content.

## Page 47
Summary: modal matrix. To transform at once, define the modal matrix:
$$\mathbf{S} := \mathbf{M}^{-1/2}\mathbf{P} \Rightarrow \mathbf{x} = \mathbf{S}\mathbf{r}$$
Useful for transforming initial conditions: $\mathbf{r}_0 = \mathbf{S}^{-1}\mathbf{x}_0$. After transforming the ICs:
$$r_i(t) = \mathrm{sign}(r_{i0})\sqrt{r_{i0}^2 + \frac{\dot{r}_{i0}^2}{\omega_i^2}}\cos\!\left(\omega_i t - \mathrm{atan}\!\left(\frac{\dot{r}_{i0}}{\omega_i r_{i0}}\right)\right)\ \forall i = 1,\dots,n$$
where sign($r_{i0}$) is +1 if $r_{i0} > 0$ and -1 if $r_{i0} < 0$. Useful for insight, and can transform back to $\mathbf{x} = \mathbf{S}\mathbf{r}$ after computing each $r_i(t)$.

## Page 48
Section divider: 7.6 Modal analysis worked example (in your own time, gives a nice animation for lecture). No further content.

## Page 49
Worked example setup. Three masses m on springs k against a wall (fixed left, free right end), displacements x1, x2, x3. Data: $m_1 = 4$ kg (all masses m = 4 kg), $k = 4$ N/m. ICs: $x_1(0) = 1$, $x_2(0) = 0$, $x_3(0) = 0$; all initial velocities zero. Task: determine the normal modes and system evolution x(t).
FIGURE-CROP: page=49 box=75,215,1360,330 name=fig09_worked_example_chain caption=Worked example chain, three masses with fixed left wall and free right end

## Page 50
Pure Mode 1 animation still: $\mathbf{r}_0 = \{0.5, 0, 0\}$, $\dot{\mathbf{r}}_0 = \mathbf{0}$. Mode arrows (1) omega = 0.45: all masses same direction; (2) omega = 1.25; (3) omega = 1.80. Displacement plot: all three masses oscillate slowly in phase (blue, orange, yellow); modal displacement plot: only $r_1$ (purple) active, cosine at omega1, others flat.

## Page 51
Pure Mode 2 animation still: $\mathbf{r}_0 = \{0, 0.5, 0\}$. Displacement plot: masses 1 and 3 out of phase with mass 2 pattern at omega2 = 1.25; modal plot: only $r_2$ (green) active.

## Page 52
Pure Mode 3 animation still: $\mathbf{r}_0 = \{0, 0, 0.3\}$. Displacement plot: fast alternating motion at omega3 = 1.80 (blue and orange antiphase, yellow small); modal plot: only $r_3$ (cyan) active.

## Page 53
Mixed mode animation still: physical IC $\mathbf{x}_0 = \{0.2, 0, 0\}$, $\dot{\mathbf{x}}_0 = \mathbf{0}$. Displacement plot: complicated non periodic looking motion of all three masses. Modal plot: all three modal coordinates active as clean cosines at omega1, omega2, omega3 (purple slow, green mid, cyan fast). Moral: messy physical motion is a superposition of three clean modal oscillations.
FIGURE-CROP: page=53 box=330,40,880,950 name=fig10_mixed_mode_response caption=Mixed mode response, messy physical displacements versus clean modal coordinates

## Page 54
Example question for Friday session: Rao Example 6.16, free vibration response using modal analysis. Two DoF system:
$$\begin{bmatrix} m_1 & 0 \\ 0 & m_2 \end{bmatrix}\begin{Bmatrix} \ddot{x}_1 \\ \ddot{x}_2 \end{Bmatrix} + \begin{bmatrix} k_1+k_2 & -k_2 \\ -k_2 & k_2+k_3 \end{bmatrix}\begin{Bmatrix} x_1 \\ x_2 \end{Bmatrix} = \vec{F} = \begin{Bmatrix} 0 \\ 0 \end{Bmatrix}$$
Data: $m_1 = 10$, $m_2 = 1$, $k_1 = 30$, $k_2 = 5$, $k_3 = 0$, ICs $\vec{x}(0) = \{1, 0\}$, $\dot{\vec{x}}(0) = \{0, 0\}$.

## Page 55
Summary (Unit 7): 1. Modal analysis changes a set of coupled N DoF equations to a set of decoupled 1 DoF equations: change coordinates (x to q); solve the symmetric eigenvalue problem (find eigenvalues of $\widetilde{\mathbf{K}}$); change coordinates again (q to r); solve using transformed initial conditions; get results back in original coordinates (r to x). 2. Next week: forced vibration.

<!-- EXTRACTION COMPLETE: 55 pages -->
