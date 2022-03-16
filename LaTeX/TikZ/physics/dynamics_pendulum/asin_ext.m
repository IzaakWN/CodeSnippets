function [y,n] = asin_ext(x,varargin)
  % ASIN_EXT  Naturally extend arcsin.
  %   Author: Izaak Neutelings (March 2022)
  %   y = asin_ext(x) arcsin(x) in [-pi/2,pi/2].
  %   y = asin_ext(x,n) arcsin(x) in [(n-1)*pi/2,(n+1)*pi/2].
  %   y = asin_ext(x,t,T) arcsin(x) in [(n-1)*T/4,(n+1)*T/4].
  if nargin==1
    n = 0; % assume default arcsin in [-pi/2,pi/2]
  elseif nargin==2
    n = varargin{1}; % shift arcsin to [(n-1)*pi/2,(n+1)*pi/2]
  else
    t = varargin{1};
    T = varargin{2};
    n = floor(2*t/T+0.5); % (t+T/4) / (T/2)
  end
  % shift by pi*n; flip arcsin for odd n
  y = pi*n + asin((-1).^mod(n,2).*x);
end
