# Exact Solution of a Pendulum in `MATLAB`

The `MATLAB` script [`pendulum.m`](pendulum.m)
produces plots and data files for the exact solutions of a simple pendulum.
It makes use of the Jacobi elliptic functions, following the derivation in
[this paper](https://www.scielo.br/j/rbef/a/ns9Lc7tfqhZh678dBPXxRsQ/?lang=en).

The solutions are divided into two main cases:
* Closed trajectories.
* Open trajectories.

<img src="fig/pendulum_phase_portrait.png" alt="Pendulum exact solution phase portrait" max-width="800"/>

## Open trajectories
The pendulum swings back and forth along an arc.
We assume initial conditions &theta;(0) = &theta;<sub>0</sub> < &pi; & &theta;'(0) = 0 < &pi;.

<img src="fig/pendulum_theta_vs_t.png" alt="Pendulum exact solution" max-width="400"/>
<img src="fig/pendulum_theta_vs_Tt.png" alt="Pendulum exact solution" max-width="400"/>
<img src="fig/pendulum_omega_vs_t.png" alt="Pendulum exact solution; angular velocity" max-width="400"/>
<img src="fig/pendulum_omega_vs_Tt.png" alt="Pendulum exact solution; angular velocity" max-width="400"/>
<img src="fig/pendulum_omega_vs_theta.png" alt="Pendulum exact solution; period" max-width="300"/>

## Open trajectories
The pendulum goes around in circles without changing angular direction.
We assume initial conditions &theta;(0) = 0; & &theta;'(0) = &Omega;<sub>0</sub> > 2&omega;<sub>0</sub>,
where &omega;<sub>0</sub> is the angular frequency for a simple harmonic oscillator via the small-angle approximation.
For a simple pendulum with a mass suspended from a wire with length L, &omega;<sub>0</sub> = sqrt(g/L).

With these initial conditions, the solution &theta;(t) increases monotonically.
To get this result, one needs to naturally extend the `arcsin` function by shifting it every half-period.
This is done by the help function [`asin_ext.m`](asin_ext.m).

<img src="fig/pendulum_open_theta_vs_t.png" alt="Pendulum exact solution (open)" max-width="400"/>
<img src="fig/pendulum_open_theta_vs_Tt.png" alt="Pendulum exact solution (open)" max-width="400"/>
<img src="fig/pendulum_open_omega_vs_t.png" alt="Pendulum exact solution (open); angular velocity" max-width="400"/>
<img src="fig/pendulum_open_omega_vs_Tt.png" alt="Pendulum exact solution (open); angular velocity" max-width="400"/>
<img src="fig/pendulum_open_omega_vs_W0.png" alt="Pendulum exact solution (open); period" max-width="300"/>

## TikZ figures
The data in the text files are used for the TikZ plot presented [here](https://tikz.net/dynamics_pendulum/).