(assert (forall ((s1 String) (s2 String) (s3 String)) (=
	(str.++ s1 (str.++ s2 s3))
	(str.++ (str.++ s1 s2) s3)
)))
(check-sat)
