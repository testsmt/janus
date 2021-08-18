(assert (str.in_re
	"PPP"
	(re.union (str.to_re "PPP") (re.+ (str.to_re "P")))
))
(check-sat)
