(declare-const x String)
(assert (= (str.to_int x) (str.to_int "1765")))
(assert (= 1 1))
(check-sat)
