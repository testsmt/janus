(declare-const b Bool)

(assert (=>
	(not b)
	(distinct 3 2)
))
(check-sat)
