(declare-fun x () String)
(assert (str.in_re x (re.++ (str.to_re "r1") (str.to_re "r2") (re.union (str.to_re "r3a") (str.to_re "r3b")) (str.to_re "r4"))))
(check-sat)
