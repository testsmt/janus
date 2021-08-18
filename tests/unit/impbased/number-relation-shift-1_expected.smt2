(assert (not (forall ((x Int) (y Int) (z Int))
	(=>
		(>= z 0)
		(>= (+ x (- (abs 0))) y)
		(>= (+ x z) y)
	)
)))
(check-sat)
