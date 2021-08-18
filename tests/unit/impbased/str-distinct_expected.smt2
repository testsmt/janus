(declare-const s String)
(assert (distinct s (str.++ s s "H")))
(check-sat)
