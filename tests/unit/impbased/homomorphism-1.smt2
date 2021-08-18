(declare-const s1 String)
(declare-const s2 String)
(assert (str.prefixof s1 s2))
(check-sat)
