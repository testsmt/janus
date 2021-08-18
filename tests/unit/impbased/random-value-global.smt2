(declare-const x String)
(assert (forall ((s String)) (= s s)))
(check-sat)
