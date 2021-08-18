(declare-const x Int)
(declare-const y Int)
(assert (=> (and (>= x 0) (>= (+ 57 (- 57)) 0)) (str.prefixof (str.substr "AZtxslXT" 0 x) (str.substr "AZtxslXT" 0 (+ 57 (- 57))))))
(check-sat)
