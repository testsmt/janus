(declare-const P Bool)
(declare-const Q Bool)

(assert
	(or P Q)	
)
(assert
	(not (=> P Q))
)
(check-sat)
