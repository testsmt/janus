(assert (ite
	(not (= 1 1))
	true
	(=>
		(= 2 2)
		(= 3 3)
		(= 4 4))
))
(assert (ite
	(not (= 1 1))
	true
	(= 2 2)
))
(check-sat)
