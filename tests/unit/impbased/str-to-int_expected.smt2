(declare-const x String)
(assert (= (str.to_int x) 1765))
(assert (= 1 (str.to_int "1")))
(check-sat)
