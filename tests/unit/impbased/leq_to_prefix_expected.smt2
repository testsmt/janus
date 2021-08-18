(assert (exists ((x0 String)) (exists ((x1 String)) (and
	(str.prefixof x1 "AB")
	(str.prefixof x1 x0)
))))
(check-sat)
