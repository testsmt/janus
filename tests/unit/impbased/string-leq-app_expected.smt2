(declare-const s1 String)
(declare-const s2 String)
(declare-const s3 String)
(assert (str.<=
	s1 (str.++ s2 s1)
))
(assert (str.<=
	s2 (str.++ s3 s3)
))
(check-sat)
