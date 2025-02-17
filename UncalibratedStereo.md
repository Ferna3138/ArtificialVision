# Uncalibrated Stereo

The main issue with the Stereo System we mentioned before is that we assume that we are working with a known fixed disparity, which might not be the case if we are not working with a Stereo Vision camera. If we were to take two pictures of an object from two random unknown positions, if we know the intrinsic parameters of the cameras, we can compute the translation and rotation of one camera with respect to the other and therefore, we can compute a 3D reconstruction of the object. This process is known as *Uncalibrated Stereo*.

![Uncalibrated Stereo Left](Images/UncalibratedTheory/Uncalibratedleft.png)

![Uncalibrated Stereo Right](Images/UncalibratedTheory/Uncalibratedright.png)

![Uncalibrated Stereo Overview](Images/UncalibratedTheory/UncalibratedScenario.png)

We can define the set of corresponding features (at least 8) in the left and right images: $(u_l^{(m)}, v_l^{(m)})$ and $(u_r^{(m)}, v_r^{(m)})$, these features can be extracted using SIFT, for example. Once found, we can find the relative rotation $R$ and translation $t$. Once found, this uncalibrated stereo system becomes calibrated.

## Epipolar Geometry

We define an *Epipole* as an image point of origin/pinhole of one camera as viewed by the other camera. The left camera has its own 3D coordinate frame \(O_l\) and so does the right one \(O_r\). It is the translation and rotation from one frame to the other.

![Epipolar Plane](Images/UncalibratedTheory/Epipolar%20Plane.png)

The projection of the center of the left camera on the right camera image, and vice versa, are referred to as the **Epipoles**, which are denoted as $(e_l, e_r)$, unique for a given stereo pair. The **Epipolar Plane** is composed of the cameras' origins $(O_l, O_r)$ and the point $P$. The base of the formed triangle passes through the epipoles; therefore, each point in the scene defines a unique epipolar plane.

### Epipolar Constraint

We can compute a normal vector $n$, which is the cross product between the unknown translation and the $X_l$ vector that corresponds to the point $P$ in the left coordinate frame.

```math
n = t \times X_l
```

![Epipolar Constraint](Images/UncalibratedTheory/Epipolar%20Constraint.png)

This normal vector should be perpendicular to $X_l$, so we use it as the epipolar constraint:

```math
X_l \cdot n = 0
```

Written in matrix-vector form:

```math
\begin{bmatrix} x_l & y_l & z_l \end{bmatrix} \begin{bmatrix} 0 & -t_z & t_y \\ t_z & 0 & -t_x \\ -t_y & t_x & 0 \end{bmatrix} \begin{bmatrix} x_l \\ y_l \\ z_l \end{bmatrix} = 0
```

As a reminder, $t_{3 \times 1}$ is the position of the Right Camera in the Left Camera's frame, and $R_{3 \times 3}$ is the orientation of the Left Camera in the Right Camera's frame.

```math
x_l = R x_r + t
```

```math
\begin{bmatrix} x_l \\ y_l \\ z_l \end{bmatrix} = \begin{bmatrix} r_{11} & r_{12} & r_{13} \\ r_{21} & r_{22} & r_{23} \\ r_{31} & r_{32} & r_{33} \end{bmatrix} \begin{bmatrix} x_r \\ y_r \\ z_r \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \\ t_z \end{bmatrix}
```

Substituting $(x_l, y_l, z_l)$ into the epipolar constraint, we get:

```math
\begin{bmatrix} x_l & y_l & z_l \end{bmatrix} \left( \begin{bmatrix} 0 & -t_z & t_y \\ t_z & 0 & -t_x \\ -t_y & t_x & 0 \end{bmatrix} \begin{bmatrix} r_{11} & r_{12} & r_{13} \\ r_{21} & r_{22} & r_{23} \\ r_{31} & r_{32} & r_{33} \end{bmatrix} \begin{bmatrix} x_r \\ y_r \\ z_r \end{bmatrix} \right) = 0
```

The product of:

```math
\begin{bmatrix} 0 & -t_z & t_y \\ t_z & 0 & -t_x \\ -t_y & t_x & 0 \end{bmatrix} \begin{bmatrix} r_{11} & r_{12} & r_{13} \\ r_{21} & r_{22} & r_{23} \\ r_{31} & r_{32} & r_{33} \end{bmatrix}
```

is known as the **Essential Matrix** $E$, which we can define as $E = T \times R$.

```math
\begin{bmatrix} x_l & y_l & z_l \end{bmatrix} \begin{bmatrix} e_{11} & e_{12} & e_{13} \\ e_{21} & e_{22} & e_{23} \\ e_{31} & e_{32} & e_{33} \end{bmatrix} \begin{bmatrix} x_r \\ y_r \\ z_r \end{bmatrix} = 0
```

## Essential Matrix

One of the main properties of the essential matrix is that it is possible to decompose it into the $T$ and $R$ matrices due to the fact that $T$ is a *Skew-Symmetric matrix* $(a_{ij} = -a_{ji})$ and $R$ is an *Orthonormal* matrix. This means that using **Singular Value Decomposition**, we can get the $T$ and $R$ matrices from $E$.

Summarizing, if $E$ is known, then we can calculate $T$ and $R$.

Since we do not know the values of $X_l$ and $X_r$, we cannot use the $X_l^T E X_r = 0$ formula, but what we do have are the projection points $u_l$ and $u_r$.

Now, $K_l$ and $K_r$ are $3 \times 3$ matrices, which multiplied by $E$ we call the **Fundamental Matrix** $F$:

```math
\begin{bmatrix} u_l & v_l & 1 \end{bmatrix} \begin{bmatrix} f_{11} & f_{12} & f_{13} \\ f_{21} & f_{22} & f_{23} \\ f_{31} & f_{32} & f_{33} \end{bmatrix} \begin{bmatrix} u_r \\ v_r \\ 1 \end{bmatrix} = 0
```

Therefore, we define the essential matrix as:

```math
E = K_l^T F K_r
```
