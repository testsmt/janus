(assert (forall ((b Bool)) (or
	b
	(not b)
)))
(assert (not (exists ((b Bool)) (and
	b
	(not b)
))))
(check-sat)
