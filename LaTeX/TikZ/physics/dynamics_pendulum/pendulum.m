% Author: Izaak Neutelings (Februari 2021)
% Description:
%   Produce plots and data for the exact solution of a pendulum,
%   using Jacobi elliptic functions. Please see
%   https://github.com/IzaakWN/CodeSnippets/tree/master/LaTeX/TikZ/physics/dynamics_pendulum
%clear all; close all; clc
myblue = [0 0.4470 0.7410];
myred = [0.8500 0.3250 0.0980];

%%%%%%%%%%%%%%%%%%%%%%%%
%%   PHASE PORTRAIT   %%
%%%%%%%%%%%%%%%%%%%%%%%%
% Adapted from http://matlab.cheme.cmu.edu/2011/08/09/phase-portraits-of-a-system-of-odes/

disp("1) omega vs. theta - phase portrait")
w0 = 1; % angular frequency for s.h.o.
f = @(t,Y) [Y(2); -w0^2*sin(Y(1))]; % ODE
figure(1)
hold on
disp("  x0       v0      T       tf")
colors = turbo(18); % color map
tls = ""; %strings(1,8); % legend titles
i = 1;
for v0 = [ ...
          %0.5 1.0 1.5 ...
          0.4 0.8 1.2 1.6 ...
          2.0 ...
          2.1 -2.1 ...
          2.4 -2.4 2.8 -2.8 ...
          3.0 -3.0 3.2 -3.2 ...
         ]
  if abs(v0)<=2.0
    x0 = 0; % theta(0)=0 initial condition
    k = min(abs(v0)/(2*w0),0.99978); % sin(theta0/2)
    T = 4*ellipke(k^2)/w0; % period
    tf = 1.01*T; % final time t
  else
    x0 = -sign(v0)*2*pi; % theta(0) initial condition
    k = max(abs(v0)/(2*w0),1.0001); % sin(theta0/2)
    T = 4*ellipke(1/k^2)/(k*w0); % period
    tf = 1.01*T; % final time t
  end
  tspan = linspace(0,tf,300);
  [~,ys] = ode45(f,tspan,[x0;v0]);
  %ys(:,1) = 2*wrapToPi(0.5*ys(:,1));
  %ys = wrapAndReorder(2*pi+ys,4*pi)-2*pi;
  if v0>2.1
    ys = ys(1:find(ys>2*pi,1),:); % clip off
  elseif v0<-2.1
    ys = ys(1:find(ys<-2*pi,1),:); % clip off
  end
  fprintf("  %4.1f %7.1f %7.1f %7.1f\n",x0,v0,T,tf)
  plot(ys(:,1),ys(:,2),'LineWidth',1.3,'Color',colors(i,:));
  %plot(ys(1,1),ys(1,2),'bo','MarkerSize',5,'MarkerFaceColor',colors(i,:)) % starting point
  %plot(ys(end,1),ys(end,2),'ks','MarkerSize',5,'MarkerFaceColor',colors(i,:)) % ending point
  if v0>0 % store
    fname = sprintf("data/pendulum_phase-%.1f.txt",v0);
    fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
    file  = fopen(fname,'w');
    fprintf(file,'%-12s %-12s\n','theta','omega'); % header
    fprintf(file,'%-12.8f %-12.8f\n',ys'); % data
    fclose(file);
    tls(i) = sprintf('$\\Omega_0/\\omega_0=%.10g$',v0);
  end
  i = i+1;
end
leg = legend(tls,'Position', [0.88 0.35 0.03 0.40], ...
             'Interpreter','latex','FontSize',11);
leg.ItemTokenSize = [11,100];
xlabel("$\theta$ [rad]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
xlim([-2*pi 2*pi]);
ylim([-1.1*pi 1.1*pi]);
xticks(-2*pi:pi/2:2*pi)
xticklabels({'-2\pi','-3\pi/2','-\pi','-\pi/2',...
             '0','\pi/2','\pi','3\pi/2','2\pi'})
%axis tight equal
grid on
hold off
mysaveas("fig/pendulum_phase_portrait",8,0.07)


%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  CLOSE TRAJECTORIES   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initial conditions
% * theta(0) = x0, with 0 < x0 < pi,
% * dtheta/dt(0) = 0.
% Sources:
%   https://www.scielo.br/j/rbef/a/ns9Lc7tfqhZh678dBPXxRsQ/?lang=en
%   https://www.scielo.br/j/rbef/a/ns9Lc7tfqhZh678dBPXxRsQ/?format=pdf&lang=en

disp("2) theta vs. time")
figure(2)
hold on
t = linspace(0,50,401); % time
tls = ""; % legend titles
colors = turbo(7); % color map
disp("  x0    omega   freq f  period T")
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           %0.1 ...
           1.0 2.0 ...
           2.4 2.8 ... %2.5 ...
           3.0 3.1
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2); % elliptic modulus
  m = k^2;
  T = 4*ellipke(m)/w0; % period
  f = 1./T; % frequency
  w = 2*pi*f; % average angular frequency, omega
  fprintf("  %4.2f %7.4f %7.4f %7.4f\n",x0,w,f,T)
  [sn,cn,dn] = ellipj(w0*(T/4-t),m); % Jacobi elliptic functions
  x = 2*asin(k*sn); % theta (exact pendulum solution)
  v = -2*k*w0.*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  plot([T T],[-3.5 1.1*x0],'Color',colors(i,:),'LineWidth',0.5); % vertical line at t=T
  plot(t,x0*cos(w*t),'--','Color',colors(i,:),'LineWidth',0.5); % simple s.h.o. with the same period
  plot(t,x,'Color',colors(i,:),'LineWidth',1.4); % exact pendulum solution
  tls(3*i) = sprintf('$\\theta_0=%.4g$',x0);
  fname = sprintf("data/pendulum-%.1f.txt",x0);
  fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
  file  = fopen(fname,'w');
  fprintf(file,'%-12s %-12s %-12s\n','time','theta','dtheta/dt'); % header
  fprintf(file,'%-12.8f %-12.8f %-12.8f\n',[t;x;v]); % data
  fclose(file);
  i = i+1;
end
xlabel("$t$ [s]",'Interpreter','latex','FontSize',14)
ylabel("$\theta$ [rad]",'Interpreter','latex','FontSize',14)
ylim([-3.5 3.95])
yticks(-pi:pi/4:4)
yticklabels({'-\pi','-3\pi/4','-\pi/2','-\pi/4',...
             '0','\pi/4','\pi/2','3\pi/4','\pi','5\pi/4'})
leg = legend(tls,'NumColumns',3, ... %'Location', 'northoutside', ...
             'Position',[0.54 0.9 0.3 0.07], ... 
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_theta_vs_t")

disp("3) theta vs. Tt")
figure(3)
hold on
t = linspace(0,2,401); % time
tls = ""; % legend titles
colors = turbo(9); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.0 1.5 2.0 ...
           2.4 2.8 ...
           3.0 3.1 3.14
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2); % elliptic modulus
  m = k^2;
  T = 4*ellipke(m)/w0; % period
  f = 1./T; % frequency
  w = 2*pi*f; % average angular frequency, omega
  [sn,cn,dn] = ellipj(w0*(T/4-T*t),m); % Jacobi elliptic function
  x = 2*asin(k*sn); % theta (exact pendulum solution)
  v = -2*k*w0.*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  plot(t,x0*cos(w*T*t),'--','Color',colors(i,:),'LineWidth',0.5); % simple s.h.o. with the same period
  plot(t,x,'Color',colors(i,:),'LineWidth',1.4); % exact pendulum solution
  tls(2*i) = sprintf('$\\theta_0=%.4g$',x0);
  fname = sprintf("data/pendulum-%.1f_norm.txt",x0);
  fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
  file  = fopen(fname,'w');
  fprintf(file,'%-12s %-12s %-12s\n','Tt','theta','dtheta/dt'); % header
  fprintf(file,'%-12.8f %-12.8f %-12.8f\n',[t;x;v]); % data
  fclose(file);
  i = i+1;
end
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\theta$ [rad]",'Interpreter','latex','FontSize',14)
ylim([-3.5 3.8])
yticks(-pi:pi/4:3.5)
yticklabels({'-\pi','-3\pi/4','-\pi/2','-\pi/4',...
             '0','\pi/4','\pi/2','3\pi/4','\pi'})
leg = legend(tls,'NumColumns',1, ...  %'Location', 'northoutside', ...
             'Position',[0.49 0.18 0.1 0.3], ... 
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_theta_vs_Tt")

disp("4) dtheta/dt vs. t")
figure(4)
hold on
t = linspace(0,50,501);
tls = ""; % legend titles
colors = turbo(7); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.2 2.0 ...
           2.4 2.8 ...
           3.0 3.1
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2); % elliptic modulus
  m = k^2;
  T = 4*ellipke(m)/w0; % period
  w = 2*pi/T; %pi/(2*ellipke(sin(x0/2)^2)); omega
  [sn,cn,dn] = ellipj(w0*(T/4-t),m); % Jacobi elliptic functions
  v = -2*k*w0*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  vmax = x0*w; % maximum omega, s.h.o.
  %vmax = 2*k*w0; % maximum omega, exact pendulum
  plot([0.75*T 0.75*T],[-2.2 0.9*x0],'Color',colors(i,:),'LineWidth',0.7); % vertical line at t=T
  plot(t,-vmax*sin(w*t),'--','Color',colors(i,:),'LineWidth',0.7); % simple s.h.o. with the same period
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(3*i) = sprintf('$\\theta_0=%.4g$',x0);
  i = i+1;
end
leg = legend(tls,'NumColumns',3,'Position',[0.53 0.90 0.2 0.08], ... 
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [13,100];
ylim([-2.2 2.7])
xlabel("$t$ [s]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_omega_vs_t")

disp("5) dtheta/dt vs. Tt")
figure(5)
hold on
t = linspace(0,2,501);
tls = ""; % legend titles
colors = turbo(8); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.2 2.0 ...
           2.4 2.8 ...
           3.0 3.1 3.14
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2); % elliptic modulus
  m = k^2;
  T = 4*ellipke(m)/w0; % period
  w = 2*pi/T; %pi/(2*ellipke(sin(x0/2)^2)); omega
  [sn,cn,dn] = ellipj(w0*T*(1/4-t),m); % Jacobi elliptic functions
  v = -2*k*w0*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  vmax = x0*w; % maximum omega, s.h.o.
  plot(t,-vmax*sin(2*pi*t),'--','Color',colors(i,:),'LineWidth',0.7); % simple s.h.o. with the same period
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(2*i) = sprintf('$\\theta_0=%.4g$',x0);
  i = i+1;
end
leg = legend(tls,'NumColumns',1,'Position',[0.82 0.17 0.08 0.3], ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [13,100];
ylim([-2.2 2.2])
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_omega_vs_Tt")

disp("6) T/T0 vs. theta0")
t0 = linspace(0,3.14,315); % theta0
k = sin(t0/2);
T = 2*ellipke(k.^2)/pi; % T/T0
w = 1./T; % omega/omega0 = f/f0
Wmax = 2*k; % maximum angular velocity
fname = sprintf("data/pendulum_period.txt");
file  = fopen(fname,'w');
fprintf(file,'%-12s %-12s %-12s %-12s\n','theta0','T/T0','omega/omega0','Wmax/omega0');
fprintf(file,'%-12.8f %-12.8f %-12.8f %-12.8f\n',[t0;T;w;Wmax]);
fclose(file);
figure(6)
hold on
plot([0 3.2],[1 1],'--','LineWidth',0.7,'Color',myred);
plot(t0,T,'LineWidth',1.5,'Color',myblue);
leg = legend(["Small-angle approximation ($T=T_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','northwest', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlabel("$\theta_0$ [rad]",'Interpreter','latex','FontSize',14)
ylabel('$T/T_0$','Interpreter','latex','FontSize',14)
xlim([0 3.2])
ylim([0 5.5])
xticks(0:pi/4:3.4)
xticklabels({'0','\pi/4','\pi/2','3\pi/4','\pi'})
grid on
hold off
mysaveas("fig/pendulum_period_vs_theta",6)

disp("7) omega/omega0 vs. theta0")
figure(7)
hold on
plot([0 3.2],[1 1],'--','LineWidth',0.7,'Color',myred);
plot(t0,w,'LineWidth',1.5,'Color',myblue);
leg = legend(["Small-angle approximation ($\omega=\omega_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','southwest', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlabel("$\theta_0$ [rad]",'Interpreter','latex','FontSize',14)
ylabel("$\omega/\omega_0 = f/f_0$",'Interpreter','latex','FontSize',14)
xlim([0 3.2])
ylim([0.1 1.1])
xticks(0:pi/4:3.4)
xticklabels({'0','\pi/4','\pi/2','3\pi/4','\pi'})
grid on
hold off
mysaveas("fig/pendulum_omega_vs_theta",6)

disp("8) omega_max vs. theta0")
figure(8)
hold on
plot(t0,t0,'--','LineWidth',0.7,'Color',myred);
plot(t0,Wmax,'LineWidth',1.5,'Color',myblue);
leg = legend(["Small-angle approximation ($\Omega_\mathrm{max}=\theta_0\omega_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','southeast', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlabel("$\theta_0$ [rad]",'Interpreter','latex','FontSize',14)
ylabel("$\Omega_\mathrm{max}/\omega_0$",'Interpreter','latex','FontSize',14)
xlim([0 3.2])
ylim([0 2.1])
xticks(0:pi/4:3.4)
xticklabels({'0','\pi/4','\pi/2','3\pi/4','\pi'})
hold off
grid on
mysaveas("fig/pendulum_Wmax_vs_theta",6)

%disp("8) sin/pendulum vs. t")
%figure(8)
%xlabel('$t$','Interpreter','latex','FontSize',14)
%ylabel('(cos-pendulum)/abs(pendulum)','FontSize',14)
%hold on
%x0 = 3.0;
%om = pi/(2*ellipke(sin(x0/2)^2));
%t = linspace(0,6.0,100);
%x = 2*asin(sin(x0/2)*ellipj(ellipke(sin(x0/2)^2)-t,sin(x0/2)^2));
%x = (x0*cos(om*t) - x)./abs(x);
%plot(t,x);


%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%   OPEN TRAJECTORIES   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initial conditions
% * theta(0) = 0,
% * dtheta/dt(0) = W0 > 2w0,
% where w0=1 is the angular frequency for a simple harmonic oscillator.
% We use the Jacobi real transformation for m > 1:
% * K(m) = K(1/m)/k,
% * sn(u,m) = sn(k*u,1/m)/k.
% following [1] and [2].
% Note that if one uses the jacobiAM function [3], 
% one does not need to do these transformations.
% 
% [1] https://en.wikipedia.org/wiki/Jacobi_elliptic_functions#The_Jacobi_real_transformations
% [2] https://dlmf.nist.gov/19.7
% [3] https://ch.mathworks.com/help/symbolic/jacobiam.html

disp("9) theta vs. t (W0>2w0)")
figure(9)
hold on
t = linspace(0,12,401); % time
tls = ""; % legend titles
colors = turbo(8); % color map
disp("  W0/w0  W0/2w0  omega   freq f  period T")
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
          2.001 ...
          2.010 ...
          2.05 ...
          2.2 ...
          2.5 ...
          3.0 ...
          4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0); % elliptic modulus > 1
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  f = 1./T; % frequency
  w = 2*pi*f; % average angular frequency, omega
  fprintf("  %4.2f %6.2f %9.4f %7.4f %7.4f\n",W0/w0,k,w,f,T)
  [sn,~,dn] = ellipj(W0*t/2,1/m); % Jacobi elliptic functions
  x = 2*asin_ext(sn,t,2*T); % theta (exact pendulum solution)
  v = W0*dn; % dtheta/dt
  plot([T T],[0 7.0],'Color',colors(i,:),'LineWidth',0.5); % vertical line at t=T
  %plot(t,W0*t,'--','Color',colors(i,:),'LineWidth',0.5); % constant angular velocity
  plot(t,w*t,'--','Color',colors(i,:),'LineWidth',0.5); % constant angular velocity
  plot(t,x,'Color',colors(i,:),'LineWidth',1.4); % exact pendulum solution
  tls(3*i) = sprintf('$\\Omega_0/2\\omega_0=%.5g$',k);
  if W0<2.2
    fname = "data/pendulum_open-%.5g.txt";
  else
    fname = "data/pendulum_open-%.1f.txt";
  end
  fname = sprintf(fname,W0);
  fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
  file  = fopen(fname,'w');
  fprintf(file,'%-12s %-12s %-12s\n','time','theta','dtheta/dt'); % header
  fprintf(file,'%-12.8f %-12.8f %-12.8f\n',[t;x;v]); % data
  fclose(file);
  i = i+1;
end
xlabel("$t$ [s]",'Interpreter','latex','FontSize',14)
ylabel("$\theta$ [rad]",'Interpreter','latex','FontSize',14)
ylim([0 22])
yticks(0:pi:7*pi)
yticklabels({'0','\pi','2\pi','3\pi','4\pi','5\pi','6\pi','7\pi'})
leg = legend(tls,'Location','northwest', ...
             'Interpreter','latex','FontSize',13);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_open_theta_vs_t")

disp("10) theta vs. Tt (W0>2w0)")
figure(10)
hold on
t = linspace(0,2.5,401); % time
tls = ""; % legend titles
colors = turbo(10); % color map
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
          2.00000002 ...
          2.00002 ...
          2.001 ...
          2.01 2.05 2.2 ...
          2.5 3.0 4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0); % elliptic modulus > 1
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  %w = 2*pi/T; % angular velocity omega
  [sn,~,dn] = ellipj(W0*T*t/2,1/m); % Jacobi elliptic functions
  x = 2*asin_ext(sn,T*t,2*T); % theta (exact pendulum solution)
  v = W0*dn; % dtheta/dt
  plot(t,x,'Color',colors(i,:),'LineWidth',1.4); % exact pendulum solution
  tls(i) = sprintf('$\\Omega_0/2\\omega_0=%.10g$',k);
  if W0<2.2
    fname = "data/pendulum_open-%.10g_norm.txt";
  else
    fname = "data/pendulum_open-%.1f_norm.txt";
  end
  fname = sprintf(fname,W0);
  fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
  file  = fopen(fname,'w');
  fprintf(file,'%-12s %-12s %-12s\n','time','theta','dtheta/dt'); % header
  fprintf(file,'%-12.8f %-12.8f %-12.8f\n',[t;x;v]); % data
  fclose(file);
  i = i+1;
end
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\theta$ [rad]",'Interpreter','latex','FontSize',14)
ylim([0 16])
yticks(0:pi:5*pi)
yticklabels({'0','\pi','2\pi','3\pi','4\pi','5\pi'})
leg = legend(tls,'Location','southeast', ...
             'Interpreter','latex','FontSize',13);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_open_theta_vs_Tt")

disp("11) dtheta/dt vs. t (W0>2w0)")
figure(11)
hold on
t = linspace(0,12,401);
tls = ""; % legend titles
colors = turbo(9); % color map
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
           2.001 2.010 2.05 ...
           2.2 2.5 3.0 ...
           3.6 4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0); % elliptic modulus > 1
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  [~,~,dn] = ellipj(W0*t/2,1/m); % Jacobi elliptic functions
  v = W0*dn; % dtheta/dt
  plot([T T],[0 W0+0.1],'Color',colors(i,:),'LineWidth',0.7); % vertical line at t=T
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(2*i) = sprintf('$\\Omega_0/2\\omega_0=%.6g$',k);
  i = i+1;
end
leg = legend(tls,'NumColumns',4,'Position',[0.3 0.9 0.5 0.08], ... 
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [10,100];
ylim([0 4.7])
xlabel("$t$ [s]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_omega_vs_t")

disp("12) dtheta/dt vs. Tt (W0>2w0)")
figure(12)
hold on
t = linspace(0,2.5,401);
tls = ""; % legend titles
colors = turbo(9); % color map
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
           2.001 2.010 2.05 ...
           2.2 2.5 3.0 ...
           3.6 4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0); % elliptic modulus > 1
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  [~,~,dn] = ellipj(W0*T*t/2,1/m); % Jacobi elliptic functions
  v = W0*dn; % dtheta/dt
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(i) = sprintf('$\\Omega_0/2\\omega_0=%.6g$',k);
  i = i+1;
end
leg = legend(tls,'NumColumns',4,'Position',[0.3 0.9 0.5 0.08], ... 
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [10,100];
ylim([0 4.7])
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_omega_vs_Tt")

disp("13) T/T0 vs. W0/2w0 (W0>2w0)")
w0 = 1; % angular frequency for s.h.o.
W0 = linspace(2.02,10.02,321);
k = W0/(2*w0); % elliptic modulus > 1
m = k.^2;
T = 2*w0*ellipke(1./m)/pi./W0; % period
w = 1./T; % omega/omega0 = f/f0
Wmin = 2*sqrt(m-1);
fname = sprintf("data/pendulum_period_open.txt");
file  = fopen(fname,'w');
fprintf(file,'%-12s %-12s %-12s %-12s %-12s\n','W0/w0','W0/2w0','T/T0','omega/omega0','Wmin/omega0');
fprintf(file,'%-12.8f %-12.8f %-12.8f %-12.8f %-12.8f\n',[W0/w0;k;T;w;Wmin]);
fclose(file);
figure(13)
hold on
plot(k,1./(2*k),'--','LineWidth',0.7,'Color',myred);
plot(k,T,'LineWidth',1.4,'Color',myblue);
leg = legend(["Uniform circular motion ($T/T_0 = \omega_0/\Omega_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','northwest', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlim([1 5])
ylim([0 1.1])
xlabel("$\Omega_0/2\omega_0$",'Interpreter','latex','FontSize',14)
ylabel("$T/T_0$",'Interpreter','latex','FontSize',14)
hold off
grid on
mysaveas("fig/pendulum_open_period_vs_W0",6)

disp("14) omega/omega0 vs. W0/2w0 (W0>2w0)")
figure(14)
hold on
plot(k,2*k,'--','LineWidth',0.7,'Color',myred);
plot(k,w,'LineWidth',1.5,'Color',myblue);
leg = legend(["Uniform circular motion ($\omega = \Omega_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','northwest', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlim([1 5])
ylim([0 10])
xlabel("$\Omega_0/2\omega_0$",'Interpreter','latex','FontSize',14)
ylabel("$\omega/\omega_0 = f/f_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_omega_vs_W0",6)

disp("15) Omega_max/omega0 vs. W0/2w0 (W0>2w0)")
tts = ["Uniform circular motion ($\omega = \Omega_0$)" "Exact solution"];
figure(15)
hold on
plot(k,2*k,'--','LineWidth',0.7,'Color',myred);
plot(k,Wmin,'LineWidth',1.5,'Color',myblue);
leg = legend(["Uniform circular motion ($\Omega_\mathrm{min} = \Omega_0$)" "Exact solution"], ...
             'NumColumns',1,'Location','northwest', ...
             'Interpreter','latex','FontSize',14);
leg.ItemTokenSize = [15,100];
xlim([1 5])
ylim([0 10])
xlabel("$\Omega_0/2\omega_0 = \Omega_\mathrm{max}/2\omega_0$",'Interpreter','latex','FontSize',14)
ylabel("$\Omega_\mathrm{min}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_Wmin_vs_W0",6)

disp("Done.")


%%%%%%%%%%%%%%%%%%%%%%
%   HELP FUNCTIONS   %
%%%%%%%%%%%%%%%%%%%%%%

function mysaveas(fname,width,rmarg)
  if nargin==1
    width = 8; % height
  end
  if nargin<=2
    rmarg = 0.02; % extra right margin
  end
  set(gca,'Units','normalized'); % ensure normalized units
  set(gcf,'PaperPosition',[0 0 width 5]); % position plot at left hand corner with width w and height 5
  set(gcf,'PaperSize',[width 5]); % set the paper to have width w and height 5
  Tight = get(gca,'TightInset');  % gives you the bording spacing between plot box and any axis labels
  Tight = [0.02/width 0.005 rmarg 0.02]+Tight; % [Left Bottom Right Top] spacing
  set(gca,'Position',[Tight(1) Tight(2) 1-Tight(1)-Tight(3) 1-Tight(2)-Tight(4)]);
  %return % skip saving figures
  saveas(gcf,fname,'pdf') % save figure as PDF
  %%%saveas(gcf,fname,'png') % save figure as PNG (low res)
  print(gcf,fname,'-dpng','-r300') % save figure as PNG (high res)
end