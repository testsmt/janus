(declare-const x Int)

(assert (or
	(= x 2)
	(= x 3)
	(= x 4)
	(= x 5)
))

(check-sat)
