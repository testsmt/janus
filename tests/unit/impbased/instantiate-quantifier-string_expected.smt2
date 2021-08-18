(assert (forall ((s1 String) (s2 String)) (=
	(str.++ s1 (str.++ s2 "AZtxslXT"))
	(str.++ (str.++ s1 s2) "AZtxslXT")
)))
(check-sat)
