(assert (str.in_re
	"abab"
	(re.+ (str.to_re "ab"))
))
(check-sat)
