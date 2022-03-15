function B = wrapAndReorder(A,lim)
  B = A;
  if length(A)==2 && A(end,1)>=lim
    B(end,1) = B(end,1) - lim; % subtract wrap limit
    B = B([2,1],:); % flip
    return
  end
  for i = 1:length(A)-1
    if A(i,1)>=lim
      B = A(i:end,:); % last rows
      B(:,1) = B(:,1) - lim; % subtract wrap limit
      B = wrapAndReorder(B,lim); % wrap recursively
      B(end+1:end+i-1,:) = A(1:i-1,:); % insert in front
      return
    end
  end
end

% A=[1,1;2,2;3,3;4,4;5,5;6,6;7,7;8,8;9,9;10,10]
% wrapAndReorder(A,3)
% => [1,7;2,8;3,9;4,10;1,4;2,5;3,6;1,1;2,2;3,3]