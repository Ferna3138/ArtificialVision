#Simple Stereo

Given that the camera is calibrated, we can find the 3D scene point from a single 2D image. Going from 3D to 2D (point):
```math
\begin{equation*}
u = f_x \frac{x_c}{z_c} + o_x \;\;\;\;\;\: v = f_y \frac{y_c}{z_c} + o_y
\end{equation*}
```

And going from 2D to 3D (ray):

```math
\begin{equation*}
x = \frac{z}{f_x} (u - o_x) \;\;\;\;\;\;\; y = \frac{z}{f_y} (u - o_y)
\end{equation*}
```
```math
\begin{equation*}
z>0
\end{equation*}
```
In order to reconstruct the 3D scene we need more information, the way to do so is to use a second camera, using a Stereo System.

##Binocular Vision
This system is composed by two identical cameras, they share the same intrinsic parameters and they are separated by a horizontal baseline $b$.


<img src="images/SimpleStereoTheory/Binocular%20Vision.png" width="50%">  
**Figure 1:** Binocular Vision

Let us assume we have found a unique point in both images given by $(u_l, v_l)$ and $(u_r, v_r)$, since we have both this coordinates, we now have 4 corresponding equations:

```math
\begin{equation*}
    u_l = f_x \frac{x}{z} + o_x \;\;\;\;\;\;\;\;\;  v_l = f_y \frac{y}{z} + o_y    
\end{equation*}
```
```math
\begin{equation*}
    u_r = f_x \frac{x-b}{z} + o_x \;\;\;\;\;\;\;\;\;  v_r = f_y \frac{y}{z} + o_y    
\end{equation*}
```
We assume $(f_x, f_y, b, o_x, o_y)$ are known. Given this four equations, we can get the position $(x,y,z)$ in the scene.

Solving for $(x,y,z)$ we get:
```math
\begin{equation*}
    x = \frac{b(u_l - o_x)}{(u_l - u_r)} \;\;\; y = \frac{b f_x (v_l - o_y)}{f_y(u_l - u_r)} \;\;\;  z = \frac{b f_x}{(u_l - u_r)}    
\end{equation*}
```
An important aspect of this three equations is that we have $(u_l - u_r)$, this relation is called *Disparity* which is inversely proportional to the $z$ depth and proportional to the *Baseline*, in other words, if a point is closer to the camera, the disparity is bigger and if a point is far away from the camera, the disparity is close to 0. On the other hand, a bigger Baseline will result on a bigger disparity.

##Stereo Matching
The goal of this process is to find the disparity between the left and the right images, both were taken using the same intrinsic parameters. This horizontal stereo system presents disparity on the horizontal axis only, therefore $v_l = v_r$.

<img src="images/SimpleStereoTheory/Stereo%20System%20Left.png" width="30%">  
**Figure 2:** Binocular Vision Left

<img src="images/SimpleStereoTheory/Stereo%20System%20Right.png" width="30%">  
**Figure 3:** Binocular Vision Right

Since we do not have vertical disparity, we can use Template Matching in order to find features in the images, we use a *Scan Line* $S$ and a *Template Window* $T$ to compute the disparity map, where brighter objects are closer in the scene.

<img src="images/SimpleStereoTheory/Disparity%20Map.png" width="30%">  
**Figure 4:** Disparity Map

Now we can compute the *Disparity* and *Depth* respectively:
```math
d = u_l - u_r \;\;\;\;\; z=\frac{bf_x}{(u_l-u_r)}
```
Finding a pixel $(k,l)$ can be done using different methods, here we have the computation using the *sum of squared distances*:
```math
SSD(k,l) = \sum_{(i,j) \in T} |E_l(i,j)-E_r(i+k,\:j+l)|^2
```
##Issues with Stereo Matching
One of the main limitations of this system is that the smaller the window size is, the higher the sensibility to noise, therefore, giving a much worst localisation, on the other hand, a bigger window will result on poor localisation but less noise issues. In order to address this problem, a solution might be to use an Adaptive Window Method, for each point, match using windows of multiple sizes and use the disparity that is a result of the best similarity measure (minimise SSD per pixel).

Another limitation is that surfaces in the image need to be textured, and this textures should not be repetitive.
