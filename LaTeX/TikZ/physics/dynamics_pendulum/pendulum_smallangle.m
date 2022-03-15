% Author: Izaak Neutelings (Februari 2021)
% https://nl.mathworks.com/help/symbolic/simulate-physics-pendulum-swing.html
% https://nl.mathworks.com/matlabcentral/answers/604771-how-to-code-simple-pendulum-motion-using-ode45

theta_ic = [pi; 0]; % initial conditions: theta(t=0)=0.5; dtheta(t=0)=0.
tspan = [0 20];
[t, theta] = ode45(@odeFun, tspan, theta_ic);
plot(t, theta);
legend({'$\theta$', '$\dot{\theta}$'}, ...
    'Location', 'best', ...
    'Interpreter', 'latex', ...
    'FontSize', 16)

function dtheta = odeFun(t, theta)
    g = 1; %9.8;
    l = 1;
    % theta(1) = theta, theta(2) = dtheta
    dtheta = zeros(2, 1);
    dtheta(1) = theta(2);
    dtheta(2) = -g/l*theta(1);
end