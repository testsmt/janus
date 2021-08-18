(assert (str.in_re
	"abde"
	(re.++ (str.to_re "ab") (str.to_re "de"))
))
(check-sat)
