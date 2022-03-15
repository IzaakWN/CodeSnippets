% Author: Izaak Neutelings (Februari 2021)
% Source: https://www.scielo.br/j/rbef/a/ns9Lc7tfqhZh678dBPXxRsQ/?lang=en
%         https://www.scielo.br/j/rbef/a/ns9Lc7tfqhZh678dBPXxRsQ/?format=pdf&lang=en
% Adapted from http://matlab.cheme.cmu.edu/2011/08/09/phase-portraits-of-a-system-of-odes/
clear all; close all; clc

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
    k = min(abs(v0)/(2*w0),0.9998); % sin(theta0/2)
    T = 4*ellipke(k^2)/w0; % period
    tf = 1.01*T; % last t
  else
    x0 = -sign(v0)*2*pi; % theta(0) initial condition
    k = max(abs(v0)/(2*w0),1.0001); % sin(theta0/2)
    T = 4*ellipke(1/k^2)/(k*w0); % period
    tf = 1.01*T;
  end
  [~,ys] = ode45(f,[0,tf],[x0;v0]);
  %ys(:,1) = 2*wrapToPi(0.5*ys(:,1));
  %ys = wrapAndReorder(2*pi+ys,4*pi)-2*pi;
  if v0>2.1
    ys = ys(1:find(ys>2*pi,1),:); % clip off
  elseif v0<-2.1
    ys = ys(1:find(ys<-2*pi,1),:); % clip off
  end
  fprintf("  %4.1f %7.1f %7.1f %7.1f\n",x0,v0,T,tf)
  plot(ys(:,1),ys(:,2),'LineWidth',1.3,'Color',colors(i,:));
  plot(ys(1,1),ys(1,2),'bo','MarkerSize',5,'MarkerFaceColor',colors(i,:)) % starting point
  plot(ys(end,1),ys(end,2),'ks','MarkerSize',5,'MarkerFaceColor',colors(i,:)) % ending point
  if v0>0 % store
    fname = sprintf("data/pendulum_phase-%.1f.txt",v0);
    fname = regexprep(fname,"(\d)\.(\d)","$1p$2");
    file  = fopen(fname,'w');
    fprintf(file,'%-12s %-12s\n','theta','omega'); % header
    fprintf(file,'%-12.8f %-12.8f\n',ys'); % data
    fclose(file);
    tls(3*i-2) = sprintf('$\\Omega_0/\\omega_0=%.10g$',v0);
  end
  i = i+1;
end
leg = legend(tls,'Position', [0.86 0.27 0.1 0.5], ...
             'Interpreter','latex','FontSize',10);
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
mysaveas("fig/pendulum_phase_portrait")

disp("2) theta vs. time")
figure(2)
hold on
t = linspace(0,50,300); % time
tls = ""; % legend titles
colors = turbo(7); % color map
disp("  x0    omega   freq f  period T")
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           %0.1 ...
           1.0 ...
           2.0 ...
           2.4 ... %2.5 ...
           2.8 ...
           3.0 ...
           3.1 ...
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2);
  T = 4*ellipke(k^2)/w0; % period
  f = 1./T; % frequency
  w = 2*pi*f; %pi/(2*ellipke(sin(x0/2)^2)); omega
  fprintf("  %4.2f %7.4f %7.4f %7.4f\n",x0,w,f,T)
  [sn,cn,dn] = ellipj(w0*(T/4-t),k^2); % Jacobi elliptic functions
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
ylim([-3.5 3.7])
yticks(-pi:pi/4:3.5)
yticklabels({'-\pi','-3\pi/4','-\pi/2','-\pi/4',...
             '0','\pi/4','\pi/2','3\pi/4','\pi'})
leg = legend(tls,'NumColumns',3, ... %'Location', 'northoutside', ...
             'Position',[0.5 0.86 0.4 0.1], ... 
             'Interpreter', 'latex','FontSize',11);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_theta_vs_t")

disp("3) theta vs. Tt")
figure(3)
hold on
t = linspace(0,2,300); % time
tls = ""; % legend titles
colors = turbo(8); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.0 1.5 2.0 ...
           2.4 2.8 ...
           3.0 3.1 ...
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2);
  T = 4*ellipke(k^2)/w0; % period
  f = 1./T; % frequency
  w = 2*pi*f;
  [sn,cn,dn] = ellipj(w0*(T/4-T*t),k^2); % Jacobi elliptic function
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
             'Position',[0.46 0.16 0.1 0.3], ... 
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_theta_vs_Tt")

disp("4) dtheta/dt vs. t")
figure(4)
hold on
t = linspace(0,50,300);
tls = ""; % legend titles
colors = turbo(7); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.2 ...
           2.0 ...
           2.4 ...
           2.8 ...
           3.0 ...
           3.1 ...
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2);
  T = 4*ellipke(k^2)/w0; % period
  w = 2*pi/T; %pi/(2*ellipke(sin(x0/2)^2)); omega
  [sn,cn,dn] = ellipj(w0*(T/4-t),k^2); % Jacobi elliptic functions
  v = -2*k*w0*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  vmax = x0*w; % s.h.o.
  %vmax = 2*k*w0; % exact pendulum
  plot([0.75*T 0.75*T],[-2.2 0.9*x0],'Color',colors(i,:),'LineWidth',0.7); % vertical line at t=T
  plot(t,-vmax*sin(w*t),'--','Color',colors(i,:),'LineWidth',0.7); % simple s.h.o. with the same period
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(3*i) = sprintf('$\\theta_0=%.4g$',x0);
  i = i+1;
end
leg = legend(tls,'NumColumns',3,'Position',[0.5 0.84 0.3 0.1], ... 
             'Interpreter','latex','FontSize',11);
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
t = linspace(0,2,300);
tls = ""; % legend titles
colors = turbo(7); % color map
i = 1;
for x0 = [ ... % amplitude theta(0) = x0
           1.2 ...
           2.0 ...
           2.4 2.8 ...
           3.0 3.1 ...
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = sin(x0/2);
  T = 4*ellipke(k^2)/w0; % period
  w = 2*pi/T; %pi/(2*ellipke(sin(x0/2)^2)); omega
  [sn,cn,dn] = ellipj(w0*T*(1/4-t),k^2); % Jacobi elliptic functions
  v = -2*k*w0*cn.*dn./sqrt(1-(k*sn).^2); % dtheta/dt
  vmax = x0*w; % s.h.o.
  plot(t,-vmax*sin(2*pi*t),'--','Color',colors(i,:),'LineWidth',0.7); % simple s.h.o. with the same period
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(2*i) = sprintf('$\\theta_0=%.4g$',x0);
  i = i+1;
end
leg = legend(tls,'NumColumns',1,'Position',[0.76 0.17 0.1 0.3], ...
             'Interpreter','latex','FontSize',12);
leg.ItemTokenSize = [13,100];
ylim([-2.2 2.2])
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_omega_vs_Tt")

disp("6) T/T0 vs. theta0")
t0 = linspace(0,0.995*pi,200);
T = 2*ellipke(sin(t0/2).^2)/pi; % T/T0
w = 1./T; % omega/omega0 = f/f0
fname = sprintf("data/pendulum_period.txt");
file  = fopen(fname,'w');
fprintf(file,'%-12s %-12s %-12s\n','theta0','T/T0','omega/omega0');
fprintf(file,'%-12.8f %-12.8f %-12.8f\n',[t0;T;w]);
fclose(file);
figure(6)
plot(t0,T,'LineWidth',1.2);
%plot(t0,2*ellipj(pi/2,sin(t0/2).^2)/pi)
xlabel("$\theta_0$ [rad]",'Interpreter','latex','FontSize',14)
ylabel('$T/T_0$','Interpreter','latex','FontSize',14)
xlim([0 3.4])
xticks(0:pi/4:3.4)
xticklabels({'0','\pi/4','\pi/2','3\pi/4','\pi'})
grid on
mysaveas("fig/pendulum_period_vs_theta",6)

disp("7) omega/omega0 vs. theta0")
figure(7)
plot(t0,w,'LineWidth',1.2);
xlabel("$\theta_0$ [rad]",'Interpreter','latex','FontSize',14)
ylabel("$\omega/\omega_0 = f/f_0$",'Interpreter','latex','FontSize',14)
xlim([0 3.4])
xticks(0:pi/4:3.4)
xticklabels({'0','\pi/4','\pi/2','3\pi/4','\pi'})
grid on
mysaveas("fig/pendulum_omega_vs_theta",6)

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

disp("9) theta vs. t (W0>2w0)")
figure(9)
hold on
t = linspace(0,12,300); % time
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
  k = W0/(2*w0);
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  f = 1./T; % frequency
  w = 2*pi*f; % angular velocity omega
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
leg = legend(tls, ...
             'Location', 'northwest', ...
             'Interpreter', 'latex', ...
             'FontSize', 11 );
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_open_theta_vs_t")

disp("10) theta vs. Tt (W0>2w0)")
figure(10)
hold on
t = linspace(0,2.5,300); % time
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
  k = W0/(2*w0);
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  w = 2*pi/T; % angular velocity omega
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
leg = legend(tls, ...
             'Location', 'southeast', ...
             'Interpreter', 'latex', ...
             'FontSize', 12 );
leg.ItemTokenSize = [13,100];
grid on
hold off
mysaveas("fig/pendulum_open_theta_vs_Tt")

disp("11) dtheta/dt vs. t (W0>2w0)")
figure(11)
hold on
t = linspace(0,12,300);
tls = ""; % legend titles
colors = turbo(9); % color map
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
           2.001 2.010 2.05 ...
           2.2 2.5 3.0 ...
           3.6 4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0);
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  [~,~,dn] = ellipj(W0*t/2,1/m); % Jacobi elliptic functions
  v = W0*dn; % dtheta/dt
  plot([T T],[0 W0+0.1],'Color',colors(i,:),'LineWidth',0.7); % vertical line at t=T
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(2*i) = sprintf('$\\Omega_0/2\\omega_0=%.6g$',k);
  i = i+1;
end
leg = legend(tls,'NumColumns',4,'Position',[0.3 0.83 0.5 0.1], ... 
             'Interpreter','latex','FontSize',11);
leg.ItemTokenSize = [10,100];
ylim([0 4.8])
xlabel("$t$ [s]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_omega_vs_t")

disp("12) dtheta/dt vs. Tt (W0>2w0)")
figure(12)
hold on
t = linspace(0,2.5,300);
tls = ""; % legend titles
colors = turbo(9); % color map
i = 1;
for W0 = [ ... % angular velocity dtheta/dt(0) = W0
           2.001 2.010 2.05 ...
           2.2 2.5 3.0 ...
           3.6 4.0
         ]
  w0 = 1; % angular frequency for s.h.o.
  k = W0/(2*w0);
  m = k^2;
  T = 4*ellipke(1/m)/W0; % period
  [~,~,dn] = ellipj(W0*T*t/2,1/m); % Jacobi elliptic functions
  v = W0*dn; % dtheta/dt
  plot(t,v,'Color',colors(i,:),'LineWidth',1.3); % exact pendulum solution
  tls(i) = sprintf('$\\Omega_0/2\\omega_0=%.6g$',k);
  i = i+1;
end
leg = legend(tls,'NumColumns',4,'Position',[0.3 0.83 0.5 0.1], ... 
             'Interpreter','latex','FontSize',11);
leg.ItemTokenSize = [10,100];
ylim([0 4.8])
xlabel("$t$ [$T$]",'Interpreter','latex','FontSize',14)
ylabel("$\dot{\theta}/\omega_0$",'Interpreter','latex','FontSize',14)
grid on
hold off
mysaveas("fig/pendulum_open_omega_vs_Tt")

disp("13) T/T0 vs. W0/2w0 (W0>2w0)")
w0 = 1; % angular frequency for s.h.o.
W0 = linspace(2.02,10,200);
k = W0/(2*w0);
m = k.^2;
T = 2*w0*ellipke(1./m)/pi./W0; % period
w = 1./T; % omega/omega0 = f/f0
fname = sprintf("data/pendulum_period_open.txt");
file  = fopen(fname,'w');
fprintf(file,'%-12s %-12s %-12s %-12s\n','W0/w0','W0/2w0','T/T0','omega/omega0');
fprintf(file,'%-12.8f %-12.8f %-12.8f %-12.8f\n',[W0/w0;k;T;w]);
fclose(file);
figure(13)
plot(k,T,'LineWidth',1.4);
xlabel("$\Omega_0/2\omega_0$",'Interpreter','latex','FontSize',14)
ylabel("$T/T_0$",'Interpreter','latex','FontSize',14)
grid on
mysaveas("fig/pendulum_open_period_vs_W0",6)

disp("14) omega/omega0 vs. W0/2w0 (W0>2w0)")
figure(14)
plot(k,w,'LineWidth',1.4);
xlabel("$\Omega_0/2\omega_0$",'Interpreter','latex','FontSize',14)
ylabel("$\omega/\omega_0 = f/f_0$",'Interpreter','latex','FontSize',14)
grid on 
mysaveas("fig/pendulum_open_omega_vs_W0",6)

disp("Done.")

function mysaveas(fname,w)
  if nargin==1
    w = 8;
  end
  %return % skip figures
  set(gcf,'PaperPosition',[0 0 w 5]); % position plot at left hand corner with width w and height 5. 
  set(gcf,'PaperSize',[w 5]); % set the paper to have width w and height 5.
  saveas(gcf,fname,'pdf') % save figure as PDF
  %%%saveas(gcf,fname,'png') % save figure as PNG
  print(gcf,fname,'-dpng','-r300') % save figure as PNG
end