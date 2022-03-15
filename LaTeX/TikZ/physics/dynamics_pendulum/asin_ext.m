
% ASIN_EXT  Extend arcsin.
%   y = asin_ext(x) arcsin of x in [-pi/2,pi/2].
%   y = asin_ext(x,n) arcsin of x in [(n-1)*pi/2,(n+1)*pi/2].
%   y = asin_ext(x,t,T) arcsin of x in [(n-1)*T/4,(n+1)*T/4].

function [y,n] = asin_ext(x,varargin)
  if nargin==1
    n = 0;
  elseif nargin==2
    n = varargin{1};
  else % nargin>=2
    t = varargin{1};
    T = varargin{2};
    n = floor((t+T/4)/(T/2));
  end
  y = pi*n+asin((-1).^mod(n,2).*x);
end
