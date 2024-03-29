lato(1..n).
simbolo(1..5).

% Assign at most one symbol to each cell
{griglia(X,Y,S) : simbolo(S), S != 5} 1:- lato(X), lato(Y), not griglia(X, Y, 5).

% Constraint 1: For each suits, the count of cards of that suit must be less than what given in the input
:- hearts < #count{X,Y : lato(X), lato(Y), griglia(X,Y,1)}.
:- clubs < #count{X,Y : lato(X), lato(Y), griglia(X,Y,2)}.
:- spades < #count{X,Y : lato(X), lato(Y), griglia(X,Y,3)}.
:- diamonds < #count{X,Y : lato(X), lato(Y), griglia(X,Y,4)}.

% Constraint 2: No more than three equal suits adjacent to each other on the same row
:- simbolo(S), lato(X), lato(Y1), lato(Y2), lato(Y3), lato(Y4),
   Y1+1 == Y2, Y1+2 == Y3, Y1+3 == Y4,
   S != 5,
   griglia(X,Y1,S), griglia(X,Y2,S), griglia(X,Y3,S), griglia(X,Y4,S).

% Constraint 3: No more than three equal suits adjacent to each other on the same column
:- simbolo(S), lato(Y), lato(X1), lato(X2), lato(X3), lato(X4),
   X1+1 == X2, X1+2 == X3, X1+3 == X4,
   S != 5,
   griglia(X1,Y,S), griglia(X2,Y,S), griglia(X3,Y,S), griglia(X4,Y,S).

score(P) :- P = RowPokers * 6 + ColPokers * 4 + RowTrips * 3 + ColTrips * 3 + RowPairs + ColPairs,
            RowPokers = #count{X,Y : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 != S2, S1 != S3, S1 != S4, S2 != S3, S2 != S4, S3 != S4,
                                     S1 != 5, S2 != 5, S3 != 5, S4 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), lato(Y+3), Y <= n-3,
                                     griglia(X,Y,S1), griglia(X,Y+1,S2), griglia(X,Y+2,S3), griglia(X,Y+3,S4)},
            ColPokers = #count{X,Y : simbolo(S1), simbolo(S2), simbolo(S3), simbolo(S4),
                                     S1 != S2, S1 != S3, S1 != S4, S2 != S3, S2 != S4, S3 != S4,
                                     S1 != 5, S2 != 5, S3 != 5, S4 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), lato(X+3), X <= n-3,
                                     griglia(X,Y,S1), griglia(X+1,Y,S2), griglia(X+2,Y,S3), griglia(X+3,Y,S4)},
            RowTrips  = #count{X,Y : simbolo(S), S != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), Y <= n-2,
                                     griglia(X,Y,S), griglia(X,Y+1,S), griglia(X,Y+2,S)},
            ColTrips  = #count{X,Y : simbolo(S), S != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), X <= n-2,
                                     griglia(X,Y,S), griglia(X+1,Y,S), griglia(X+2,Y,S)},
            RowPairs  = #count{X,Y : simbolo(S1), simbolo(S2), S1 != S2, S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y-1), Y == n-1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S1), griglia(X,Y-1,S2);
                               X,Y : simbolo(S1), simbolo(S2), simbolo(S3),
                                     S1 != S2, S1 != S3, S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), lato(Y-1), Y > 1, Y < n-1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S1), griglia(X,Y+2,S2), griglia(X,Y-1,S3);
                               X,Y : simbolo(S1), simbolo(S2), S1 != S2, S1 != 5,
                                     lato(X), lato(Y), lato(Y+1), lato(Y+2), Y == 1,
                                     griglia(X,Y,S1), griglia(X,Y+1,S1), griglia(X,Y+2,S2)},
            ColPairs  = #count{X,Y : simbolo(S1), simbolo(S2),
                                     S1 != S2, S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X-1), X == n-1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S1), griglia(X-1,Y,S2);
                               X,Y : simbolo(S1), simbolo(S2), simbolo(S3), S1 != S2, S1 != S3, S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), lato(X-1), X > 1, X < n-1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S1), griglia(X+2,Y,S2), griglia(X-1,Y,S3);
                               X,Y : simbolo(S1), simbolo(S2), S1 != S2,
                                     S1 != 5,
                                     lato(Y), lato(X), lato(X+1), lato(X+2), X == 1,
                                     griglia(X,Y,S1), griglia(X+1,Y,S1), griglia(X+2,Y,S2)}.

#maximize{P:score(P)}.
#show griglia/3.