(assert (forall ((x0 Bool)) (=>
	(and x0 (= 1 1))
	(and x0 (= 2 2))
	(and x0 (= 3 3))
	(and x0 (= 4 4))
)))
(assert (forall ((x0 Bool)) (=>
	(and x0 (= 1 1))
	(and x0 (= 2 2))
)))
(check-sat)
