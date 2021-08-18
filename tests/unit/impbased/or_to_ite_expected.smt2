(declare-const x Int)

(assert (exists ((x0 Bool)) (ite
	x0
	(= x 2)
	(= x 3)
)))
(check-sat)
