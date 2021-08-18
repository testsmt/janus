(assert (str.in_re
	"aaaa"
	(re.+ (str.to_re "a"))
))
(check-sat)
