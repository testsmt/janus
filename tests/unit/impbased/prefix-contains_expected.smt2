(declare-const s String)
(assert (str.contains
	"."
	s
))
(check-sat)
