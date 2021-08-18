(assert (=>
	(= 1 1)
	(= 2 2)
	(= 3 3)
	(= 4 4)
))
(assert (=>
	(= 1 1)
	(= 2 2)
))
(check-sat)
