(assert (str.in_re
	(str.++ "abde" "de")
	(re.++ (str.to_re "ab") (str.to_re (str.++ "de" "de")))
))
(check-sat)
