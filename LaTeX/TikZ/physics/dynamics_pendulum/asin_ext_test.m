% Izaak Neutelings (March 2022)
% Description: Test the asin_ext function.
clear all; close all; clc

disp("1) Extended arcsin")
figure(1)
x = linspace(-1,1,200);
tls = "sin"; % legend titles
hold on
plot(x,sin(x),'--','LineWidth',0.8);
for n = [ 0 1 2 3 ]
  y = asin_ext(x,n);
  plot(x,y,'LineWidth',1.6);
  tls{end+1} = sprintf('asin, $n=%d$',n);
end
leg = legend(tls,'Location','north', ...
             'Interpreter','latex','FontSize',13);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/asin_ext")

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

% Help function
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