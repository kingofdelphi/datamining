function [U, S, V] = reduced_svd(A)
   eps = 0.05;
   M = A' * A;
   [NV, Vv] = eigs(M, rows(M));
   V = [];
   Nv = [];
   U = [];
   for i = 1 : rows(M)
       if (Vv(i, i) > eps)
           V = [V, NV(:, i)];
           U = [U, A * NV(:, i) ./ sqrt(Vv(i, i))];
           Nv = [Nv, sqrt(Vv(i, i))];
       end;
   end;
   S = eye(length(Nv));
   for i = 1 : length(Nv)
       S(i, i) = Nv(i);
   end;
end
