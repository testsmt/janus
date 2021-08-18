(assert (str.in_re
	"abc"
	((_ re.^ 2) (re.union (str.to_re "a") (str.to_re "bc")))
))
(check-sat)
