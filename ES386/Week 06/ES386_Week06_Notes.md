# ES386 Week 6 Notes: Free Multiple Degree of Freedom Vibration and Modal Analysis

Module: ES386 Dynamics of Vibrating Systems. Covers Unit 6 (free n DoF vibration, undamped lumped model) and Unit 7 (modal analysis for multiple DoF systems), plus the mode shapes worksheet and the coupled 2 DoF car handout. This markdown is the recall source for tutor mode.

## 1. Introduction: modes and modal analysis

For any object, each natural frequency together with its corresponding vibrational shape (its eigenvector) defines one **normal mode**, usually just called a **mode**. Modes are inherent physical properties: they are set by the mass, damping and stiffness and by the boundary conditions, and are independent of the initial conditions. The initial conditions only decide which modes are excited and with what amplitude and phase; each mode is always present even when its amplitude is negligible.

Modal analysis matters because a structure driven near one of its natural frequencies can deform hugely under a very small force, which can destroy it (the Tacoma Narrows bridge failed in November 1940 because the twisting mode at a different natural frequency was missed; the Ferrybridge cooling towers failed in 1965 because grouping modes were missed; aeroplane wings must be checked for flutter). The goal of modal analysis is to find the natural frequencies and mode shapes and then predict the response to external forcing.

## 2. Equation of motion for a multiple DoF system

A lumped undamped system with n degrees of freedom has the matrix equation of motion
$$M\ddot{\mathbf{x}} + K\mathbf{x} = \mathbf{0}$$
M: mass matrix (kg), K: stiffness matrix (N/m), x: displacement vector (m).

For a chain of masses and springs the matrices follow heuristic rules:
- Diagonal $K_{ii}$ = sum of the stiffnesses of all springs connected to mass i.
- Off diagonal $K_{ij}$ = negative of the stiffness directly connecting masses i and j (equivalent stiffness if several).
- The same rules build the damping matrix C from damper coefficients.
- For a diagonal (no dynamic coupling) system with equal masses, $M = mI$.

## 3. Free n DoF vibration: the eigenvalue problem

Assume the trial solution $x_i = A_i\cos(\omega t + \varphi)$, so $\ddot{x}_i = -\omega^2 A_i\cos(\omega t + \varphi)$. Substituting into the equation of motion gives, with $\lambda = \omega^2$,
$$(-\omega^2 M + K)\mathbf{x} = \mathbf{0} \;\Rightarrow\; (M^{-1}K - \lambda I)\mathbf{x} = \mathbf{0}$$
This is a standard eigenvalue problem with $A = M^{-1}K$. An n by n diagonalisable A has n eigenvalue eigenvector pairs $\{\lambda_i = \omega_i^2, \mathbf{v}_i\}$, the normal modes. The general free response is a superposition of them:
$$\mathbf{x}(t) = \sum_{i=1}^{n} A_i\mathbf{v}_i\cos(\omega_i t + \phi_i)$$
The eigenvalue sets the mode frequency; the eigenvector sets the mode shape.

**Coupling types.** Static coupling means K is not diagonal (masses joined by springs). Dynamic coupling means M is not diagonal (for example a trolley with a pendulum). Three equivalent eigenproblem forms exist: $(M^{-1}K - \lambda I)X = 0$ with $\lambda = \omega^2$, and $(\mu I - D)X = 0$ with $\mu = 1/\omega^2$ and $D = K^{-1}M$.

## 4. Physical intuitions and mode shapes

- Number of modes = number of degrees of freedom.
- A finite number of degrees of freedom gives a finite number of stable patterns, though many transient motions are possible.
- A stable motion needs every inertia to share one oscillation frequency, so they move in phase or in antiphase.
- More nodes need more energy, so higher modes have higher frequency. With n modes there are at most n minus 1 nodes, at most one node between adjacent inertias.
- If the system is linear these patterns superpose. The natural frequencies and mode shapes depend only on the stiffness and inertia configuration, not on the initial conditions.

For a three mass three spring chain with unit m and k the MATLAB solver gives eigenvalues 0.5858, 2.0000, 3.4142, so $\omega = 0.77, 1.41, 1.85$ rad/s. Mode 1 has all masses on the same side (no interior node); mode 2 is antisymmetric with one node at the centre; mode 3 alternates with two nodes. See `figures/fig08_three_dof_mode_shapes.png`.

## 5. The limitation of the standard approach

The standard approach ($A = M^{-1}K$) works beautifully when the system is symmetric (equal masses and stiffnesses). It fails as soon as the masses differ. With $m_1 = 1, m_2 = 2, m_3 = 3$ and unit k,
$$A = M^{-1}K = \begin{bmatrix} 2 & -1 & 0 \\ -1/2 & 1 & -1/2 \\ 0 & -1/3 & 2/3 \end{bmatrix} \neq A^T$$
A is not symmetric, so its eigenvalues need not be real and the method breaks. The fix is to change coordinates so the single matrix in the equation of motion is symmetric.

## 6. Generalised eigenvalue problem

The equation of motion can instead be solved directly as the generalised eigenvalue problem
$$(-\omega^2 M + K)\mathbf{x} = \mathbf{0}$$
solvable by hand or with MATLAB `eig(K, M)`. This keeps the symmetry of M and K, but it would be neater still to have a single symmetric matrix.

Useful eigenvalue and symmetric matrix facts: the eigenvalues of a triangular or diagonal matrix are its diagonal entries; $\lambda = 0$ is an eigenvalue of a singular matrix; B and $B^T$ share eigenvalues; a real symmetric matrix has real eigenvalues and orthogonal eigenvectors (for distinct eigenvalues); positive definiteness ($\mathbf{v}^T B\mathbf{v} > 0$) is equivalent to positive eigenvalues, which is assumed because natural frequencies are roots of eigenvalues.

## 7. Mass normalised coordinates

Since M is diagonal, its matrix square root is $M^{1/2} = \mathrm{diag}(\sqrt{m_i})$ with inverse $M^{-1/2} = \mathrm{diag}(1/\sqrt{m_i})$. Define mass normalised coordinates
$$\mathbf{q} := M^{1/2}\mathbf{x} \iff \mathbf{x} = M^{-1/2}\mathbf{q}$$
Substituting reduces the equation of motion to
$$\ddot{\mathbf{q}} + \widetilde{K}\mathbf{q} = \mathbf{0}, \qquad \widetilde{K} := M^{-1/2}K M^{-1/2}$$
$\widetilde{K}$, the mass normalised stiffness matrix, is symmetric for all symmetric M and K, so the equation of motion is now written with a single symmetric matrix.

## 8. Normal coordinates and the modal matrix

$\widetilde{K}$ is symmetric but its components are still coupled. Let P be the matrix of eigenvectors of $\widetilde{K}$ and transform to normal coordinates
$$\mathbf{r} := P^T\mathbf{q} \iff \mathbf{q} = P\mathbf{r}$$
Substituting gives $\ddot{\mathbf{r}} + \Lambda\mathbf{r} = \mathbf{0}$ with $\Lambda = \mathrm{diag}(\lambda_i)$, so
$$\ddot{r}_i + \omega_i^2 r_i = 0 \iff r_i(t) = A_i\cos(\omega_i t + \phi_i)$$
Because $\widetilde{K}$ is real symmetric its eigenvectors are orthogonal, so the coupled matrix equation is decoupled into n independent modal equations.

**Modal matrix.** To do both transforms at once define $S := M^{-1/2}P$, so $\mathbf{x} = S\mathbf{r}$ and initial conditions map with $\mathbf{r}_0 = S^{-1}\mathbf{x}_0$. Each modal coordinate then follows
$$r_i(t) = \mathrm{sign}(r_{i0})\sqrt{r_{i0}^2 + \frac{\dot{r}_{i0}^2}{\omega_i^2}}\cos\!\left(\omega_i t - \mathrm{atan}\frac{\dot{r}_{i0}}{\omega_i r_{i0}}\right)$$
Then transform back with $\mathbf{x} = S\mathbf{r}$. Exciting a single modal coordinate gives a pure mode (all masses at one frequency); a physical initial condition excites several modes whose superposition looks complicated even though each modal coordinate is a clean cosine (see `figures/fig10_mixed_mode_response.png`).

The full modal recipe: change coordinates x to q, solve the symmetric eigenvalue problem for $\widetilde{K}$, change coordinates q to r, solve with the transformed initial conditions, then map results back r to x.

## 9. Torsional and free free systems

A torsional lumped system (disks $I_i$ on a shaft with torsional stiffnesses $K_i$, angles $\theta_i$) corresponds exactly to the axial mass spring chain (see `figures/fig07_torsional_lumped.png`), with energies
$$T = \sum_{i=1}^{n}\tfrac{1}{2}I_i\dot{\theta}_i^2, \qquad V = \sum_{i=1}^{n}\tfrac{1}{2}K_i(\theta_i - \theta_{i-1})^2$$

A **free free** system (no anchoring) always has a rigid body mode at $\omega = 0$ where every inertia moves together. Two disks twisted oppositely then released share momentum, move oppositely, and return together: one natural frequency and one node, with the second mode at zero frequency. A three inertia free free system has a zero frequency rigid mode plus two vibrating modes.

## 10. Beats and mode superposition

When two modal frequencies are close the sum of two cosines rewrites as a slow envelope times a fast carrier:
$$\cos\omega_1 t + \cos\omega_2 t = 2\cos\frac{\omega_1 - \omega_2}{2}t\;\cos\frac{\omega_1 + \omega_2}{2}t$$
The slow factor is the beat envelope. With $\omega_{1,2} = (1 \pm 0.05)$ rad/s the fast oscillation sits inside a slow cosine or sine envelope (see `figures/fig05_beat_envelopes.png`), the classic coupled pendulum beat.

## 11. Key Summary

- Equation of motion for n DoF: $M\ddot{\mathbf{x}} + K\mathbf{x} = \mathbf{0}$.
- Trial solution $\mathbf{x} = \mathbf{x}_0\cos(\omega t + \phi)$ gives the eigenvalue problem $(M^{-1}K - \omega^2 I)\mathbf{x} = \mathbf{0}$.
- Standard approach works only when $M^{-1}K$ is symmetric; it fails for unequal masses.
- Mass normalised stiffness $\widetilde{K} = M^{-1/2}K M^{-1/2}$ is always symmetric.
- Normal coordinates $\mathbf{r} = P^T\mathbf{q}$ (P eigenvectors of $\widetilde{K}$) decouple the system into modal equations $\ddot{r}_i + \omega_i^2 r_i = 0$.
- Modal matrix $S = M^{-1/2}P$ does both transforms at once: $\mathbf{x} = S\mathbf{r}$, $\mathbf{r}_0 = S^{-1}\mathbf{x}_0$.
- Number of modes = number of DoF; n modes have at most n minus 1 nodes; higher modes have more nodes and higher frequency.
- Free free systems always carry a zero frequency rigid body mode.
- Close frequencies produce beats.

## 12. Worked Examples Q&A

### Worked Example 1: 2 DoF mode shapes (worksheet Exercise 1)
Question. A 2 DoF system has $M = I$ kg and $K = \begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}$ N/m. Verify $\omega_1 = \sqrt{2}$ and $\omega_2 = 2$ rad/s are natural frequencies, find and sketch the mode shapes, and count the nodes.

Step 1: form A. Since $M = I$, the eigenvalue matrix is $A = M^{-1}K = K$.
Step 2: test the claimed frequencies as eigenvalues. With $\lambda_1 = \omega_1^2 = 2$ and $\lambda_2 = \omega_2^2 = 4$, solve $(K - \lambda I)\mathbf{v} = 0$ for each.
Step 3: solve for the eigenvectors. $\lambda = 2$ gives $v_1 = (1, 1)^T$; $\lambda = 4$ gives $v_2 = (1, -1)^T$. Both eigenvector equations are consistent, confirming the eigenvalues.
Result. Natural frequencies $\sqrt{2}$ and 2 rad/s are verified. Mode 1 (both masses moving together) has no node; mode 2 (masses in antiphase) has one node between them. Higher frequency carries the extra node.

### Worked Example 2: free free drivetrain (worksheet Exercise 2)
Question. A drivetrain modelled free free has mass matrix $\mathrm{diag}(I_1, 2I_2, I_1)$ and stiffness $\begin{pmatrix} k_1 & -k_1 & 0 \\ -k_1 & 2k_1 & -k_1 \\ 0 & -k_1 & k_1 \end{pmatrix}$. Describe the $\omega = 0$ mode, test $\omega_1 = \sqrt{k_1/I_1}$, and predict any further mode.

Step 1: identify the rigid mode. Any free free system has an $\omega = 0$ mode where all inertias rotate at the same angular velocity, the free wheel mode.
Step 2: test $\omega_1$ by substitution. Put $\theta_i = A_i\sin(\omega_1 t)$ with $\omega_1^2 = k_1/I_1$ into the three rows.
Step 3: read the amplitude ratios. Row 1 gives $k_1 A_2 = 0$ so $A_2 = 0$; row 2 gives $A_1 = -A_3$; row 3 is consistent. So $\omega_1$ is genuine: outer inertias move equally and oppositely while the middle inertia is still (one node).
Step 4: count remaining modes. Three DoF need three modes; found frequencies 0 and $\sqrt{k_1/I_1}$ with zero and one nodes, so one mode remains, with two nodes (outer inertias together, middle opposite).
Result. The model is consistent with $\omega_1 = \sqrt{k_1/I_1}$. The missing third mode has two nodes, and since more nodes mean higher frequency, $\omega_2 > \omega_1$.

### Worked Example 3: torsional three inertia (worksheet Exercise 3)
Question. A light shaft carries three inertias with $\ddot{\boldsymbol{\theta}} + \begin{pmatrix} 2 & -2 & 0 \\ -2 & 3 & -1 \\ 0 & -1 & 1 \end{pmatrix}\boldsymbol{\theta} = \mathbf{0}$. The two natural frequencies satisfy $\omega_n^2 = 3 \pm \sqrt{3}$. Find the mode shapes normalised to $\theta_1 = 1$ and comment on the number of modes.

Step 1: recognise the structure. Eigenvectors give the mode shapes, eigenvalues give $\omega_n^2$. Set $A_1 = 1$ and solve $(K - \omega_n^2 I)\mathbf{A} = 0$.
Step 2: read $A_2$ from the top row. The first row $2 - 2A_2 = \omega_n^2$ gives $A_2 = (2 - \omega_n^2)/2$, that is $A_2 = \mp(\sqrt{3} \mp 1)/2$ for the two roots.
Step 3: read $A_3$ from the bottom row. The last row $-A_2 + A_3 = \omega_n^2 A_3$ gives $A_3$ once $A_2$ is known.
Result. Mode 1 (for $\omega_n^2 = 3 - \sqrt{3}$): $\left(1, \tfrac{\sqrt{3}-1}{2}, -\tfrac{\sqrt{3}-1}{2(2-\sqrt{3})}\right)$. Mode 2 (for $3 + \sqrt{3}$): $\left(1, -\tfrac{\sqrt{3}+1}{2}, \tfrac{\sqrt{3}+1}{2(2+\sqrt{3})}\right)$. Three inertias in a free free system give only two vibration modes; the third is the rigid body rotation at $\omega_n = 0$.

### Worked Example 4: modal analysis of a three mass chain (Unit 7 slides)
Question. Three equal masses $m = 4$ kg on springs $k = 4$ N/m against a fixed wall, released from $x_1(0) = 1$ with all other displacements and all velocities zero. Determine the normal modes and the evolution x(t).

Step 1: build the modal matrix. Solve the symmetric eigenvalue problem for $\widetilde{K} = M^{-1/2}K M^{-1/2}$ to get eigenvalues $\omega_i^2$ and eigenvector matrix P, then $S = M^{-1/2}P$.
Step 2: transform the initial conditions. Compute $\mathbf{r}_0 = S^{-1}\mathbf{x}_0$ and $\dot{\mathbf{r}}_0 = S^{-1}\dot{\mathbf{x}}_0 = \mathbf{0}$.
Step 3: write each modal solution. With zero initial modal velocity each modal coordinate is a pure cosine $r_i(t) = r_{i0}\cos(\omega_i t)$ at its own frequency.
Step 4: map back to physical coordinates. Combine with $\mathbf{x}(t) = S\mathbf{r}(t)$.
Result. The messy looking physical motion is a superposition of three clean modal cosines at the three natural frequencies; exciting a single modal coordinate reproduces one pure mode shape.

## 13. Revision Questions and Answers

### Question 1: car pitch and bounce (coupled 2 DoF handout)
Question. A car of mass 1600 kg has moment of inertia 2300 kg m^2 about its centre of mass, located 1.70 m behind the front wheels and 1.35 m in front of the rear wheels. Rear suspension $k_1 = 30.0$ kN/m, front $k_2 = 35.0$ kN/m. (i) Choose coordinates that avoid dynamic coupling if possible. (ii) Find the normal mode frequencies. (iii) Locate the node of each mode.

Answer. (i) Use the vertical bounce z of the centre of mass and the pitch angle $\theta$. The equations couple through terms in $(k_2 l_2 - k_1 l_1)$; dynamic coupling is avoided when this term vanishes, so bounce and pitch decouple only if $k_1 l_1 = k_2 l_2$. Here $k_1 l_1 = 30.0 \times 1.35 = 40.5$ kN and $k_2 l_2 = 35.0 \times 1.70 = 59.5$ kN, which are unequal, so the two motions are statically coupled and must be solved together.
(ii) Form the mass matrix $\mathrm{diag}(m, I)$ and the stiffness matrix
$$K = \begin{bmatrix} k_1 + k_2 & k_2 l_2 - k_1 l_1 \\ k_2 l_2 - k_1 l_1 & k_1 l_1^2 + k_2 l_2^2 \end{bmatrix}$$
Solve $\det(K - \omega^2 M) = 0$ for the two normal mode frequencies (one predominantly bounce, one predominantly pitch).
(iii) Each mode has a node, the point along the car that stays still. Its distance from the centre of mass follows from the amplitude ratio $z/\theta$ of that eigenvector: the node sits where the bounce and pitch contributions cancel. The lower frequency mode places its node outside or near one axle, the higher frequency mode places its node between the axles.

### Question 2: free vibration by modal analysis (Rao Example 6.16)
Question. A 2 DoF system has $\mathrm{diag}(m_1, m_2)$ and $\begin{pmatrix} k_1+k_2 & -k_2 \\ -k_2 & k_2+k_3 \end{pmatrix}$ with $m_1 = 10, m_2 = 1, k_1 = 30, k_2 = 5, k_3 = 0$, released from $\mathbf{x}(0) = (1, 0)^T$ with zero velocity. Find the free vibration response.

Answer.
Step 1: assemble the matrices. $M = \mathrm{diag}(10, 1)$, $K = \begin{pmatrix} 35 & -5 \\ -5 & 5 \end{pmatrix}$.
Step 2: mass normalise. $M^{-1/2} = \mathrm{diag}(1/\sqrt{10}, 1)$, giving $\widetilde{K} = M^{-1/2}K M^{-1/2} = \begin{pmatrix} 3.5 & -5/\sqrt{10} \\ -5/\sqrt{10} & 5 \end{pmatrix}$.
Step 3: solve the symmetric eigenvalue problem for $\widetilde{K}$ to get $\omega_1^2, \omega_2^2$ and the orthogonal eigenvectors P, then the modal matrix $S = M^{-1/2}P$.
Step 4: transform the initial conditions with $\mathbf{r}_0 = S^{-1}\mathbf{x}_0$ and $\dot{\mathbf{r}}_0 = \mathbf{0}$.
Step 5: write the modal solutions $r_i(t) = r_{i0}\cos(\omega_i t)$ and map back with $\mathbf{x}(t) = S\mathbf{r}(t)$.
Result. The response is the sum of the two modes, each oscillating at its own natural frequency, weighted by how strongly the initial displacement projects onto each mode shape.

### Question 3: mode shape sketch and node count
Question. For a symmetric n DoF chain, how many nodes does each mode carry and how does frequency order relate to node count?

Answer. Mode number j (ordered by increasing frequency) carries j minus 1 interior nodes, at most one between adjacent masses. The fundamental has none, the highest mode has n minus 1. Since creating an extra node costs more strain energy for a given amplitude, node count rises with frequency, so counting nodes is a quick check on the mode order and on which sketch belongs to which frequency.
