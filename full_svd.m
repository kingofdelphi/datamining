function [U, S, V] = full_svd(A)
   eps = 0.05;
   M = A' * A;
   [NV, Vv] = eigs(M, length(M));
   V = [];
   Nv = [];
   U = [];
   m = rows(A);
   n = columns(A);
   c = m;
   for i = 1 : rows(M)
       if (Vv(i, i) > eps)
           V = [V, NV(:, i)];
           if (c > 0)
               U = [U, A * NV(:, i) / sqrt(Vv(i, i))];
               c--;
           end;
           Nv = [Nv, sqrt(Vv(i, i))];
       end;
   end;
   S = zeros(m, n);
   for i = 1 : length(Nv)
       S(i, i) = Nv(i);
   end;
   V = [V, null(V')];
   U = [U, null(U')];
end

