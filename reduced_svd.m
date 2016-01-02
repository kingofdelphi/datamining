function [U, S, V] = svd(A)
   M = A' * A;
   [NV, Vv] = eigs(M, length(M));
   V = [];
   Nv = [];
   U = [];
   for i = 1 : length(M)
       if (Vv(i, i) > 0)
           V = [V, NV(:, i)];
           U = [U, A * V(:, i) ./ sqrt(Vv(i, i))];
           Nv = [Nv, sqrt(Vv(i, i))];
       end;
   end;
   S = eye(length(Nv))
   for i = 1 : length(Nv)
       S(i, i) = Nv(i);
   end;
end
