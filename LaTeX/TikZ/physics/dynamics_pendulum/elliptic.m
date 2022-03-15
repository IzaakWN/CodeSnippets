% Author: Izaak Neutelings (Februari 2022)
% http://dx.doi.org/10.1103/PhysRevA.90.013409
clear all; close all; clc

% ELLIPTIC FUNCTIONS vs. t
disp("1) Elliptic functions vs. t (0<m<1)")
figure(1)
hold on
t = linspace(0,10,200);
colors = turbo(5); colors(1,:) = []; % color map
i = 1;
for m = [ 0 0.5 1 ]
  %T = 4*ellipke(k^2)/w0; % period
  [sn,cn,dn] = ellipj(t,m); % Jacobi elliptic functions
  plot(t,sn,'Color',colors(i,:),'LineWidth',1.2);
  plot(t,cn,'--','Color',colors(i,:),'LineWidth',1.2);
  plot(t,dn,':','Color',colors(i,:),'LineWidth',1.2);
  i = i + 1;
end
xlabel('$t$','Interpreter','latex','FontSize',14)
ylabel('$f(t)$','Interpreter','latex','FontSize',14)
grid on
hold off

% ELLIPTIC FUNCTIONS vs. Kt
disp("2) Elliptic functions vs. Kt (0<m<1)")
figure(2)
hold on 
t = linspace(0,6.1,200);
colors = turbo(5); colors(1,:) = []; % color map
i = 1;
for m = [ 0.0 0.5 0.9999 ]
  K = ellipke(m); % quarter period
  [sn,cn,dn] = ellipj(K*t,m); % Jacobi elliptic functions
  plot(t,sn,'Color',colors(i,:),'LineWidth',1.2);
  plot(t,cn,'--','Color',colors(i,:),'LineWidth',1.2);
  plot(t,dn,':','Color',colors(i,:),'LineWidth',1.2);
  i = i+1;
end
xlim([0 6.2])
xlabel('$Kt$','Interpreter','latex','FontSize',14)
ylabel('$f(t)$','Interpreter','latex','FontSize',14)
grid on
hold off

% ELLIPTIC FUNCTIONS (m>1)
% https://en.wikipedia.org/wiki/Jacobi_elliptic_functions#The_Jacobi_real_transformations
disp("3) Elliptic functions vs. t (m>1)")
figure(3)
hold on
t = linspace(0,10,200);
colors = turbo(5); colors(1,:) = []; % color map
i = 1;
for m = [ 1.1 2.0 4.0 ]
  k = sqrt(m);
  sn = ellipj(k*t,1/m)/k; % Jacobi elliptic functions
  plot(t,sn,'Color',colors(i,:),'LineWidth',1.2);
  %plot(t,cn,'--','Color',colors(i,:),'LineWidth',1.2);
  %plot(t,dn,':','Color',colors(i,:),'LineWidth',1.2);
  i = i+1;
end
xlabel('$t$','Interpreter','latex','FontSize',14)
ylabel('$f(t)$','Interpreter','latex','FontSize',14)
grid on
hold off

% ELLIPTIC FUNCTIONS vs. Kt (m>1)
disp("4) Elliptic functions vs. Kt (m>1)")
figure(4)
hold on
t = linspace(0,6.1,200);
colors = turbo(5); colors(1,:) = []; % color map
ts = strings(1,3); % legend titles
i = 1;
for m = [ 1.1 2.0 4.0 ]
  k = sqrt(m);
  K = ellipke(1/m)/k; % quarter period
  sn = ellipj(K*k*t,1/m)/k; % Jacobi elliptic functions
  plot(t,sn,'Color',colors(i,:),'LineWidth',1.2);
  %plot(t,cn,'--','Color',colors(i,:),'LineWidth',1.2);
  %plot(t,dn,':','Color',colors(i,:),'LineWidth',1.2);
  ts(i) = sprintf("$m=%.1f$",m);
  i = i+1;
end
leg = legend(ts, ...
             'Location', 'north', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
xlim([0 6.2])
xlabel('$Kt$','Interpreter','latex','FontSize',14)
ylabel('$f(t)$','Interpreter','latex','FontSize',14)
grid on
hold off

% QUARTER PERIOD vs. m
% https://en.wikipedia.org/wiki/Quarter_period
disp("5) Quarter period vs. m (0<m<1)")
figure(5)
m = linspace(0,0.99,100);
K = ellipke(m); % quarter period
plot(m,K,'LineWidth',1.2);
xlabel('$m$','Interpreter','latex','FontSize',14)
ylabel('$K(m)$','Interpreter','latex','FontSize',14)
grid on

% QUARTER PERIOD vs. m (m>1)
% https://en.wikipedia.org/wiki/Quarter_period
disp("6) Quarter period vs. m (m>1)")
figure(6)
m = linspace(1.01,50,100);
k = sqrt(m);
K = ellipke(1./m)./k; % quarter period
plot(m,K,'LineWidth',1.2);
xlabel('$m$','Interpreter','latex','FontSize',14)
ylabel('$K(1/m)/\sqrt(m)$','Interpreter','latex','FontSize',14)
grid on

disp("Done.")