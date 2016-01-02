function [U, S, V] = full_svd(A)
   M = A' * A;
   [NV, Vv] = eigs(M, length(M));
   V = [];
   Nv = [];
   U = [];
   m = length(A(:, 1));
   n = length(A(1, :));
   c = m;
   for i = 1 : length(M)
       if (Vv(i, i) > 0)
           V = [V, NV(:, i)];
           if (c > 0)
               U = [U, A * V(:, i) ./ sqrt(Vv(i, i))];
               c--;
           end
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

