(assert (forall ((x Int)) (let ((?y x))
	(= ?y ?y)
)))
(check-sat)
