(assert (str.in_re
	(str.++ "abab" "ab")
	(re.++ (re.+ (str.to_re "ab")) (str.to_re "ab"))
))
(check-sat)
