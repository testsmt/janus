(declare-const i Int)
(declare-const j Int)
(assert (=> (and (>= i 0) (>= j 0)) (str.suffixof (str.substr "AZtxslXT" i (str.len "AZtxslXT")) (str.substr "AZtxslXT" j (str.len "AZtxslXT")))))
(check-sat)
