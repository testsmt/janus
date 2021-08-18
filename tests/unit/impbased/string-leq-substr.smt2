(declare-const s1 String)
(declare-const s2 String)
(declare-const s3 String)
(assert (= 1 1))
(assert (str.<=
	s1 s2
))
(assert (str.<=
	s2 s3
))
(check-sat)
