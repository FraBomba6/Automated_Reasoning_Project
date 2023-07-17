include "globals.mzn";

int: n;
int: hearts;
int: clubs;
int: spades;
int: diamonds;
int: blocked;
array[1..n, 1..n] of var 1..5: m;

var int: p;

% Constraint 1: For each suits, the count of cards of that suit must be less than what given in the input
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 1..1, [0 | k in 1..1], [hearts | k in 1..1]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 2..2, [0 | k in 2..2], [clubs | k in 2..2]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 3..3, [0 | k in 3..3], [spades | k in 3..3]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 4..4, [0 | k in 4..4], [diamonds | k in 4..4]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 5..5, [0 | k in 5..5], [blocked | k in 5..5]);

% Constraint 2: No more than three equal suits adjacent to each other on the same row
constraint forall(i in 1..n, j in 1..n-3)(
  if m[i,j] == m[i,j+1] /\ m[i,j] == m[i,j+2] /\ m[i,j] != 5
  then m[i,j] != m[i,j+3]
  endif
 );

% Constraint 3: No more than three equal suits adjacent to each other on the same column
constraint forall(j in 1..n, i in 1..n-3)(
  if m[i,j] == m[i+1,j] /\ m[i,j] == m[i+2,j] /\ m[i,j] != 5
  then m[i,j] != m[i+3,j]
  endif
);

constraint p = 
  % Points for four different suits on same row
  sum(i in 1..n)(
    sum(j in 1..n-3)( 
      if
        m[i,j] != 5 /\
        m[i,j+1] != 5 /\
        m[i,j+2] != 5 /\
        m[i,j+3] != 5 /\
        m[i,j] != m[i,j+1] /\
        m[i,j] != m[i,j+2] /\
        m[i,j] != m[i,j+3] /\
        m[i,j+1] != m[i,j+2] /\
        m[i,j+1] != m[i,j+3] /\
        m[i,j+2] != m[i,j+3]  
      then 6
      else 0
      endif
    )
  ) +
  % Points for four different suits on same column
  sum(j in 1..n)(
    sum(i in 1..n-3)(
      if
        m[i,j] != 5 /\
        m[i+1,j] != 5 /\
        m[i+2,j] != 5 /\
        m[i+3,j] != 5 /\
        m[i,j] != m[i+1,j] /\
        m[i,j] != m[i+2,j] /\
        m[i,j] != m[i+3,j] /\
        m[i+1,j] != m[i+2,j] /\
        m[i+1,j] != m[i+3,j] /\
        m[i+2,j] != m[i+3,j]
      then 4
      else 0
      endif
    )
  ) +
  % Points for three equal suits on same row
  sum(i in 1..n)(
    sum(j in 1..n-2)(
      if m[i,j] != 5 /\ m[i,j] == m[i,j+1] /\ m[i,j] == m[i,j+2]
      then 3
      else 0
      endif
    )
  ) + 
  % Points for three equal suits on same column
  sum(j in 1..n)(
    sum(i in 1..n-2)(
      if m[i,j] != 5 /\ m[i,j] == m[i+1,j] /\ m[i,j] == m[i+2,j]
      then 3
      else 0
      endif
    )
  ) +
  % Points for two equal suits on same row
  sum(i in 1..n)(
    sum(j in 1..n-1)(
      if
        m[i,j] != 5 /\
        if j+1 == n
        then m[i,j] == m[i,j+1] /\ m[i,j] != m[i,j-1]
        else
          if j > 1
          then m[i,j] == m[i,j+1] /\ m[i,j] != m[i,j+2] /\ m[i,j] != m[i,j-1]
          else m[i,j] == m[i,j+1] /\ m[i,j] != m[i,j+2]
          endif
        endif
      then 1
      else 0
      endif
    )
  ) + 
  % Points for two equal suits on same column
  sum(j in 1..n)(
    sum(i in 1..n-1)(
      if
        m[i,j] != 5 /\
        if i+1 == n
        then m[i,j] == m[i+1,j] /\ m[i,j] != m[i-1,j]
        else
          if i>1
          then m[i,j] == m[i+1,j] /\ m[i,j] != m[i+2,j] /\ m[i,j] != m[i-1,j]
          else m[i,j] == m[i+1,j] /\ m[i,j] != m[i+2,j]
          endif
        endif
      then 1
      else 0
      endif
    )
  );
solve maximize p;

output["griglia(" ++ show(i) ++ "," ++ show(j) ++ "," ++ show(m[i,j]) ++ ") " | i,j in 1..n] ++
      ["\nOptimization: " ++ show(p)]
