(declare-const y Int)
(declare-const v Bool)
(assert (= v (not (= y (- 1)))))
(assert (ite v false (= y (- 1))))
(check-sat)
