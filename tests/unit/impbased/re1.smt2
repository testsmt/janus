(assert (str.in_re
	"abc"
	(re.++ (str.to_re "a") (str.to_re "bc"))
))
(check-sat)
