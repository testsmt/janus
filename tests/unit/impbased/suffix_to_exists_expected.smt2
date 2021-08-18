(assert (exists ((x0 String)) (exists ((x1 Int)) (=
	(str.substr x0 x1 (- (str.len x0) x1))
	"AB"
))))
(check-sat)
