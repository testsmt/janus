(declare-const b Bool)

(assert (=>
	b
	(= 1 2)
))
(check-sat)
