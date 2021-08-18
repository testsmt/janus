(declare-const P Bool)
(declare-const Q Bool)

(assert
	(=> (not P) Q)	
)
(assert
	(not (or (not P) Q))
)
(check-sat)
