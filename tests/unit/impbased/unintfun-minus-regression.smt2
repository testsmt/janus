(declare-fun x () Int)
(declare-fun y () Int)
(assert (>= (- x y) (- 2)))
(assert false)
(check-sat)
