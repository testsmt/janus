(declare-const s String)
(assert (=> (= s s) (>= (+ 1 1) (+ 1 1))))
(check-sat)
