(assert (not (forall ((x Int) (y Int) (z Int))
	(=>
		(>= z 0)
		(>= x y)
		(>= (+ x z) y)
	)
)))
(check-sat)
