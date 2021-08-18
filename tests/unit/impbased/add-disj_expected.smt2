(declare-const P Bool)
(declare-const Q Bool)
(assert
	(or (or P Q) Q)
)
(check-sat)
