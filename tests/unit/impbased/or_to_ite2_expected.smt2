(declare-const x Int)

(assert (exists ((x0 Bool)) (ite
	x0
	(or (= x 2) (= x 3) (= x 4))
	(= x 5)
)))

(check-sat)
