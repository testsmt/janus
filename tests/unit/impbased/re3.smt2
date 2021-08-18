(assert (str.in_re
	"abc"
	(str.to_re "abc")
))
(check-sat)
