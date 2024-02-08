function Z = fisherZcorr(X,Y)
C = cov(X,Y);
R = C(1,2) / (prod(sqrt(diag(C))));
Z = 0.5 * log((1+R)/(1-R));
