lato(1..n).
simbolo(1..5).

1{griglia(X,Y,S) : simbolo(S)}1 :- lato(X), lato(Y).
