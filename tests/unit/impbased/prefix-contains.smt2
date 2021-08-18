(declare-const s String)
(assert (str.prefixof
	s
	"."
))
(check-sat)
