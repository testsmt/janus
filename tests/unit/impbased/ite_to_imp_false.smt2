(declare-const b Bool)

(assert (ite
	b
	(= 1 2)
	(distinct 3 2)
))
(check-sat)
