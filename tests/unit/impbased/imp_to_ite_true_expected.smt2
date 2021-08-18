(assert (ite
	(= 1 1)
	(=>
		(= 2 2)
		(= 3 3)
		(= 4 4))
	true
))
(assert (ite
	(= 1 1)
	(= 2 2)
	true
))
(check-sat)
