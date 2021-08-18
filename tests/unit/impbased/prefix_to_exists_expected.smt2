(assert (exists ((x0 String)) (exists ((x1 Int)) (=
	(str.substr x0 0 x1 )
	"AB"
))))
(check-sat)
