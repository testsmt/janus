(declare-fun a () Real)
(declare-fun b () Real)
(declare-fun c () Real)
(assert false)
(assert (exists ((d Real))
	(=>
		(and (and
			(=>
				(=> (<= 0 d) (> d c))
				(< (- b (* d d)) 0)
			)
			(= b 0))
			(= a 0))
		(= c 0)
	)
))
(check-sat)
