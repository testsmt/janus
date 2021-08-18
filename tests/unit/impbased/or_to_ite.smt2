(declare-const x Int)

(assert (or
	(= x 2)
	(= x 3)
))
(check-sat)
