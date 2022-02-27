lato(1..n).
simbolo(1..5).

1{griglia(X,Y,S) : simbolo(S)}1 :- lato(X), lato(Y).

:- #count{X,Y : simbolo(S), S == 1, lato(X), lato(Y), griglia(X,Y,S)} > hearts.
:- #count{X,Y : simbolo(S), S == 2, lato(X), lato(Y), griglia(X,Y,S)} > clubs.
:- #count{X,Y : simbolo(S), S == 3, lato(X), lato(Y), griglia(X,Y,S)} > spades.
:- #count{X,Y : simbolo(S), S == 4, lato(X), lato(Y), griglia(X,Y,S)} > diamonds.


:- simbolo(S), lato(X), lato(Y1), lato(Y2), lato(Y3), lato(Y4),
   Y1 != Y2, Y1 != Y3, Y1 != Y4, Y2 != Y3, Y2 != Y4, Y3 != Y4,
   griglia(X,Y1,S), griglia(X,Y2,S), griglia(X,Y3,S), griglia(X,Y4,S).

:- simbolo(S), lato(Y), lato(X1), lato(X2), lato(X3), lato(X4),
   X1 != X2, X1 != X3, X1 != X4, X2 != X3, X2 != X4, X3 != X4,
   griglia(X1,Y,S), griglia(X2,Y,S), griglia(X3,Y,S), griglia(X4,Y,S).

score(P) :- P = RowPokers * 6 + ColPokers * 4 + RowTrips * 3 + ColTrips * 3 + RowPairs + ColPairs, 
            RowPokers = #count{X,Y : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 != S2, S1 != S3, S1 != S4, S2 != S3, S2 != S4, S3 != S4,
                                     S1 != 5, S2 != 5, S3 != 5, S4 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), lato(Y+3), Y <= n-3,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y+2,S3), griglia(X,Y+3,S4)},
            ColPokers = #count{Y,X : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 != S2, S1 != S3, S1 != S4, S2 != S3, S2 != S4, S3 != S4,
                                     S1 != 5, S2 != 5, S3 != 5, S4 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), lato(X+3), X <= n-3,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X+2,Y,S3), griglia(X+3,Y,S4)},
            RowTrips  = #count{X,Y : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 == S3,
                                     S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), Y <= n-2,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y+2,S3)},
            ColTrips  = #count{Y,X : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 == S3,
                                     S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), X <= n-2,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X+2,Y,S3)},
            RowPairs  = #count{X,Y : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 != S3,
                                     S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y-1),
                                     Y == n-1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y-1,S3);
                               X,Y : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 == S2, S1 != S3, S1 != S4,
                                     S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), lato(Y-1),
                                     Y > 1, Y < n-1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y+2,S3), griglia(X,Y-1,S4);
                               X,Y : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 != S3,
                                     S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2),
                                     Y == 1, Y < n-1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y+2,S3)},
           ColPairs  = #count{Y,X : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 != S3,
                                     S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X-1),
                                     X == n-1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X-1,Y,S3);
                               Y,X : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 == S2, S1 != S3, S1 != S4,
                                     S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), lato(X-1),
                                     Y > 1, Y < n-1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X+2,Y,S3), griglia(X-1,Y,S4);
                               Y,X : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 == S2, S1 != S3,
                                     S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2),
                                     X == 1, X < n-1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X+2,Y,S3)}.
                
#maximize {P:score(P)}.
#show griglia/3.
