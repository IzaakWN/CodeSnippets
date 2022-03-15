% Izaak Neutelings (March 2022)
clear all; close all; clc

disp("1) Extended arcsin")
figure(1)
x = linspace(-1,1,200);
tls = {}; % legend titles
hold on
plot(x,sin(x),'--','LineWidth',0.8);
for n = [ 0 1 2 3 ]
  y = asin_ext(x,n);
  plot(x,y,'LineWidth',1.6);
  tls{end+1} = sprintf('$n=%d$',n);
end
leg = legend(tls, ...
             'Location', 'north', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off

disp("2) ARCSIN(A*SIN)")
figure(2)
w = 1; %2*pi; % angular frequency
t = linspace(-1,1,50);
tls = {}; % legend titles
hold on
for A = [ -1 0.25 0.5 0.75 1 ] % amplitude
  y = asin_ext(A*sin(w*t),0);
  plot(t,y,'LineWidth',1.3);
  tls{end+1} = sprintf('$A=%.2g$',A);
end
leg = legend(tls, ...
             'Location', 'north', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off

disp("3) FLOOR")
figure(3)
t = linspace(-1,2,200);
tls = strings(1,2); % legend titles
colors = turbo(5); colors(1,:) = []; % color map
i = 1;
hold on
for T = [ 0.5 1 2 ] % period
  w = 2*pi/T; % angular frequency
  n = floor((t+T/4)/(T/2));
  y = sin(w*t);
  plot(t,y,'-.','LineWidth',0.7,'Color',colors(i,:));
  plot(t,n,'LineWidth',1.3,'Color',colors(i,:));
  tls(2*i-1) = sprintf('$T=%g$',T);
  i = i+1;
end
leg = legend(tls, ...
             'Location', 'northwest', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off

disp("4) ARCSIN(SIN,0)")
figure(4)
A = 1; % amplitude
t = linspace(-1,4,200);
tls = {}; % legend titles
hold on
for T = [ 1 2 4 ] % period
  w = 2*pi/T; % angular frequency
  y = asin_ext(A*sin(w*t),0);
  plot(t,y,'LineWidth',1.3);
  tls{end+1} = sprintf('$T=%.2g$',T);
end
leg = legend(tls, ...
             'Location', 'northwest', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off

disp("5) ARCSIN(SIN,t,T)")
figure(5)
A = 1; % amplitude
t = linspace(-1.5,3.5,200);
tls = strings(1,4); % legend titles
colors = turbo(5); colors(1,:) = []; % color map
i = 1;
hold on
for T = [ 1 2 4 ] % period
  w = 2*pi/T; % angular frequency
  [y,n] = asin_ext(A*sin(w*t),t,T);
  plot(t,n,'-.','LineWidth',0.7,'Color',colors(i,:));
  plot(t,y,'LineWidth',1.3,'Color',colors(i,:));
  tls(2*i) = sprintf('$T=%.2g$',T);
  i = i+1;
end
leg = legend(tls, ...
             'Location', 'northwest', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off

disp("Done")