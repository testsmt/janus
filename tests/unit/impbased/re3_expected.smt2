(assert (str.in_re
	"abc"
	(re.+ (str.to_re "abc"))
))
(check-sat)
