(declare-const s1 String)
(declare-const s2 String)
(assert (<= (str.len s1) (str.len s2)))
(check-sat)
