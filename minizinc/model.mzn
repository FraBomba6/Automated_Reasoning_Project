include "globals.mzn";

int: n;
int: hearts;   % --> 1
int: clubs;    % --> 2
int: spades;   % --> 3
int: diamonds; % --> 4

array[1..n, 1..n] of var 0..5: m;
var int: p;

% Given the number of cards for each suit the program must not exceed that number
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 1..1, [0 | k in 1..1], [hearts | k in 1..1]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 2..2, [0 | k in 2..2], [clubs | k in 2..2]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 3..3, [0 | k in 3..3], [spades | k in 3..3]);
constraint global_cardinality_low_up([m[i,j] | i,j in 1..n], 4..4, [0 | k in 4..4], [diamonds | k in 4..4]);

% Maximum 3 equals values on a row
constraint forall(i in 1..n)(
  global_cardinality_low_up([m[i,j] | j in 1..n], 1..4, [0 | k in 1..4], [3 | k in 1..4])
);

% Maximum 3 equals values on a column
constraint forall(j in 1..n)(
  global_cardinality_low_up([m[i,j] | i in 1..n], 1..4, [0 | k in 1..4], [3 | k in 1..4])
);

constraint p = 
  sum(i in 1..n)(
    sum(j in 1..n-3)(
      if
        m[i,j] != 5 /\
        m[i,j+1] != 5 /\
        m[i,j+2] != 5 /\
        m[i,j+3] != 5 /\
        m[i,j] != 0 /\
        m[i,j+1] != 0 /\
        m[i,j+2] != 0 /\
        m[i,j+3] != 0 /\
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
  sum(j in 1..n)(
    sum(i in 1..n-3)(
      if
        m[i,j] != 5 /\
        m[i+1,j] != 5 /\
        m[i+2,j] != 5 /\
        m[i+3,j] != 5 /\
        m[i,j] != 0 /\
        m[i+1,j] != 0 /\
        m[i+2,j] != 0 /\
        m[i+3,j] != 0 /\
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
  sum(i in 1..n)(
    sum(j in 1..n-2)(
      if m[i,j] != 5 /\ m[i,j] != 0 /\ m[i,j] == m[i,j+1] /\ m[i,j] == m[i,j+2]
      then 3
      else 0
      endif
    )
  ) + 
  sum(j in 1..n)(
    sum(i in 1..n-2)(
      if m[i,j] != 5 /\ m[i,j] != 0 /\ m[i,j] == m[i+1,j] /\ m[i,j] == m[i+2,j]
      then 3
      else 0
      endif
    )
  ) +
  sum(i in 1..n)(
    sum(j in 1..n-1)(
      if
        m[i,j] != 5 /\
        m[i,j] != 0 /\
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
  sum(j in 1..n)(
    sum(i in 1..n-1)(
      if
        m[i,j] != 5 /\
        m[i,j] != 0 /\
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
