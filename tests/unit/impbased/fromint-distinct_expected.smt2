(assert (=> (and (>= 0 0) (>= 1 0)) (distinct (str.from_int 0) (str.from_int 1))))
(check-sat)
